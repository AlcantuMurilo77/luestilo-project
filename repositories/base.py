from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session) -> list[ModelType]:
        return db.query(self.model).all()
    
    def create(self, db: Session, obj_in:dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()
