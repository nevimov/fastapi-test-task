from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from app import crud, deps, models, schemas
from app.core.config import settings
from app.exceptions import ShortUrlExists, ReservedUrl, UrlLimitExceeded

router = APIRouter()


@router.get("/", name="api-get-urls", summary="Get User URLs",
            response_model=List[schemas.ShortUrl])
def read_short_urls(
    response: Response,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0, le=settings.USER_SHORTURL_LIMIT),
    limit: int = Query(50, ge=1, le=settings.USER_SHORTURL_LIMIT),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get short URLs associated with the current User.
    """
    if crud.user.is_superuser(current_user):
        short_urls = crud.shorturl.get_multi(db, skip=skip, limit=limit)
    else:
        short_urls = crud.shorturl.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    count = min(  # Doesn't Protect the API !
        crud.user.count_urls(db=db, user_id=current_user.id),
        settings.USER_SHORTURL_LIMIT,
    )
    response.headers["X-User-Url-Count"] = str(count)
    return short_urls


@router.post("/", name="api-create-url", summary="Create URL",)
def create_short_url(
    request: Request,
    *,
    db: Session = Depends(deps.get_db),
    shorturl_in: schemas.ShortUrlCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a short URL associated with the current user.
    """
    reserved = [route.path[1:] for route in request.app.routes]
    try:
        return crud.shorturl.create_with_owner(
            db=db,
            obj_in=shorturl_in,
            owner_id=current_user.id,
            reserved=reserved,
        )
    except UrlLimitExceeded:
        raise HTTPException(403, detail="You've created too many URLs!")
    except ShortUrlExists:
        raise HTTPException(
            400,
            detail=[{
                "loc": ["body", "key"],
                "msg": "Such short URL already exists",
                "type": "custom.value_error",
            }]
        )
    except ReservedUrl:
        raise HTTPException(
            400,
            detail=[{
                "loc": ["body", "key"],
                "msg": "This URL is reserved! Please use another one.",
                "type": "custom.value_error",
            }]
        )
