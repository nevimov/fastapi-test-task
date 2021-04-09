from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.crud.base import CRUDBase
from app.exceptions import ShortUrlExists, ReservedUrl, UrlLimitExceeded
from app.models.shorturl import ShortUrl
from app.schemas.shorturl import ShortUrlCreate, ShortUrlUpdate
from app.utils import get_random_string


class CRUDShortUrl(CRUDBase[ShortUrl, ShortUrlCreate, ShortUrlUpdate]):

    def get_by_key(self, db: Session, key: str) -> Optional[ShortUrl]:
        """
        Get a short URL using its `key`.

        The key is a part of the short URL that follows the domain and slash.
        For example, given the URL 'shurl.me/foo-bar', the key is 'foo-bar'.
        """
        return db.query(ShortUrl).filter(ShortUrl.key == key).first()

    def create_with_owner(self, db: Session, owner_id: int,
                          obj_in: ShortUrlCreate,
                          reserved: list = []) -> ShortUrl:
        """
        Create a new short URL and associate it with the given user.
        """
        urlkey = obj_in.key

        if urlkey in reserved:
            raise ReservedUrl

        # Limit the number of short URLs a user may create.
        if crud.user.count_urls(db, owner_id) >= settings.USER_SHORTURL_LIMIT:
            raise UrlLimitExceeded
        # XXX: This solution is likely to be prone to race conditions.
        # TODO: Investigate alternative solutions like locking or using a
        # CHECK CONSTRAINT + storing the URL counts in DB.

        # If the user did enter a desired short URL, try to save it to the
        # database and raise an exception, if a URL with such path already
        # exists.
        if urlkey:
            db_obj = ShortUrl(owner_id=owner_id, **obj_in.dict())
            db.add(db_obj)
            try:
                db.commit()
            except IntegrityError:
                raise ShortUrlExists(urlkey)
            db.refresh(db_obj)
            return db_obj

        # If the user did not enter a desired short URL, generate one randomly.
        while True:
            key = get_random_string(length=7)
            if key in reserved:
                continue

            db_obj = ShortUrl(
                key=key,
                # 7 should be more than enough. We use: 52 letters + 10 digits
                # = 72 characters. This gives us 72**7 = 10 030 613 004 288
                # possible combinations.
                destination=obj_in.destination,
                owner_id=owner_id,
            )
            db.add(db_obj)
            try:
                db.commit()
            except IntegrityError:
                continue  # Just try again, if the short URL key already exists
            else:
                db.refresh(db_obj)
                return db_obj

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0,
                           limit: int = 100) -> List[ShortUrl]:
        """
        Get up to `limit` short URLs owned by the given user.

        If `skip` is specified, the first `skip` records will be skipped.
        """
        return (
            db.query(self.model)
            .filter(ShortUrl.owner_id == owner_id)
            .order_by(desc(ShortUrl.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

shorturl = CRUDShortUrl(ShortUrl)
