from repositories.base import BaseRepository
from models.models import Product
from sqlalchemy.future import select
from sqlalchemy import and_

class ProductRepository(BaseRepository[Product]):
    def __init__(self, session):
        super().__init__(Product, session)
    
    async def get_all(
    self,
    min_price: float | None = None,
    max_price: float | None = None,
    category_filter: int | None = None,
    availability_filter: bool | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Product]:

        stmt = select(self.model)
        conditions = []

        if min_price is not None:
            conditions.append(self.model.selling_price >= min_price)
        if max_price is not None:
            conditions.append(self.model.selling_price <= max_price)
        if category_filter is not None:
            conditions.append(self.model.category_id == category_filter)
        if availability_filter is not None:
            conditions.append(self.model.availability == availability_filter)
        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

