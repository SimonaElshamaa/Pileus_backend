from pydantic import BaseModel, Field
from typing import Optional

class CameraBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class CameraCreate(CameraBase):
    pass

class CameraUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)

class CameraOut(CameraBase):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2
