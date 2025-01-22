from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from app.dependencies import get_db, get_or_404
from app.models import Artwork, Artist
from datetime import datetime

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

@router.post("/")
def add_artwork(
    artist_id: int,
    title: str,
    size: str,
    year: int,
    end_year: int | None, # Nullable field
    image_url: str,
    hi_res_url: str = None,  # Nullable field
    description: str = None,  # Nullable field
    keywords: str = None,  # Nullable field
    department: int = None,  # Foreign key field that can be nullable
    series: int = None,  # Foreign key field that can be nullable
    price: float = None,  # Nullable decimal field
    sold: int = 0,  # Default value for sold (not sold by default)
    db: Session = Depends(get_db)
):
    """Add artwork to db"""
    # Check if artist exists (assuming there is an artist model or table)
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Create a new artwork instance
    new_artwork = Artwork(
        artist_id=artist_id,
        title=title,
        size=size,
        year=year,
        end_year=end_year,
        image_url=image_url,
        hi_res_url=hi_res_url,
        description=description,
        keywords=keywords,
        department=department,
        series=series,
        date_added=datetime.utcnow(),
        price=price,
        sold=sold
    )

    # Add the artwork to the database and commit
    db.add(new_artwork)
    db.commit()
    db.refresh(new_artwork)

    return {"message": "Artwork added successfully", "artwork": new_artwork}
