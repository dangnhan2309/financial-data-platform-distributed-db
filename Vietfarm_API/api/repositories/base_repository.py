from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def list(self, db: Session, offset: int = 0, limit: int = 100) -> list[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.scalars(stmt).all())

    def get(self, db: Session, entity_id: Any) -> T | None:
        return db.get(self.model, entity_id)

    def create(self, db: Session, payload: dict[str, Any]) -> T:
        entity = self.model(**payload)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db: Session, entity: T, payload: dict[str, Any]) -> T:
        for field, value in payload.items():
            setattr(entity, field, value)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity: T) -> None:
        db.delete(entity)
        db.commit()
