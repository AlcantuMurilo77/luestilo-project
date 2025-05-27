from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.network.schemas.order import OrderCreate, OrderRead, OrderUpdate
from repositories.order_repository import OrderRepository
from utils.database import get_db 

router = APIRouter(prefix="/orders", tags=["order"])

@router.get(
    "/",
    response_model=List[OrderRead],
    summary="Listar pedidos",
    description="Retorna lista paginada de pedidos com filtros opcionais.",
    responses={
        200: {
            "description": "Pedidos retornados com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "client_id": 123,
                            "status": "pending",
                            "created_at": "2025-05-26T15:30:00Z",
                            "updated_at": "2025-05-26T15:30:00Z"
                        }
                    ]
                }
            }
        }
    }
)
def list_orders(
    category_name: Optional[str] = Query(None, description="Filtro por categoria"),
    section_name: Optional[str] = Query(None, description="Filtro por seção"),
    price_min: Optional[float] = Query(None, description="Preço mínimo"),
    price_max: Optional[float] = Query(None, description="Preço máximo"),
    available: Optional[bool] = Query(None, description="Disponibilidade"),
    skip: int = Query(0, ge=0, description="Número de itens a pular"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de itens a retornar"),
    session: Session = Depends(get_db)
):
    repo = OrderRepository(session)
    orders = repo.list(category_name, section_name, price_min, price_max, available, skip, limit)
    return orders

@router.post(
    "/",
    response_model=OrderRead,
    status_code=201,
    summary="Criar pedido",
    description="Cria um novo pedido com os produtos indicados.",
    responses={
        201: {
            "description": "Pedido criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "client_id": 123,
                        "status": "pending",
                        "created_at": "2025-05-26T15:30:00Z",
                        "updated_at": "2025-05-26T15:30:00Z"
                    }
                }
            }
        },
        400: {"description": "Dados inválidos para criação do pedido"}
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "client_id": 123,
                        "status": "pending",
                        "products": [
                            {
                                "product_id": 456,
                                "quantity": 2,
                                "unit_price": 25.5
                            }
                        ]
                    }
                }
            }
        }
    }
)
def create_order(
    product_data: OrderCreate,
    session: Session = Depends(get_db)
):
    repo = OrderRepository(session)
    try:
        new_order = repo.create(product_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_order

@router.get(
    "/{id}",
    response_model=OrderRead,
    summary="Buscar pedido por ID",
    description="Retorna os detalhes do pedido identificado pelo ID.",
    responses={
        200: {
            "description": "Pedido encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "client_id": 123,
                        "status": "pending",
                        "created_at": "2025-05-26T15:30:00Z",
                        "updated_at": "2025-05-26T15:30:00Z"
                    }
                }
            }
        },
        404: {"description": "Pedido não encontrado"}
    }
)
def get_order(id: int, session: Session = Depends(get_db)):
    repo = OrderRepository(session)
    order = repo.get(id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.put(
    "/{id}",
    response_model=OrderRead,
    summary="Atualizar pedido",
    description="Atualiza os dados do pedido identificado pelo ID.",
    responses={
        200: {
            "description": "Pedido atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "client_id": 123,
                        "status": "completed",
                        "created_at": "2025-05-26T15:30:00Z",
                        "updated_at": "2025-05-27T09:15:00Z"
                    }
                }
            }
        },
        404: {"description": "Pedido não encontrado"}
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "client_id": 123,
                        "status": "completed",
                        "products": [
                            {
                                "product_id": 456,
                                "quantity": 2,
                                "unit_price": 25.5
                            }
                        ]
                    }
                }
            }
        }
    }
)
def update_order(
    id: int,
    product_data: OrderUpdate,
    session: Session = Depends(get_db)
):
    repo = OrderRepository(session)
    updated_order = repo.update(id, product_data.dict(exclude_unset=True))
    if not updated_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return updated_order

@router.delete(
    "/{id}",
    status_code=204,
    summary="Deletar pedido",
    description="Deleta o pedido identificado pelo ID.",
    responses={
        204: {"description": "Pedido deletado com sucesso"},
        404: {"description": "Pedido não encontrado"}
    }
)
def delete_order(id: int, session: Session = Depends(get_db)):
    repo = OrderRepository(session)
    existing = repo.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    repo.delete(id)
