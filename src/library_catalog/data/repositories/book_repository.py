from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from base_repository import BaseRepository
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
                    Book.title == title if title else True,
                    Book.author == author if author else True,
                    Book.genre == genre if genre else True,
                    Book.year == year if year else True,
                    Book.avialable == available if available else True
                )
            ).offset(offset).limit(limit)
        )
        return result.scalars().all()
    
    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        pass
    
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
            select(Book).where(
                and_(
                    Book.title == title if title else True,
                    Book.author == author if author else True,
                    Book.genre == genre if genre else True,
                    Book.year == year if year else True,
                    Book.avialable == available if available else True
                )
            ).offset(offset).limit(limit)
        )
        return result.scalars().all()
