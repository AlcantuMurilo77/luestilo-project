from pydantic import BaseModel, Field, ConfigDict



class ProductSecionCreate(BaseModel):
    name: str = Field(min_length=3, max_length=60)

class ProductSectionRead(BaseModel):
    id: int
    name: str

    class Config:
        model_config = ConfigDict(from_attributes=True)
