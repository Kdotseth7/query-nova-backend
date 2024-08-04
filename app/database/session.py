from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
import logging

DATABASE_URL = f"postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

if __name__ == "__main__":
    print(DATABASE_URL)