import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import sys

load_dotenv()

# Environment variable validation
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set!")
    print("Please set DATABASE_URL in your .env file")
    sys.exit(1)

# Database connection with error handling
try:
    engine = create_engine(DATABASE_URL)
    # Test connection
    with engine.connect() as conn:
        pass
except Exception as e:
    print(f"ERROR: Failed to connect to database: {e}")
    print("Please check your DATABASE_URL and ensure the database is running")
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()