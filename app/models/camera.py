from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime



class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
