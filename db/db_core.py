import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.config import db_config
from db.models import Base

# Создаем движок БД
engine = create_async_engine(db_config.url(), echo=True)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)

# Управление сессиями
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Создаем таблицы в БД
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# if __name__ == '__main__':
#     asyncio.run(create_tables())
#     print("Tables created!")