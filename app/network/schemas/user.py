from pydantic import BaseModel, EmailStr, ConfigDict, Field
class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="strongpassword123")


class UserRead(BaseModel):
    id: int = Field(..., example=1)
    email: EmailStr = Field(..., example="user@example.com")
    is_admin: bool = Field(..., example=False)

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field("bearer", example="bearer")


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


