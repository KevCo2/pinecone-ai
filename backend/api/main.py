from fastapi import FastAPI, Depends, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field
import re
from . import models, deps

app = FastAPI(
    title="AI E-commerce Intelligence API",
    description="API for e-commerce product intelligence and trends",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class ProductResponse(BaseModel):
    id: int
    name: str
    price: Optional[float] = None
    currency: Optional[str] = None
    
class TrendResponse(BaseModel):
    id: int
    trend_type: str
    description: str
    
class ReviewResponse(BaseModel):
    id: int
    product_id: int
    review_text: str
    rating: Optional[float] = None
    source: Optional[str] = None

# API key validation
def validate_api_key_format(api_key: str) -> bool:
    """Validate API key format (should be 32-64 characters, alphanumeric)"""
    return bool(re.match(r'^[A-Za-z0-9]{32,64}$', api_key))

def get_api_key(x_api_key: str = Header(...), db: Session = Depends(deps.get_db)):
    """Validate and retrieve API key"""
    if not validate_api_key_format(x_api_key):
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key format"
        )
    
    try:
        api_key = db.query(models.APIKey).filter_by(key=x_api_key, active=True).first()
        if not api_key:
            raise HTTPException(
                status_code=401, 
                detail="Invalid or inactive API key"
            )
        return api_key
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, 
            detail="Database error during API key validation"
        )

@app.get("/products", response_model=List[ProductResponse])
def get_products(
    q: Optional[str] = Query(None, min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    api_key: models.APIKey = Depends(get_api_key),
    db: Session = Depends(deps.get_db)
):
    """Get products with optional search query"""
    try:
        query = db.query(models.Product)
        if q:
            # Use parameterized query to prevent SQL injection
            query = query.filter(models.Product.name.ilike(f"%{q}%"))
        
        products = query.offset(offset).limit(limit).all()
        
        return [
            ProductResponse(
                id=p.id,
                name=p.name,
                price=float(p.price) if p.price else None,
                currency=p.currency
            )
            for p in products
        ]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching products"
        )

@app.get("/trends", response_model=List[TrendResponse])
def get_trends(
    trend_type: Optional[str] = Query(None, min_length=1, max_length=50),
    limit: int = Query(10, ge=1, le=100),
    api_key: models.APIKey = Depends(get_api_key),
    db: Session = Depends(deps.get_db)
):
    """Get trends with optional filtering by trend type"""
    try:
        query = db.query(models.Trend)
        if trend_type:
            query = query.filter(models.Trend.trend_type == trend_type)
        
        trends = query.limit(limit).all()
        
        return [
            TrendResponse(
                id=t.id,
                trend_type=t.trend_type,
                description=t.description
            )
            for t in trends
        ]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching trends"
        )

@app.get("/reviews", response_model=List[ReviewResponse])
def get_reviews(
    product_id: int = Query(..., ge=1),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    api_key: models.APIKey = Depends(get_api_key),
    db: Session = Depends(deps.get_db)
):
    """Get reviews for a specific product"""
    try:
        # Verify product exists
        product = db.query(models.Product).filter_by(id=product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        
        reviews = db.query(models.Review).filter_by(product_id=product_id).offset(offset).limit(limit).all()
        
        return [
            ReviewResponse(
                id=r.id,
                product_id=r.product_id,
                review_text=r.review_text,
                rating=float(r.rating) if r.rating else None,
                source=r.source
            )
            for r in reviews
        ]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching reviews"
        )

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}