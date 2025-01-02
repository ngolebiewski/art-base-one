from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import Artwork, Artist, Base 

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is Art Base One"}

# SQLite database URL (adjust the path to your db file)
DATABASE_URL = "sqlite:///../db/artbasetwo.db"  # Update the path if needed

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

# API route to fetch all artwork titles
@app.get("/artworks/titles")
def get_artwork_titles(db: Session = Depends(get_db)):
    try:
        artworks = db.query(Artwork.title).all()  # Query for artwork titles
        return {"titles": [artwork.title for artwork in artworks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
@app.get("/artists/names")
def get_artist_names(db: Session = Depends(get_db)):
    try:
        artists = db.query(Artist).all()  # Query for artist names
        return [{"first_name": artist.first_name, "last_name": artist.last_name} 
                for artist in artists
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

# Create all tables in the database
Base.metadata.create_all(bind=engine)