from fastapi import FastAPI, Depends, HTTPException, Header
from typing import List, Optional

app = FastAPI()

# Dummy API key check
def get_api_key(x_api_key: str = Header(...)):
    # Replace with real DB/API key check
    if x_api_key != "test-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/products")
def get_products(q: Optional[str] = None, api_key: str = Depends(get_api_key)):
    # Replace with DB query
    return [{"id": 1, "name": "Sample Product", "price": 19.99}]

@app.get("/trends")
def get_trends(api_key: str = Depends(get_api_key)):
    # Replace with DB query
    return [{"id": 1, "trend_type": "price_drop", "description": "Biggest price drops this week"}]

@app.get("/reviews")
def get_reviews(product_id: int, api_key: str = Depends(get_api_key)):
    # Replace with DB query
    return [{"id": 1, "product_id": product_id, "review_text": "Great!", "rating": 5}]