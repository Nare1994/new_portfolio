from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User
from src.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    Репозиторий для работы с пользователями
    """
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        """
        Получить пользователя по email
        """
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, email: str, hashed_password: str, full_name: str | None = None) -> User:
        """
        Создать нового пользователя
        """
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_superuser=False
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: str) -> User | None:
        """
        Получить пользователя по ID
        """
        return await self.get(user_id)