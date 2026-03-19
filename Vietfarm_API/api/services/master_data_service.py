from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.repositories.base_repository import BaseRepository


def list_entities(repository: BaseRepository, db: Session, offset: int = 0, limit: int = 100):
    return repository.list(db, offset=offset, limit=limit)


def get_entity_or_404(repository: BaseRepository, db: Session, entity_id: str, entity_name: str):
    entity = repository.get(db, entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} not found: {entity_id}",
        )
    return entity


def create_entity(repository: BaseRepository, db: Session, payload: dict[str, Any], entity_name: str):
    try:
        return repository.create(db, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create {entity_name}: {str(exc)}",
        ) from exc


def update_entity(repository: BaseRepository, db: Session, entity: Any, payload: dict[str, Any], entity_name: str):
    try:
        return repository.update(db, entity, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update {entity_name}: {str(exc)}",
        ) from exc


def delete_entity(repository: BaseRepository, db: Session, entity: Any, entity_name: str):
    try:
        repository.delete(db, entity)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete {entity_name}: {str(exc)}",
        ) from exc
