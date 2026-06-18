from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_
from .base_repository import BaseRepository
from ..models.book import Book

class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)
    
    async def find_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Book]:
        """Поиск книг с фильтрацией."""
        result = await self.session.execute(
            select(Book).where(
                and_(
                    Book.title.ilike(f"%{title}%") if title else True,
                    Book.author.ilike(f"%{author}%") if author else True,
                    Book.genre == genre if genre else True,
                    Book.year == year if year else True,
                    Book.available == available if available else True
                )
            ).offset(offset).limit(limit)
        )
        return result.scalars().all()
    
    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        res = await self.session.execute(
            select(Book)
            .where(Book.isbn == isbn)
        )
        return res.scalar_one_or_none()
    
    async def count_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> int:
        """Подсчитать количество книг по фильтрам."""
        result = await self.session.execute(
            select(func.count()).select_from(Book).where(
                and_(
                    Book.title.ilike(f"%{title}%") if title else True,
                    Book.author.ilike(f"%{author}%") if author else True,
                    Book.genre == genre if genre else True,
                    Book.year == year if year else True,
                    Book.available == available if available else True
                )
            )
        )
        return result.scalar_one()
