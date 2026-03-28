from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from api.utils.database import SessionLocal, engine


def get_session() -> Session:
    return SessionLocal()


def has_table(table_name: str) -> bool:
    inspector = inspect(engine)
    return inspector.has_table(table_name)


def bulk_insert(db: Session, objects: Sequence[object], chunk_size: int = 500) -> None:
    if not objects:
        return
    for index in range(0, len(objects), chunk_size):
        db.bulk_save_objects(objects[index: index + chunk_size])
