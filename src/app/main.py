from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app import models  # noqa: F401
from src.app.api.v1 import api_router
from src.app.core.config import settings
from src.app.core.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
