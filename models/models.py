from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey, Column, DateTime, String, Integer, func, Boolean, Float, CheckConstraint

Base = declarative_base()
metadata = Base.metadata

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    cpf = Column(String(14), nullable=False, unique=True)
    orders = relationship("Order", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}', cpf='{self.cpf}')>"

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    name = Column(String(60), nullable=False, unique=True)
    products = relationship("Product", back_populates="category")

class ProductSection(Base):
    __tablename__ = "product_sections"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    name = Column(String(60), nullable=False, unique=True)
    products = relationship("Product", back_populates="section")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)

    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("product_sections.id"), nullable=False)

    cost = Column(Float, nullable=True)
    selling_price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)

    description = Column(String(200), nullable=True)
    bar_code = Column(String(100), nullable=True, unique=True)

    initial_stock = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=True)

    images = Column(String, nullable=True)

    category = relationship("ProductCategory", back_populates="products")
    section = relationship("ProductSection", back_populates="products")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    client = relationship("Client", back_populates="orders")
    products = relationship(
        "OrderProduct",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class OrderProduct(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )

    order = relationship("Order", back_populates="products")
    product = relationship("Product")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
