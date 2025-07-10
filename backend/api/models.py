from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP)
    api_keys = relationship('APIKey', back_populates='user')

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    key = Column(String, unique=True, nullable=False, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    user = relationship('User', back_populates='api_keys')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(Text)
    price = Column(Numeric(10,2))
    currency = Column(String(10))
    last_seen = Column(TIMESTAMP)
    reviews = relationship('Review', back_populates='product')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    review_text = Column(Text)
    rating = Column(Numeric(2,1))
    review_date = Column(TIMESTAMP)
    source = Column(String)
    product = relationship('Product', back_populates='reviews')

class Trend(Base):
    __tablename__ = 'trends'
    id = Column(Integer, primary_key=True, index=True)
    trend_type = Column(String(50))
    description = Column(Text)
    data = Column(JSON)
    created_at = Column(TIMESTAMP)