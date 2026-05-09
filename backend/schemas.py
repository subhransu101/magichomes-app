from pydantic import BaseModel
from typing import Optional

class PropertyBase(BaseModel):
    title: str
    city: str
    property_type: str
    house_type: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: int
    image_url: str

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int

    class Config:
        orm_mode = True
