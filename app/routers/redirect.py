
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Link, Click


router = APIRouter(tags=["Redirect"])


@router.get("/{code}")
def redirect_to_original(
    code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    link = (
        db.query(Link)
        .filter(Link.code == code)
        .first()
    )

    if link is None:
        raise HTTPException(
            status_code=404,
            detail="Short link not found",
        )

    if link.expires_at is not None:
        expiry = link.expires_at

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

        if expiry <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=410,
                detail="This short link has expired",
            )

    click = Click(
        link_id=link.id,
        clicked_at=datetime.now(timezone.utc),
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer"),
    )

    db.add(click)
    db.commit()

    return RedirectResponse(
        url=link.original_url,
        status_code=302,
    )
