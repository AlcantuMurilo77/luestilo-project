from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.network.schemas.product import ProductCreate, ProductRead, ProductUpdate
from utils.database import get_db 
from repositories.product_repository import ProductRepository

router = APIRouter(prefix="/products", tags=["product"])

@router.get("/", response_model=List[ProductRead])
def list_products(
    category_name: Optional[str] = None,
    section_name: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
):
    repo = ProductRepository(session)
    products = repo.list(category_name, section_name, price_min, price_max, available, skip, limit)
    return products

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(
    product_data: ProductCreate,
    session: Session = Depends(get_db)
):
    repo = ProductRepository(session)
    try:
        new_product = repo.create(product_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


    return new_product

@router.get("/{id}", response_model=ProductRead)
def get_product(id: int, session: Session = Depends(get_db)):
    repo = ProductRepository(session)
    product = repo.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.put("/{id}", response_model=ProductRead)
def update_product(
    id: int,
    product_data: ProductUpdate,
    session: Session = Depends(get_db)
):
    repo = ProductRepository(session)
    updated_product = repo.update(id, product_data.model_dump())
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_product

@router.delete("/{id}", status_code=204)
def delete_product(id: int, session: Session = Depends(get_db)):
    repo = ProductRepository(session)
    repo.delete(id)

