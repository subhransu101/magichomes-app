from sqlalchemy import Column, Integer, String, Float
from database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    city = Column(String, index=True) # Bangalore or Mumbai
    property_type = Column(String, index=True) # buy or rent
    house_type = Column(String, index=True) # flat or house
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Integer)
    image_url = Column(String)
