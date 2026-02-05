from sqlalchemy.orm import Session
from app.models.camera import Camera
from app.schemas.camera import CameraCreate, CameraUpdate


# Get one camera by ID
def get_camera(db: Session, camera_id: int):
    return db.query(Camera).filter(Camera.id == camera_id).first()


# Get all cameras
def get_cameras(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Camera).offset(skip).limit(limit).all()


# Create camera
def create_camera(db: Session, camera: CameraCreate):
    db_camera = Camera(name=camera.name)
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


# Update camera
def update_camera(db: Session, camera_id: int, camera_data: CameraUpdate):
    camera = get_camera(db, camera_id)
    if not camera:
        return None

    if camera_data.name is not None:
        camera.name = camera_data.name

    db.commit()
    db.refresh(camera)
    return camera


# Delete camera
def delete_camera(db: Session, camera_id: int):
    camera = get_camera(db, camera_id)
    if not camera:
        return None

    db.delete(camera)
    db.commit()
    return camera
