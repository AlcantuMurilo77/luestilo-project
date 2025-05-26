from repositories.base import BaseRepository
from models.models import Order

class OrderRepository(BaseRepository[Order]):
    def __init__(self, session):
        super().__init__(Order, session)
