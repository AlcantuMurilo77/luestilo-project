from pydantic import BaseModel, EmailStr, Field

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60)
    email: EmailStr
    cpf: str = Field(..., min_length=3, max_length=14)

class ClientRead(BaseModel):
    id: int
    name: str
    email: str
    cpf: str

    class Config:
        orm_mode = True
