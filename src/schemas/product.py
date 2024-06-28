from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str
    name: str
    description: str
    pricing: dict
    availability: dict
    category: str
    pricing: dict = Field(..., json_schema_extra={"example": {"amount": 100.0, "currency": "BRL"}})
    availability: dict = Field(..., json_schema_extra={"example": {"quantity": 50, "timestamp": "2024-06-12T12:00:00Z"}})