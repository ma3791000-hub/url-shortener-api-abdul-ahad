
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Click(Base):
    __tablename__ = "clicks"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    link_id: Mapped[int] = mapped_column(
        ForeignKey("links.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    clicked_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    referrer: Mapped[str | None] = mapped_column(
        String(2048), nullable=True
    )
