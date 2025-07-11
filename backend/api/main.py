from fastapi import FastAPI, Depends, HTTPException, Header
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, deps
from .db import create_tables

app = FastAPI()

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# Real API key check
def get_api_key(x_api_key: str = Header(...), db: Session = Depends(deps.get_db)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key required")
    api_key = db.query(models.APIKey).filter_by(key=x_api_key, active=True).first()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

@app.get("/products")
def get_products(q: Optional[str] = None, api_key: models.APIKey = Depends(get_api_key), db: Session = Depends(deps.get_db)):
    try:
        query = db.query(models.Product)
        if q:
            query = query.filter(models.Product.name.ilike(f"%{q}%"))
        products = query.all()
        return [{"id": p.id, "name": p.name, "price": float(p.price) if p.price else None} for p in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/trends")
def get_trends(api_key: models.APIKey = Depends(get_api_key), db: Session = Depends(deps.get_db)):
    try:
        trends = db.query(models.Trend).all()
        return [{"id": t.id, "trend_type": t.trend_type, "description": t.description} for t in trends]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/reviews")
def get_reviews(product_id: int, api_key: models.APIKey = Depends(get_api_key), db: Session = Depends(deps.get_db)):
    try:
        # Check if product exists
        product = db.query(models.Product).filter_by(id=product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        reviews = db.query(models.Review).filter_by(product_id=product_id).all()
        return [{"id": r.id, "product_id": r.product_id, "review_text": r.review_text, "rating": float(r.rating) if r.rating else None} for r in reviews]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")