
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from utils.schemas.order import OrderCreate, OrderRead, OrderUpdate
from repositories.order_repository import OrderRepository
from utils.database import get_db 

router = APIRouter(prefix="/orders", tags=["order"])

@router.get("/", response_model=List[OrderRead])
def list_orders(
    category_name: Optional[str] = None,
    section_name: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
):
    repo = OrderRepository(session)
    products = repo.list(category_name, section_name, price_min, price_max, available, skip, limit)
    return products

@router.post("/", response_model=OrderRead, status_code=201)
def create_order(
    product_data: OrderCreate,
    session: Session = Depends(get_db)
):
    repo = OrderRepository(session)
    try:
        new_product = repo.create(product_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_product

@router.get("/{id}", response_model=OrderRead)
def get_order(id: int, session: Session = Depends(get_db)):
    repo = OrderRepository(session)
    product = repo.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{id}", response_model=OrderRead)
def update_order(
    id: int,
    product_data: OrderUpdate,
    session: Session = Depends(get_db)
):
    repo = OrderRepository(session)
    updated_product = repo.update(id, product_data.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_product

@router.delete("/{id}", status_code=204)
def delete_order(id: int, session: Session = Depends(get_db)):
    repo = OrderRepository(session)
    repo.delete(id)

