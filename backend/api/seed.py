import os
from backend.api.db import SessionLocal, Base, engine
from backend.api.models import User, APIKey, Product, Review, Trend
from sqlalchemy.orm import Session
import hashlib
import secrets

# Create all tables (idempotent)
Base.metadata.create_all(bind=engine)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    db: Session = SessionLocal()
    # Create test user
    user = User(email="test@example.com", password_hash=hash_password("testpass"))
    db.add(user)
    db.commit()
    db.refresh(user)
    # Create API key
    api_key_value = secrets.token_hex(32)
    api_key = APIKey(user_id=user.id, key=api_key_value, active=True)
    db.add(api_key)
    # Create sample product
    product = Product(name="Sample Product", url="https://example.com/product", price=19.99, currency="USD")
    db.add(product)
    db.commit()
    db.refresh(product)
    # Create sample review
    review = Review(product_id=product.id, review_text="Great product!", rating=5, source="example.com")
    db.add(review)
    # Create sample trend
    trend = Trend(trend_type="price_drop", description="Sample price drop trend", data={"product_id": product.id})
    db.add(trend)
    db.commit()
    print(f"Seeded test user (email: test@example.com, password: testpass)")
    print(f"API Key: {api_key_value}")

if __name__ == "__main__":
    main()