from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime

from src.library_catalog.core.database import Base

import uuid
import datetime

class Book(Base):
    """Model for books table"""
    __tablename__ = 'books'

    book_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title: Mapped[str] = mapped_column(String[500], index=True, nullable=False)
    author: Mapped[str] = mapped_column(String[300], index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    genre: Mapped[str] = mapped_column(String[100], index=True)
    pages: Mapped[int] = mapped_column(Integer)
    available: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now, nullable=False)


    def __repr__(self) -> str:
        return f"<Book(id={self.book_id}, title='{self.title}')>"