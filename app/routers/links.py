
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config import BASE_URL
from app.database import get_db
from app.models import Click, Link
from app.schemas import LinkCreate
from app.services.link_service import create_link


router = APIRouter(
    prefix="/api/links",
    tags=["Links"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_short_link(
    link_data: LinkCreate,
    db: Session = Depends(get_db),
):
    try:
        link = create_link(
            db=db,
            original_url=str(link_data.url),
            custom_alias=link_data.custom_alias,
            expires_at=link_data.expires_at,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return {
        "id": link.id,
        "code": link.code,
        "original_url": link.original_url,
        "short_url": f"{BASE_URL}/{link.code}",
        "created_at": link.created_at,
        "expires_at": link.expires_at,
    }


@router.get("/")
def list_links(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Link).count()

    links = (
        db.query(Link)
        .order_by(Link.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "links": [
            {
                "id": link.id,
                "code": link.code,
                "original_url": link.original_url,
                "short_url": f"{BASE_URL}/{link.code}",
                "created_at": link.created_at,
                "expires_at": link.expires_at,
            }
            for link in links
        ],
    }
@router.delete("/{code}")
def delete_short_link(
    code: str,
    db: Session = Depends(get_db),
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