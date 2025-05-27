from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="strongpassword123")

class UserRead(BaseModel):
    id: int = Field(..., example=1)
    email: EmailStr = Field(..., example="user@example.com")
    is_admin: bool = Field(..., example=False)

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field("bearer", example="bearer")
