from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    api_keys = relationship('APIKey', back_populates='user', cascade='all, delete-orphan')

class APIKey(Base):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    key = Column(String(64), unique=True, nullable=False, index=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    user = relationship('User', back_populates='api_keys')

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    url = Column(Text)
    price = Column(Numeric(10, 2))
    currency = Column(String(10))
    last_seen = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    reviews = relationship('Review', back_populates='product', cascade='all, delete-orphan')

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    review_text = Column(Text)
    rating = Column(Numeric(2, 1))
    review_date = Column(TIMESTAMP)
    source = Column(String(255))
    
    # Relationships
    product = relationship('Product', back_populates='reviews')

class Trend(Base):
    __tablename__ = 'trends'
    
    id = Column(Integer, primary_key=True, index=True)
    trend_type = Column(String(50), index=True)
    description = Column(Text)
    data = Column(JSONB)  # Using JSONB for PostgreSQL optimization
    created_at = Column(TIMESTAMP, default=func.current_timestamp())