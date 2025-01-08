from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from models import Base # Import necessary models

# SQLite database URL (adjust the path to your db file)
DATABASE_URL = "sqlite:///../db/artbasethree.db"  # Update the path if needed

# Set up SQLAlchemy engine and session maker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example: Dependency for common exception handling
def get_or_404(query_result):
    if not query_result:
        raise HTTPException(status_code=404, detail="Resource not found")
    return query_result

# Create all tables in the database if not present
Base.metadata.create_all(bind=engine)
