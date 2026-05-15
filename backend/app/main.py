from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.exceptions import register_exception_handlers
from app.middleware.security import SecurityHeadersMiddleware
from app.routers import admin, auth, bookings, cleaning, guests, items, reports, rooms, stays
from app.seed import seed_database

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API для управления гостиницей (номера, бронирование, уборка, отчёты).",
    lifespan=lifespan,
)
register_exception_handlers(app)
app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)

app.include_router(items.router)

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(guests.router)
app.include_router(bookings.router)
app.include_router(stays.router)
app.include_router(cleaning.router)
app.include_router(reports.router)
app.include_router(admin.router)


@app.get("/", tags=["meta"])
def read_root() -> dict[str, str]:
    return {"message": "Hotel Management API is running."}


@app.get("/health", tags=["meta"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/health", tags=["meta"])
def api_health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
