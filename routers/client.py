from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from utils.schemas.client import ClientRead, ClientCreate
from repositories.client_repository import ClientRepository
from utils.database import get_db
from models.models import Client

router = APIRouter(prefix="/clients", tags=["client"])

@router.get(
    "/",
    response_model=List[ClientRead],
    summary="Listar clientes",
    description="Retorna uma lista paginada de clientes, filtrando por nome e email opcionais.",
    responses={
        200: {
            "description": "Lista de clientes retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "João Silva",
                            "email": "joao.silva@email.com",
                            "cpf": "12345678901"
                        }
                    ]
                }
            }
        }
    }
)
def list_clients(
    name: Optional[str] = Query(None, description="Filtro pelo nome do cliente"),
    email: Optional[str] = Query(None, description="Filtro pelo email do cliente"),
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
):
    repo = ClientRepository(session)
    clients = repo.list(name=name, email=email, skip=skip, limit=limit)
    return clients


@router.post(
    "/",
    response_model=ClientRead,
    status_code=201,
    summary="Criar cliente",
    description="Cria um novo cliente, verificando se o email e CPF não estão cadastrados.",
    responses={
        201: {
            "description": "Cliente criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Maria Oliveira",
                        "email": "maria.oliveira@email.com",
                        "cpf": "10987654321"
                    }
                }
            }
        },
        400: {
            "description": "Email ou CPF já cadastrado"
        }
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "name": "Maria Oliveira",
                        "email": "maria.oliveira@email.com",
                        "cpf": "10987654321"
                    }
                }
            }
        }
    }
)
def create_client(
    client_data: ClientCreate,
    session: Session = Depends(get_db)
):
    repo = ClientRepository(session)

    if repo.get_by_email(client_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if repo.get_by_cpf(client_data.cpf):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    client_obj = Client(**client_data.dict())
    new_client = repo.create(client_obj)
    return new_client


@router.get(
    "/{id}",
    response_model=ClientRead,
    summary="Buscar cliente por ID",
    description="Retorna o cliente com o ID informado, ou erro 404 se não encontrado.",
    responses={
        200: {
            "description": "Cliente encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "João Silva",
                        "email": "joao.silva@email.com",
                        "cpf": "12345678901"
                    }
                }
            }
        },
        404: {"description": "Cliente não encontrado"}
    }
)
def get_client(id: int, session: Session = Depends(get_db)):
    repo = ClientRepository(session)
    client = repo.get(id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.put(
    "/{id}",
    response_model=ClientRead,
    summary="Atualizar cliente",
    description="Atualiza os dados do cliente pelo ID, retorna erro 404 se não encontrado.",
    responses={
        200: {
            "description": "Cliente atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "João Silva Atualizado",
                        "email": "joao.silva@email.com",
                        "cpf": "12345678901"
                    }
                }
            }
        },
        404: {"description": "Cliente não encontrado"}
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "name": "João Silva Atualizado",
                        "email": "joao.silva@email.com",
                        "cpf": "12345678901"
                    }
                }
            }
        }
    }
)
def update_client(
    id: int,
    client_data: ClientCreate,
    session: Session = Depends(get_db)
):
    repo = ClientRepository(session)
    existing = repo.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    updated = repo.update(id, client_data)
    return updated


@router.delete(
    "/{id}",
    status_code=204,
    summary="Deletar cliente",
    description="Deleta o cliente pelo ID, retorna erro 404 se não encontrado.",
    responses={
        204: {"description": "Cliente deletado com sucesso"},
        404: {"description": "Cliente não encontrado"}
    }
)
def delete_client(id: int, session: Session = Depends(get_db)):
    repo = ClientRepository(session)
    existing = repo.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    repo.delete(id)
