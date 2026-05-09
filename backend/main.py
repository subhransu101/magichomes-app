from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/properties", response_model=List[schemas.Property])
def get_properties(
    city: Optional[str] = None,
    property_type: Optional[str] = None,
    house_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Property)
    
    if city:
        query = query.filter(models.Property.city == city)
    if property_type:
        query = query.filter(models.Property.property_type == property_type)
    if house_type:
        query = query.filter(models.Property.house_type == house_type)
    if min_price is not None:
        query = query.filter(models.Property.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Property.price <= max_price)
        
    return query.all()

@app.get("/api/properties/{property_id}", response_model=schemas.Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@app.post("/api/properties/init_mock_data")
def init_mock_data(db: Session = Depends(get_db)):
    # Check if data already exists
    if db.query(models.Property).first():
        return {"message": "Mock data already initialized."}

    mock_properties = [
        # Bangalore Buy
        {"title": "Luxury Villa in Indiranagar", "city": "Bangalore", "property_type": "buy", "house_type": "house", "price": 45000000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 3200, "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Modern Apartment in Whitefield", "city": "Bangalore", "property_type": "buy", "house_type": "flat", "price": 12000000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1500, "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Spacious Flat in Koramangala", "city": "Bangalore", "property_type": "buy", "house_type": "flat", "price": 25000000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 2000, "image_url": "https://images.unsplash.com/photo-1502672260266-1c1de2d9d00c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Penthouse in Jayanagar", "city": "Bangalore", "property_type": "buy", "house_type": "flat", "price": 35000000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 2800, "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Cozy Studio in HSR Layout", "city": "Bangalore", "property_type": "buy", "house_type": "flat", "price": 6000000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 600, "image_url": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        # Bangalore Rent
        {"title": "2BHK in Bellandur", "city": "Bangalore", "property_type": "rent", "house_type": "flat", "price": 35000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1100, "image_url": "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "3BHK in Electronic City", "city": "Bangalore", "property_type": "rent", "house_type": "flat", "price": 45000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1600, "image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "1BHK in Marathahalli", "city": "Bangalore", "property_type": "rent", "house_type": "flat", "price": 22000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 750, "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Independent House in BTM Layout", "city": "Bangalore", "property_type": "rent", "house_type": "house", "price": 60000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 2000, "image_url": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Premium Flat in Malleshwaram", "city": "Bangalore", "property_type": "rent", "house_type": "flat", "price": 85000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 2500, "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        # Mumbai Buy
        {"title": "Sea View Apartment in Bandra", "city": "Mumbai", "property_type": "buy", "house_type": "flat", "price": 85000000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1800, "image_url": "https://images.unsplash.com/photo-1560184897-ae75f418493e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Luxury Flat in Juhu", "city": "Mumbai", "property_type": "buy", "house_type": "flat", "price": 120000000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 2500, "image_url": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "2BHK in Andheri West", "city": "Mumbai", "property_type": "buy", "house_type": "flat", "price": 25000000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1000, "image_url": "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Compact 1BHK in Goregaon", "city": "Mumbai", "property_type": "buy", "house_type": "flat", "price": 11000000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 550, "image_url": "https://images.unsplash.com/photo-1522771731478-44fb896cb007?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Spacious Duplex in Powai", "city": "Mumbai", "property_type": "buy", "house_type": "flat", "price": 55000000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 2100, "image_url": "https://images.unsplash.com/photo-1600607687931-57d56b2b4bc1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        # Mumbai Rent
        {"title": "Studio Apartment in Colaba", "city": "Mumbai", "property_type": "rent", "house_type": "flat", "price": 45000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 450, "image_url": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "2BHK in Malad West", "city": "Mumbai", "property_type": "rent", "house_type": "flat", "price": 38000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 900, "image_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "3BHK in Navi Mumbai", "city": "Mumbai", "property_type": "rent", "house_type": "flat", "price": 55000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1400, "image_url": "https://images.unsplash.com/photo-1494526585095-c41746248156?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Fully Furnished Flat in Worli", "city": "Mumbai", "property_type": "rent", "house_type": "flat", "price": 120000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1700, "image_url": "https://images.unsplash.com/photo-1502672023488-70e25813eb80?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Cozy 1BHK in Vile Parle", "city": "Mumbai", "property_type": "rent", "house_type": "flat", "price": 32000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 600, "image_url": "https://images.unsplash.com/photo-1556020685-e63193364162?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
    ]

    for p in mock_properties:
        db_prop = models.Property(**p)
        db.add(db_prop)
    
    db.commit()
    return {"message": "Mock data initialized successfully."}
