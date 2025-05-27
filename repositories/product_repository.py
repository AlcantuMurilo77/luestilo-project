from sqlalchemy.orm import Session, joinedload 
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from models.models import Product, ProductCategory, ProductSection  # Ajuste conforme seu modelo de produto
from app.network.schemas.product import ProductCreate
from repositories.base import BaseRepository

class ProductRepository(BaseRepository[Product]):
    
    def __init__(self, session: Session):
        super().__init__(Product, session)

    def list(
        self,
        category_name: Optional[str] = None,
        section_name: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Product]:
        query = self.session.query(self.model)

        if category_name:
            query = query.join(ProductCategory).filter(ProductCategory.name.ilike(f"%{category_name}%"))
        if section_name:
            query = query.join(ProductSection).filter(ProductSection.name.ilike(f"%{section_name}%"))
        if price_min is not None:
            query = query.filter(self.model.selling_price >= price_min)
        if price_max is not None:
            query = query.filter(self.model.selling_price <= price_max)
        if available is not None:
            query = query.filter(self.model.availability == available)

        query = query

        return query.offset(skip).limit(limit).all()

    def get(self, id: int) -> Optional[Product]:
        return self.session.query(Product).options(
                joinedload(Product.category).joinedload(ProductCategory.products),
                joinedload(Product.section).joinedload(ProductSection.products),
        ).filter(Product.id == id).first()


    def create(self, obj_in: ProductCreate) -> Product:
        category = self.session.query(ProductCategory).filter(ProductCategory.id == obj_in.category_id).first()
        section = self.session.query(ProductSection).filter(ProductSection.id == obj_in.section_id).first()

        if not category or not section:
            raise ValueError("Categoria ou Seção não encontrados")

        new_product = Product(
            name=obj_in.name,
            category_id=category.id,
            section_id=section.id,
            cost=obj_in.cost,
            selling_price=obj_in.selling_price,
            availability=obj_in.availability,
            description=obj_in.description,
            bar_code=obj_in.bar_code,
            initial_stock=obj_in.initial_stock,
            expiration_date=obj_in.expiration_date,
            images=obj_in.images
        )

        self.session.add(new_product)

        try:
            self.session.commit()
            self.session.refresh(new_product)
            return new_product
        except IntegrityError as e:
            self.session.rollback()
            # Aqui você pode personalizar a mensagem ou re-levantar uma exceção específica
            raise ValueError(f"Erro ao criar produto: {str(e.orig)}")

    def update(self, id: int, obj_in: dict) -> Optional[Product]:
        db_obj = self.get(id)
        if not db_obj:
            return None

        # Se necessário, manipule a categoria e seção para atualizações também
        if "category_name" in obj_in:
            category = self.session.query(ProductCategory).filter(ProductCategory.name == obj_in["category_name"]).first()
            if category:
                db_obj.category_id = category.id

        if "section_name" in obj_in:
            section = self.session.query(ProductSection).filter(ProductSection.name == obj_in["section_name"]).first()
            if section:
                db_obj.section_id = section.id

        for key, value in obj_in.items():
            setattr(db_obj, key, value)

        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

