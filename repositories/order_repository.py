from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models.models import Order, OrderProduct
from repositories.base import BaseRepository
from datetime import datetime
from typing import Optional, List

class OrderRepository(BaseRepository[Order]):
    def __init__(self, session):
        super().__init__(Order, session)

    async def get_all(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        section_id: Optional[int] = None,
        order_id: Optional[int] = None,
        status: Optional[str] = None,
        client_id: Optional[int] = None
    ) -> List[Order]:
        query = select(Order).options(joinedload(Order.products).joinedload(OrderProduct.product))

        if order_id:
            query = query.where(Order.id == order_id)
        if status:
            query = query.where(Order.status == status)
        if client_id:
            query = query.where(Order.client_id == client_id)
        if start_date:
            query = query.where(Order.created_at >= start_date)
        if end_date:
            query = query.where(Order.created_at <= end_date)

        results = (await self.session.execute(query)).scalars().unique().all()


        if section_id:
            results = [
                order for order in results
                if any(op.product.section_id == section_id for op in order.products)
            ]

        return results
