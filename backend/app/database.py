from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os

from app.config import settings

_db_url = os.environ.get("DATABASE_URL", settings.database_url)
connect_args = {"check_same_thread": False} if _db_url.startswith("sqlite") else {}
engine = create_engine(_db_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
