from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.network.schemas.product import ProductCreate, ProductRead, ProductUpdate
from utils.database import get_db 
from repositories.product_repository import ProductRepository

router = APIRouter(prefix="/products", tags=["product"])

@router.get(
    "/",
    response_model=List[ProductRead],
    summary="Listar produtos",
    description="Retorna uma lista paginada de produtos, com filtros opcionais por categoria, seção, preço e disponibilidade.",
    responses={
        200: {
            "description": "Lista de produtos retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Arroz",
                            "category_id": 2,
                            "section_id": 1,
                            "selling_price": 10.50,
                            "initial_stock": 100,
                            "cost": 7.00,
                            "availability": True,
                            "description": "Arroz branco tipo 1",
                            "bar_code": "1234567890123",
                            "expiration_date": "2025-12-31T00:00:00Z",
                            "images": None
                        }
                    ]
                }
            }
        }
    }
)
def list_products(
    category_name: Optional[str] = Query(None, description="Filtro por nome da categoria"),
    section_name: Optional[str] = Query(None, description="Filtro por nome da seção"),
    price_min: Optional[float] = Query(None, description="Preço mínimo"),
    price_max: Optional[float] = Query(None, description="Preço máximo"),
    available: Optional[bool] = Query(None, description="Filtra apenas produtos disponíveis"),
    skip: int = Query(0, ge=0, description="Quantidade de itens a pular"),
    limit: int = Query(10, gt=0, le=100, description="Limite de itens a retornar"),
    session: Session = Depends(get_db)
):
    repo = ProductRepository(session)
    products = repo.list(category_name, section_name, price_min, price_max, available, skip, limit)
    return products

@router.post(
    "/",
    response_model=ProductRead,
    status_code=201,
    summary="Criar produto",
    description="Cria um novo produto com as informações fornecidas.",
    responses={
        201: {
            "description": "Produto criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Arroz",
                        "category_id": 2,
                        "section_id": 1,
                        "selling_price": 10.50,
                        "initial_stock": 100,
                        "cost": 7.00,
                        "availability": True,
                        "description": "Arroz branco tipo 1",
                        "bar_code": "1234567890123",
                        "expiration_date": "2025-12-31T00:00:00Z",
                        "images": None
                    }
                }
            }
        },
        400: {
            "description": "Dados inválidos ou erro na criação do produto"
        }
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "name": "Arroz",
                        "category_id": 2,
                        "section_id": 1,
                        "selling_price": 10.50,
                        "initial_stock": 100,
                        "cost": 7.00,
                        "availability": True,
                        "description": "Arroz branco tipo 1",
                        "bar_code": "1234567890123",
                        "expiration_date": "2025-12-31T00:00:00Z",
                        "images": None
                    }
                }
            }
        }
    }
)
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

@router.get(
    "/{id}",
    response_model=ProductRead,
    summary="Buscar produto por ID",
    description="Retorna o produto com o ID especificado.",
    responses={
        200: {
            "description": "Produto encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Arroz",
                        "category_id": 2,
                        "section_id": 1,
                        "selling_price": 10.50,
                        "initial_stock": 100,
                        "cost": 7.00,
                        "availability": True,
                        "description": "Arroz branco tipo 1",
                        "bar_code": "1234567890123",
                        "expiration_date": "2025-12-31T00:00:00Z",
                        "images": None
                    }
                }
            }
        },
        404: {"description": "Produto não encontrado"}
    }
)
def get_product(id: int, session: Session = Depends(get_db)):
    repo = ProductRepository(session)
    product = repo.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put(
    "/{id}",
    response_model=ProductRead,
    summary="Atualizar produto",
    description="Atualiza o produto com o ID especificado.",
    responses={
        200: {
            "description": "Produto atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Arroz integral",
                        "category_id": 2,
                        "section_id": 1,
                        "selling_price": 12.00,
                        "initial_stock": 90,
                        "cost": 8.00,
                        "availability": True,
                        "description": "Arroz integral tipo 1",
                        "bar_code": "1234567890123",
                        "expiration_date": "2026-01-31T00:00:00Z",
                        "images": None
                    }
                }
            }
        },
        404: {"description": "Produto não encontrado"}
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "name": "Arroz integral",
                        "category_id": 2,
                        "section_id": 1,
                        "selling_price": 12.00,
                        "initial_stock": 90,
                        "cost": 8.00,
                        "availability": True,
                        "description": "Arroz integral tipo 1",
                        "bar_code": "1234567890123",
                        "expiration_date": "2026-01-31T00:00:00Z",
                        "images": None
                    }
                }
            }
        }
    }
)
def update_product(
    id: int,
    product_data: ProductUpdate,
    session: Session = Depends(get_db)
):
    repo = ProductRepository(session)
    updated_product = repo.update(id, product_data.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_product

@router.delete(
    "/{id}",
    status_code=204,
    summary="Deletar produto",
    description="Deleta o produto com o ID especificado.",
    responses={
        204: {"description": "Produto deletado com sucesso"},
        404: {"description": "Produto não encontrado"}
    }
)
def delete_product(id: int, session: Session = Depends(get_db)):
    repo = ProductRepository(session)
    existing = repo.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    repo.delete(id)
