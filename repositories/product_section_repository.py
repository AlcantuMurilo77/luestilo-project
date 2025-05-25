from base import BaseRepository
from models.models import ProductSection

class ProductSectionRepository(BaseRepository[ProductSection]):
    def __init__(self):
        super().__init__(ProductSection)
