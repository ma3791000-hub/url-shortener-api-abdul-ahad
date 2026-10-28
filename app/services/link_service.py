from sqlalchemy.exc import IntegrityError
import secrets
import string
from datetime import datetime

from sqlalchemy.orm import Session

from app.config import BASE_URL
from app.models import Link


def generate_short_code(length: int = 7) -> str:
    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def create_unique_code(db: Session) -> str:
    while True:
        code = generate_short_code()

        existing_link = (
            db.query(Link)
            .filter(Link.code == code)
            .first()
        )

        if existing_link is None:
            return code



def create_link(
    db: Session,
    original_url: str,
    custom_alias: str | None = None,
    expires_at: datetime | None = None,
) -> Link:
    if custom_alias:
        existing_link = (
            db.query(Link)
            .filter(Link.code == custom_alias)
            .first()
        )

        if existing_link is not None:
            raise ValueError("This custom alias is already in use.")

        code = custom_alias
    else:
        code = create_unique_code(db)

    new_link = Link(
        code=code,
        original_url=original_url,
        expires_at=expires_at,
    )

    
    db.add(new_link)

    try:
        db.commit()
        db.refresh(new_link)
    except IntegrityError as error:
        db.rollback()
        raise ValueError(
            "This custom alias is already in use."
        ) from error

    return new_link

