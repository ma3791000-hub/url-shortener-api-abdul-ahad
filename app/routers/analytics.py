
from datetime import datetime, timedelta,timezone

from fastapi import APIRouter, Depends, HTTPException,Query
from app.schemas.link import LinkStatsResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Click, Link


router = APIRouter(
    prefix="/api/links",
    tags=["Analytics"],
)


@router.get("/{code}/stats", response_model=LinkStatsResponse)
def get_link_stats(
    code: str,
     days: int = Query(default=7, ge=1, le=30),
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

    current_time = datetime.now(timezone.utc)
    start_date = current_time.date() - timedelta(days=days - 1)

    start_datetime = datetime.combine(
    start_date,
    datetime.min.time(),
    tzinfo=timezone.utc,
)
    daily_results = (
        db.query(
            func.date(Click.clicked_at).label("day"),
            func.count(Click.id).label("clicks"),
        )
        .filter(
            Click.link_id == link.id,
            Click.clicked_at >= start_datetime,
        )
        .group_by(func.date(Click.clicked_at))
        .all()
    )

    daily_counts = {
        row.day: row.clicks
        for row in daily_results
    }

    clicks_per_day = []
    for i in range(days):
        day = (start_date + timedelta(days=i)).isoformat()
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
