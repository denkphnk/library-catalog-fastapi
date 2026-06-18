from ..base.base_client import BaseApiClient
from ...domain.exceptions import OpenLibraryException, OpenLibraryTimeoutException

import httpx

class OpenLibraryClient(BaseApiClient):
    """Клиент для Open Library API."""
    
    def __init__(
        self,
        base_url: str = "https://openlibrary.org",
        timeout: float = 10.0,
    ):
        super().__init__(base_url, timeout=timeout)
    
    def client_name(self) -> str:
        return "openlibrary"
    

    async def search_by_title_author(
        self,
        title: str,
        author: str
    ) -> dict:
        """Поиск по названию и автору."""
        try:
            data = await self._get(
                "/search.json",
                params={
                    "title": title,
                    "author": author,
                    "limit": 1
                }
            )
            
            docs = data.get("docs", [])
            if not docs:
                return {}
            
            return self._extract_book_data(docs[0])
        
        except httpx.TimeoutException:
            raise OpenLibraryTimeoutException(self.timeout)
        except httpx.HTTPError as e:
            raise OpenLibraryException(str(e))
    
    async def enrich(
        self,
        title: str,
        author: str,
        isbn: str | None = None,
    ) -> dict:
        """
        Обогатить данные книги.
        
        Пытается по title+author.
        
        Returns:
            dict: Обогащенные данные или пустой словарь
        """
        
        return await self.search_by_title_author(title, author)
    
    def _extract_book_data(self, doc: dict) -> dict:
        """
        Извлечь нужные поля из ответа Open Library.
        
        Args:
            doc: Документ из массива docs
            
        Returns:
            dict: Обработанные данные
        """
        result = {}
        
        # Cover URL
        if cover_id := doc.get("cover_i"):
            result["cover_url"] = (
                f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            )
        
        # Subjects (темы)
        if subjects := doc.get("subject"):
            result["subjects"] = subjects[:10]  # Первые 10
        
        # Publisher
        if publisher := doc.get("publisher"):
            result["publisher"] = publisher[0] if publisher else None
        
        # Language
        if language := doc.get("language"):
            result["language"] = language[0] if language else None
        
        # Ratings
        if ratings := doc.get("ratings_average"):
            result["rating"] = ratings
        
        return result