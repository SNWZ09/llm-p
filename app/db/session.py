#создаём асинхронный engine SQLAlchemy и фабрику сессий
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
#импорт настроек (нам потребуется SQLITE_PATH)
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{settings.sqlite_path}'

#создаем engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False
)

#создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False, #чтобы после сохранения мы могли читать данные
    class_=AsyncSession
)
