from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session
    
    def get(self, id: int) -> Optional[ModelType]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list[ModelType]:
        return self.session.query(self.model).all()
    
    def create(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        self.session.commit()
        self.session.refresh(obj_in)
        return obj_in
    
    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        db_obj = self.session.query(self.model).get(id)
        if not db_obj:
            return None  

        for key, value in obj_in.items():
            setattr(db_obj, key, value)

        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> None:
        db_obj = self.session.query(self.model).get(id)
        if not db_obj:
            return  # ou lance uma exceção se preferir

        self.session.delete(db_obj)
        self.session.commit()
