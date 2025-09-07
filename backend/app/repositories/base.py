"""
Base repository implementing common CRUD operations.
Provides generic database operations for all repositories.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with CRUD operations.
    Implements Repository Pattern for data access abstraction.
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with model class.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Optional[ModelType]: Record if found, None otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_direction: str = "asc"
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Field name to order by
            order_direction: Order direction ('asc' or 'desc')
            
        Returns:
            List[ModelType]: List of records
        """
        query = db.query(self.model)
        
        if order_by:
            order_field = getattr(self.model, order_by, None)
            if order_field:
                if order_direction.lower() == "desc":
                    query = query.order_by(desc(order_field))
                else:
                    query = query.order_by(asc(order_field))
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Database session
            obj_in: Pydantic schema with creation data
            **kwargs: Additional fields not in schema
            
        Returns:
            ModelType: Created record
        """
        obj_data = obj_in.model_dump()
        obj_data.update(kwargs)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record.
        
        Args:
            db: Database session
            db_obj: Existing database object
            obj_in: Update data (schema or dictionary)
            
        Returns:
            ModelType: Updated record
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        Delete a record by ID.
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Optional[ModelType]: Deleted record if found, None otherwise
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def count(self, db: Session) -> int:
        """
        Count total records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total record count
        """
        return db.query(self.model).count()
    
    