from models.models import Client
from repositories.base import BaseRepository

class ClientRepository(BaseRepository[Client]):
    def __init__(self, session):
        super().__init__(Client, session)
