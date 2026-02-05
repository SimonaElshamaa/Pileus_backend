
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Create Engine (DB Connection)
engine = create_engine(
    settings.database_url,
    echo=False,  # True only in development if you want SQL logs
    pool_size=10,
    max_overflow=20
)

# 2. Create Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
