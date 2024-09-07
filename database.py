import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Load the DATABASE_URL from an environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
    
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session local instance to connect to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for your models
Base = declarative_base()

# Dependency to get the database session for requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
