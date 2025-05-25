from base import BaseRepository
from models.models import ProductCategory

class ProductCategoryRepository(BaseRepository[ProductCategory]):
    def __init__(self):
        super().__init__(ProductCategory)
