from sqlalchemy.orm import Session
from app.crud.camera import get_camera, get_cameras, create_camera, update_camera, delete_camera
from app.schemas.camera import CameraCreate, CameraUpdate


# Get one camera
def get_camera_by_id(db: Session, camera_id: int):
    camera = get_camera(db, camera_id)
    if not camera:
        return None  # or raise exception here if you want
    return camera


# Get all cameras with optional pagination
def list_cameras(db: Session, skip: int = 0, limit: int = 100):
    return get_cameras(db, skip=skip, limit=limit)


# Create new camera with some business rules
def add_camera(db: Session, camera_data: CameraCreate):
    # Example business rule: name must be capitalized
    camera_data.name = camera_data.name.title()
    return create_camera(db, camera_data)


# Update camera
def modify_camera(db: Session, camera_id: int, camera_data: CameraUpdate):
    # Example business rule: trim whitespace
    if camera_data.name:
        camera_data.name = camera_data.name.strip()
    return update_camera(db, camera_id, camera_data)


# Delete camera
def remove_camera(db: Session, camera_id: int):
    return delete_camera(db, camera_id)