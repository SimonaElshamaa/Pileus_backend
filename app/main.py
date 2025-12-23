from fastapi import FastAPI
from app.api import user
from app.db.base import init_db

app = FastAPI(title="My Company Backend")

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
