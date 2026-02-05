from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.camera import CameraOut
from app.models.camera import Camera
from app.core.dependancies import get_db

router = APIRouter()

@router.get("/")
def list_cameras():
    return [{"id": 1, "name": "Camera1"}]

@router.get("/cameras/{id}", response_model=CameraOut)
def get_camera(id: int, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == id).first()

    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    return camera
