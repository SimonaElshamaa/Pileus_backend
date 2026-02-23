from pydantic import BaseModel, Field
from typing import Optional

class IMSBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class IMSCreate(IMSBase):
    pass

class IMSUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)

class IMSOut(IMSBase):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2