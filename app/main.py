from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.base import init_db

app = FastAPI(title="My Company Backend")

# Include routers
app.include_router(api_router, prefix="/api/v1")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
