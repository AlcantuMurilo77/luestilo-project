from repositories.base import BaseRepository
from models.models import ProductSection

class ProductSectionRepository(BaseRepository[ProductSection]):
    def __init__(self, session):
        super().__init__(ProductSection, session)
