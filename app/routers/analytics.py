
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Click, Link


router = APIRouter(
    prefix="/api/links",
    tags=["Analytics"],
)


@router.get("/{code}/stats")
def get_link_stats(
    code: str,
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

    total_clicks = (
        db.query(func.count(Click.id))
        .filter(Click.link_id == link.id)
        .scalar()
    )

    seven_days_ago = datetime.utcnow() - timedelta(days=6)
    daily_results = (
        db.query(
            func.date(Click.clicked_at).label("day"),
            func.count(Click.id).label("clicks"),
        )
        .filter(
            Click.link_id == link.id,
            Click.clicked_at >= seven_days_ago,
        )
        .group_by(func.date(Click.clicked_at))
        .all()
    )

    daily_counts = {
        row.day: row.clicks
        for row in daily_results
    }

    clicks_per_day = []
    for i in range(7):
        day = (seven_days_ago + timedelta(days=i)).date().isoformat()
        clicks_per_day.append({
            "date": day,
            "clicks": daily_counts.get(day, 0),
        })

    top_referrers = (
        db.query(
            Click.referrer,
            func.count(Click.id).label("clicks"),
        )
        .filter(
            Click.link_id == link.id,
            Click.referrer.isnot(None),
            Click.referrer != "",
        )
        .group_by(Click.referrer)
        .order_by(func.count(Click.id).desc())
        .limit(3)
        .all()
    )

    return {
        "code": link.code,
        "title": link.title,
        "total_clicks": total_clicks,
        "clicks_per_day": clicks_per_day,
        "top_referrers": [
            {
                "referrer": row.referrer,
                "clicks": row.clicks,
            }
            for row in top_referrers
        ],
    }
