from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Open DB connection and ensure indexes
    await connect_to_mongo()
    yield
    # Shutdown: Cleanly disconnect
    await close_mongo_connection()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}