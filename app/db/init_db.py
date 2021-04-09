"""
Populate the database with initial data.
"""
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.db import base  # noqa
# NOTE: Make sure all SQL Alchemy models are imported (app.db.base) before
# initializing DB, otherwise, SQL Alchemy might fail to initialize
# relationships properly.
# For more details, see:
# https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.utils import get_random_string


def create_dev_data(db: Session) -> None:
    """
    Create some dummy data for the development environment.
    """
    # Create a non-staff user for testing purposes
    user = crud.user.get_by_email(db, email="user@example.com")
    if not user:
        user_in = schemas.UserCreate(
            email="user@example.com",
            password="dummypass",
            is_superuser=False,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    else:
        db.query(models.ShortUrl).filter(models.ShortUrl.owner_id == user.id).delete()

    # Create some shortened URLs and associate them with the test user.
    for _ in range(310):
        obj_in = schemas.ShortUrlCreate(
            destination=f"https://google.com/?q={get_random_string(40)}"
        )
        crud.shorturl.create_with_owner(
            db=db,
            owner_id=user.id,
            obj_in=obj_in,
        )


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    # Create the initial superuser account
    superuser = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not superuser:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(db, obj_in=user_in)

    create_dev_data(db)