from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Базовый репозиторий с общими методами
    """
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def get(self, id: str) -> ModelType | None:
        """
        Получить запись по ID
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100):
        """
        Получить несколько записей
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs) -> ModelType:
        """
        Создать новую запись
        """
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: str, **kwargs) -> ModelType | None:
        """
        Обновить запись
        """
        obj = await self.get(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await self.db.commit()
            await self.db.refresh(obj)
        return obj

    async def delete(self, id: str) -> bool:
        """
        Удалить запись
        """
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return True
        return False