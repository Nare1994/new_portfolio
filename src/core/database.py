from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings

# Создаём асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.database_url,
    echo=True,  # Логировать SQL запросы (полезно для разработки)
    future=True,
)

# Создаём фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """
    Зависимость для получения сессии базы данных
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()