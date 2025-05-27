from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.middlewares.is_admin_middleware import user_access_admin_middleware
from app.network.schemas.client import ClientRead, ClientCreate
from utils.database import get_db
from repositories.client_repository import ClientRepository
from models.models import Client

router = APIRouter(prefix="/clients", tags=["client"])

@router.get("/", response_model=List[ClientRead])
def list_clients(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
):
    repo = ClientRepository(session)
    clients = repo.list(name=name, email=email, skip=skip, limit=limit)
    return clients

@router.post("/", response_model=ClientRead, status_code=201)
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

@router.get("/{id}", response_model=ClientRead)
def get_client(id: int, session: Session = Depends(get_db)):
    repo = ClientRepository(session)
    client = repo.get(id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@router.put("/{id}", response_model=ClientRead)
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

@router.delete("/{id}", status_code=204, dependencies=[Depends(user_access_admin_middleware)])
def delete_client(id: int, session: Session = Depends(get_db)):
    repo = ClientRepository(session)
    existing = repo.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    repo.delete(id)
