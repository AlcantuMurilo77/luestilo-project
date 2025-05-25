from base import BaseRepository
from models.models import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)
