from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import Artwork, Artist, Base 

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "This is Art Base One"}

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

from sqlalchemy.exc import SQLAlchemyError

# returns all artists
@app.get("/artists")
def get_artist_names(db: Session = Depends(get_db)):
    """ Returns data from all artists"""
    try:
        artists = db.query(Artist).all()  # Query for artist names
        return [artist for artist in artists
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

from sqlalchemy.exc import SQLAlchemyError

# @app.get("/artworks/all")
# def get_all_artworks(db: Session = Depends(get_db)):
#     """
#     Fetches all rows from the 'art_list' view in the database.

#     Args:
#         db (Session): The database session dependency.

#     Returns:
#         dict: A dictionary with a "data" key containing a list of rows as dictionaries.
#     """
#     try:
#         # Query the 'art_list' view
#         result = db.execute(text("SELECT * FROM art_list"))
#         rows = result.mappings().all()

#         # Convert the rows to a list of dictionaries for JSON serialization
#         data = [dict(row) for row in rows]

#         return {"data": data}
#     except SQLAlchemyError as e:
#         # Log or print error details for debugging
#         raise HTTPException(status_code=500, detail="Database query failed.") from e
#     except Exception as e:
#         # Catch any other unexpected errors
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# @app.get("/artworks/{artwork_id}")
# async def read_artwork(artwork_id: int, db: Session = Depends(get_db)):
#     try:
#         result = db.execute(text("SELECT * FROM art_list WHERE id = :artwork_id"), {"artwork_id": artwork_id})
#         rows = result.mappings().all()

#         if not rows:
#             raise HTTPException(status_code=404, detail="Artwork not found.")

#         # Convert the rows to a list of dictionaries for JSON serialization
#         data = [dict(row) for row in rows]

#         return {"artwork": data}
#     except SQLAlchemyError as e:
#         # Log or print error details for debugging
#         raise HTTPException(status_code=500, detail="Database query failed.") from e
#     except Exception as e:
#         # Catch any other unexpected errors
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
# Create all tables in the database
Base.metadata.create_all(bind=engine)
