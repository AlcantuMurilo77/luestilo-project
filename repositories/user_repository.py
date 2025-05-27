from typing import Optional
from repositories.base import BaseRepository
from models.models import User
from sqlalchemy.future import select

class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = self.session.execute(stmt).first()
        if result:
            return result[0]
        return None
