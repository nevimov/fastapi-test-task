from fastapi import APIRouter, Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, deps

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/")


@router.get("/", name="my-urls", summary="Display User URLs page",
            response_class=HTMLResponse)
async def display_user_urls(request: Request):
    """
    Display a page listing all short URLs created by the user.
    """
    return templates.TemplateResponse(
        "my-urls.html",
        {"request": request}
    )


@router.get("/login", name="login", summary="Display Login Page",
            response_class=HTMLResponse)
async def display_login_page(request: Request):
    """
    Display a login page that allows the user to get a JWT token required to
    access auth-protected pages (like "My URLs").
    """
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# NOTE: This path function MUST BE the last one registered.
@router.get("/{short_url_key}")
async def redirect_short_url(short_url_key, db: Session = Depends(deps.get_db)):
    """
    Redirect the user to the destination associated with the `short_url_key`.
    """
    short_url = crud.shorturl.get_by_key(db, short_url_key)
    if not short_url:
        raise HTTPException(404, "Page Not Found")
    return RedirectResponse(short_url.destination)
