from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
import logging
from contextlib import contextmanager

# Construct the database URL
DATABASE_URL = f"postgresql://{settings.SYNTHETIC_DB_USER}:{settings.SYNTHETIC_DB_PASSWORD}@{settings.SYNTHETIC_DB_HOST}/{settings.SYNTHETIC_DB_NAME}"

# Create a synchronous engine
engine = create_engine(DATABASE_URL, future=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Dependency to get the database session
@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
