
from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    code: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    original_url: Mapped[str] = mapped_column(
        String(2048), nullable=False
    )
    title: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime (timezone=True), nullable=True
    )
