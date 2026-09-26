from __future__ import annotations

from fastapi import FastAPI

from app.api import router as api_router
from app.config import settings
from app.database import Base, engine
from app.models import Booking, Contractor, Guest, Listing, Message, WorkOrder  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version="0.1.0")
    app.include_router(api_router, prefix="/api")

    @app.get("/")
    async def root():
        return {"app": settings.APP_NAME, "status": "running"}

    @app.on_event("startup")
    def startup_event():
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
