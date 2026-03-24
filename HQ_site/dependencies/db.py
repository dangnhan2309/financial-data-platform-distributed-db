from sqlalchemy.orm import Session
from core.database import SessionLocal


def get_db():
    """
    Dependency để lấy DB session
    FastAPI sẽ tự động mở và đóng session
    """

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()