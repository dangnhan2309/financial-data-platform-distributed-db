from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session
from sqlalchemy import desc

T = TypeVar('T')  # Generic type for any model


class BaseRepository(Generic[T]):
    """
    Base repository class providing generic CRUD operations.

    Usage:
    class CustomerRepository(BaseRepository[Customer]):
        pass

    repo = CustomerRepository(db=session, model=Customer)
    customers = repo.get_all()
    customer = repo.get_by_id(1)
    repo.create(data)
    """

    def __init__(self, db: Session, model: Type[T]):
        """
        Initialize repository with database session and model class.

        Args:
            db: SQLAlchemy session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    # ===== READ Operations =====

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all records with pagination.

        Args:
            skip: Number of records to skip (default: 0)
            limit: Max number of records to return (default: 100)

        Returns:
            List of model instances
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get single record by ID.

        Args:
            id: Record ID

        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_by_filter(self, **kwargs) -> List[T]:
        """
        Get records by filtering.

        Args:
            **kwargs: Column name = value pairs for filtering

        Returns:
            List of matching records

        Example:
            repo.get_by_filter(status="active", category="food")
        """
        query = self.db.query(self.model)
        for column, value in kwargs.items():
            if hasattr(self.model, column):
                query = query.filter(getattr(self.model, column) == value)
        return query.all()

    def get_one_by_filter(self, **kwargs) -> Optional[T]:
        """
        Get first record matching filter criteria.

        Args:
            **kwargs: Column name = value pairs for filtering

        Returns:
            First matching record or None
        """
        query = self.db.query(self.model)
        for column, value in kwargs.items():
            if hasattr(self.model, column):
                query = query.filter(getattr(self.model, column) == value)
        return query.first()

    def count(self) -> int:
        """Get total count of records."""
        return self.db.query(self.model).count()

    def get_recent(self, limit: int = 10) -> List[T]:
        """Get most recent records (requires created_at column)."""
        return self.db.query(self.model).order_by(
            desc(self.model.created_at)
        ).limit(limit).all()

    # ===== CREATE Operations =====

    def create(self, obj: T) -> T:
        """
        Create and save new record.

        Args:
            obj: Model instance with data

        Returns:
            Created model instance with ID

        Raises:
            Exception: If database error occurs
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error creating {self.model.__name__}: {str(e)}")

    def create_bulk(self, objects: List[T]) -> List[T]:
        """
        Create multiple records at once.

        Args:
            objects: List of model instances

        Returns:
            List of created instances with IDs
        """
        try:
            self.db.add_all(objects)
            self.db.commit()
            for obj in objects:
                self.db.refresh(obj)
            return objects
        except Exception as e:
            self.db.rollback()
            raise Exception(
                f"Error bulk creating {self.model.__name__}: {str(e)}")

    # ===== UPDATE Operations =====

    def update(self, id: int, data: dict) -> Optional[T]:
        """
        Update record by ID.

        Args:
            id: Record ID
            data: Dictionary of column:value pairs to update

        Returns:
            Updated model instance or None if not found

        Raises:
            Exception: If database error occurs
        """
        try:
            obj = self.get_by_id(id)
            if not obj:
                return None

            for key, value in data.items():
                if hasattr(obj, key) and key != 'id':
                    setattr(obj, key, value)

            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error updating {self.model.__name__}: {str(e)}")

    def update_multiple(self, filter_dict: dict, update_dict: dict) -> int:
        """
        Update multiple records matching filter.

        Args:
            filter_dict: Filter criteria
            update_dict: Values to update

        Returns:
            Number of records updated
        """
        try:
            query = self.db.query(self.model)
            for column, value in filter_dict.items():
                if hasattr(self.model, column):
                    query = query.filter(getattr(self.model, column) == value)

            count = query.update(update_dict)
            self.db.commit()
            return count
        except Exception as e:
            self.db.rollback()
            raise Exception(
                f"Error batch updating {self.model.__name__}: {str(e)}")

    # ===== DELETE Operations =====

    def delete(self, id: int) -> bool:
        """
        Delete record by ID.

        Args:
            id: Record ID

        Returns:
            True if deleted, False if not found

        Raises:
            Exception: If database error occurs
        """
        try:
            obj = self.get_by_id(id)
            if not obj:
                return False

            self.db.delete(obj)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error deleting {self.model.__name__}: {str(e)}")

    def delete_multiple(self, **kwargs) -> int:
        """
        Delete multiple records matching filter.

        Args:
            **kwargs: Filter criteria

        Returns:
            Number of records deleted
        """
        try:
            query = self.db.query(self.model)
            for column, value in kwargs.items():
                if hasattr(self.model, column):
                    query = query.filter(getattr(self.model, column) == value)

            count = query.delete()
            self.db.commit()
            return count
        except Exception as e:
            self.db.rollback()
            raise Exception(
                f"Error batch deleting {self.model.__name__}: {str(e)}")

    # ===== UTILITY Operations =====

    def exists(self, **kwargs) -> bool:
        """Check if record exists matching filter criteria."""
        return self.get_one_by_filter(**kwargs) is not None
