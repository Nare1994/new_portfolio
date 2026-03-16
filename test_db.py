import asyncpg
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env


async def test_connection():
    try:
        # Используем параметры из .env
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            database=os.getenv("POSTGRES_DB", "fastapi_shop"),
            host=os.getenv("POSTGRES_SERVER", "localhost"),
            port=os.getenv("POSTGRES_PORT", 5433)
        )
        print("✅ Успешное подключение к PostgreSQL!")

        # Проверим версию
        version = await conn.fetchval("SELECT version();")
        print(f"Версия PostgreSQL: {version}")

        await conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(test_connection())