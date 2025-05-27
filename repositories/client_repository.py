from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from models.models import Client
from repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):


    def __init__(self, session: Session):
        super().__init__(Client, session)

    def list(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Client]:
        query = self.session.query(self.model)

        if name:
            query = query.filter(self.model.name.ilike(f"%{name}%"))
        if email:
            query = query.filter(self.model.email.ilike(f"%{email}%"))

        return query.offset(skip).limit(limit).all()

    def get_by_email(self, email: str) -> Optional[Client]:
        return (
            self.session.query(self.model)
            .filter(self.model.email == email)
            .first()
        )

    def get_by_cpf(self, cpf: str) -> Optional[Client]:
        return (
            self.session.query(self.model)
            .filter(self.model.cpf == cpf)
            .first()
        )

