import re
from pydantic import BaseModel, EmailStr, Field, ConfigDict,field_validator

class ClientCreate(BaseModel):
    name: str = Field(min_length=3, max_length=60)
    email: EmailStr = Field(
        examples=["example@gmail.com"],
        description="The email address of the client",
    )
    cpf: str  = Field(
        examples=["00000000000"]
    )

    @field_validator('cpf')
    def validate_cpf(cls, v):
        digits = re.sub(r'\D', '', v)
        if len(digits) != 11:
            raise ValueError("cpf inválido")
        return digits 


class ClientRead(BaseModel):
    id: int
    name: str
    email: str
    cpf: str

    model_config = ConfigDict(from_attributes=True)
