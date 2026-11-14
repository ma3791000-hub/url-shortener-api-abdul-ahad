
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class LinkCreate(BaseModel):
    url: HttpUrl
    custom_alias: str | None = Field(default=None, min_length=6, max_length=8)
    expires_at: datetime | None = None
    title: str | None = Field(default=None, max_length=255)


class LinkUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    expires_at: datetime | None = None


class LinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    original_url: str
    short_url: str
    created_at: datetime
    expires_at: datetime | None = None
    title: str | None = None


class LinkListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    links: list[LinkResponse]


class DailyClickStats(BaseModel):
    date: str
    clicks: int


class TopReferrerStats(BaseModel):
    referrer: str
    clicks: int


class LinkStatsResponse(BaseModel):
    code: str
    title: str | None = None
    total_clicks: int
    clicks_per_day: list[DailyClickStats]
    top_referrers: list[TopReferrerStats]
