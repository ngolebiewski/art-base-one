from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from app.dependencies import get_db, get_or_404
from app.models import Artwork

router = APIRouter()

@router.get("/")
def get_all_artworks(db: Session = Depends(get_db)):
    """     Fetches all artowork rows from the 'art_list' view in the database, which adds in mediums, series, and departments as text -- rather than as an ID number.
            Returns: dict: A dictionary with a "data" key containing a list of rows as dictionaries.
    """
    try:
        result = db.execute(text("SELECT * FROM art_list")).mappings().all() 
        get_or_404(result)  
        data = [dict(row) for row in result]
        return {"data": data}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed.") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/titles")
def get_artwork_titles(db: Session = Depends(get_db)):
    artworks = db.query(Artwork.title).all()
    return {"titles": [artwork.title for artwork in artworks]}

@router.get("/{artwork_id}")
def get_artwork(artwork_id: int, db: Session = Depends(get_db)):
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    return get_or_404(artwork)
