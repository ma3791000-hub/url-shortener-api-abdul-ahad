from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config import BASE_URL
from app.database import get_db
from app.models import Click, Link
from app.schemas.link import (
    LinkCreate,
    LinkUpdate,
    LinkResponse,
    LinkListResponse,
)
from app.services.link_service import create_link
from app.security import verify_api_key


router = APIRouter(
    prefix="/api/links",
    tags=["Links"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=LinkResponse,
)
def create_short_link(
    link_data: LinkCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    try:
        link = create_link(
            db=db,
            original_url=str(link_data.url),
            custom_alias=link_data.custom_alias,
            expires_at=link_data.expires_at,
            title=link_data.title,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return LinkResponse(
        id=link.id,
        code=link.code,
        original_url=link.original_url,
        short_url=f"{BASE_URL}/{link.code}",
        created_at=link.created_at,
        expires_at=link.expires_at,
        title=link.title,
    )


@router.patch(
    "/{code}",
    response_model=LinkResponse,
)
def update_short_link(
    code: str,
    link_data: LinkUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    link = db.query(Link).filter(Link.code == code).first()

    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short link not found",
        )

    update_data = link_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(link, field, value)

    db.commit()
    db.refresh(link)

    return LinkResponse(
        id=link.id,
        code=link.code,
        original_url=link.original_url,
        short_url=f"{BASE_URL}/{link.code}",
        created_at=link.created_at,
        expires_at=link.expires_at,
        title=link.title,
    )

@router.get(
    "/",
    response_model=LinkListResponse,
)
def list_links(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    status: str = Query(default="all", pattern="^(active|expired|all)$"),
    db: Session = Depends(get_db),
):
    query = db.query(Link)
    if search:
        query = query.filter(
            Link.title.ilike(f"%{search}%")
        )
    from datetime import datetime, timezone

    current_time = datetime.now(timezone.utc)

    if status == "active":
        query = query.filter(
            (Link.expires_at.is_(None)) |
            (Link.expires_at > current_time)
        )

    elif status == "expired":
        query = query.filter(
            Link.expires_at.isnot(None),
            Link.expires_at <= current_time
        )

    total = query.count()

    links = (
        query
        .order_by(Link.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    response_links = [
        LinkResponse(
            id=link.id,
            code=link.code,
            original_url=link.original_url,
            short_url=f"{BASE_URL}/{link.code}",
            created_at=link.created_at,
            expires_at=link.expires_at,
            title=link.title,
        )
        for link in links
    ]

    return LinkListResponse(
        page=page,
        page_size=page_size,
        total=total,
        links=response_links,
    )



@router.delete("/{code}")
def delete_short_link(
    code: str,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    link = db.query(Link).filter(Link.code == code).first()

    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short link not found",
        )

    db.query(Click).filter(
        Click.link_id == link.id
    ).delete(synchronize_session=False)

    db.delete(link)
    db.commit()

    return {
        "message": "Short link and click data deleted successfully",
        "code": code,
    }