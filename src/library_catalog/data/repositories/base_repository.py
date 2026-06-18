from typing import Generic, TypeVar, Type
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def create(self, **kwargs) -> T:
        """Создать запись."""
        new_record = self.model(**kwargs)
        self.session.add(new_record)
        await self.session.commit()
        await self.session.refresh(new_record)
        return new_record
    
    async def get_by_id(self, id: UUID) -> T | None:
        """
        Получить по ID.
        
        📝 Примечание: session.get() автоматически работает с primary key модели,
        независимо от его названия (id, book_id, user_id и т.д.)
        """


        return await self.session.get(self.model, id)
    
    async def update(self, id: UUID, **kwargs) -> T | None:
        """Обновить запись."""
        record = await self.session.get(self.model, id)

        if not record:
            return None
        
        for key, value in kwargs.items():
            setattr(record, key, value)
        
        await self.session.commit()
        return record
    
    async def delete(self, id: UUID) -> bool:
        """Удалить запись."""
        record = await self.session.get(self.model, id)
        if not record:
            return False
        
        await self.session.delete(record)
        await self.session.commit()
        return True
    
    async def get_all(self, limit: int = 100, offset: int = 0,
    ) -> list[T]:
        """Получить все записи с пагинацией."""
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()
