from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from models.models import Order, Product, ProductCategory, ProductSection, OrderProduct
from app.network.schemas.order import OrderCreate, OrderUpdate
from repositories.base import BaseRepository

class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: Session):
        super().__init__(Order, session)
        self.session = session

    def list(
        self,
        category_name: Optional[str] = None,
        section_name: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Order]:
        query = self.session.query(Order).join(Order.products).join(OrderProduct.product)

        if category_name:
            query = query.join(Product.category).filter(ProductCategory.name == category_name)

        if section_name:
            query = query.join(Product.section).filter(ProductSection.name == section_name)

        if price_min is not None:
            query = query.filter(Product.price >= price_min)

        if price_max is not None:
            query = query.filter(Product.price <= price_max)

        if available is not None:
            query = query.filter(Product.available == available)


        query = query.options(
                joinedload(Order.products).joinedload(OrderProduct.product),
                joinedload(Order.client)  
        )

        return query.offset(skip).limit(limit).all()


    def get(self, id: int) -> Optional[Order]:
        return self.session.query(Order).options(
            joinedload(Order.products).joinedload(OrderProduct.product),
            joinedload(Order.client)  
        ).filter(Order.id == id).first()

    def create(self, obj_in: OrderCreate) -> Order:
        new_order = Order(
            client_id=obj_in.client_id,
            status=obj_in.status or "pending",
        )

        new_order.products = [
            OrderProduct(
                product_id=product.product_id,
                quantity=product.quantity,
                unit_price=product.unit_price
            )
            for product in obj_in.products
        ]

        self.session.add(new_order)
        try:
            self.session.commit()
            self.session.refresh(new_order)
            return new_order
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError("Erro ao criar pedido: " + str(e.orig))

    def update_order(self, id: int, obj_in: OrderUpdate) -> Optional[Order]:
        db_obj = self.get(id)
        if not db_obj:
            return None

        data = obj_in.model_dump(exclude_unset=True)
        products_data = data.pop("products", None)

        # Atualiza os campos simples (client_id, status etc.)
        for key, value in data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        if products_data is not None:
            # Remove os produtos antigos da ordem
            db_obj.products.clear()

            # Garante que db_obj.id já foi atribuído
            self.session.flush()

            # Adiciona os novos produtos
            for prod_data in products_data:
                prod_data["order_id"] = db_obj.id  # agora db_obj.id não é None
                db_obj.products.append(OrderProduct(**prod_data))

        # Comita e atualiza o objeto
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

