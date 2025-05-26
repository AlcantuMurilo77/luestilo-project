from repositories.base import BaseRepository
from models.models import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self, session):
        super().__init__(Product, session)
    
    '''def get_all(self, price_filter, category_filter, availability_fitler) -> list[Product]:
        query = self.session.query(self.model)
        if price_filter:
            query.filter(self.model.price <= price_filter)
        
        return query.all()'''
