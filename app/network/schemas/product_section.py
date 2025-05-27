from pydantic import BaseModel, Field, ConfigDict


class ProductSectionCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, example="Frozen Foods")

class ProductSectionRead(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Frozen Foods")

    model_config = ConfigDict(from_attributes=True)
