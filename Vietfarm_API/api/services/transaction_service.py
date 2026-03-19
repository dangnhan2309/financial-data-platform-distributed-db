from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.repositories.base_repository import BaseRepository


def create_transaction(repository: BaseRepository, db: Session, payload: dict, entity_name: str):
    try:
        return repository.create(db, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create {entity_name}: {str(exc)}",
        ) from exc
