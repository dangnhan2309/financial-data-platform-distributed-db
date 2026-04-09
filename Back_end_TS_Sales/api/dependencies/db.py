from fastapi import Depends
from sqlalchemy.orm import Session
from api.utils.database import SessionLocal


def get_db():
    """
    Dependency to get database session.
    This is used in FastAPI endpoints as: db: Session = Depends(get_db)

    FastAPI will:
    1. Call SessionLocal() to get a session
    2. Pass it to your endpoint
    3. Automatically close it after the endpoint returns
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
