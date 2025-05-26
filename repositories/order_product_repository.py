from repositories.base import BaseRepository
from models.models import OrderProduct

class OrderProductRepository(BaseRepository[OrderProduct]):
    def __init__(self, session):
        super().__init__(OrderProduct, session)
