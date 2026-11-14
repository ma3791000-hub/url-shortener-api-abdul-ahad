from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
def to_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
class LinkCreate(BaseModel):
    url: HttpUrl
    custom_alias: str | None = Field(default=None, min_length=6, max_length=8)
    expires_at: datetime | None = None
    title: str | None = Field(default=None, max_length=255)

    @field_validator("expires_at")
    @classmethod
    def normalize_expires_at(cls, value):
        return to_utc(value)


class LinkUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    expires_at: datetime | None = None

    @field_validator("expires_at")
    @classmethod
    def normalize_expires_at(cls, value):
        return to_utc(value)


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