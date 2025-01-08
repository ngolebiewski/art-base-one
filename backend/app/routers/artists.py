from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db, get_or_404
from models import Artist

router = APIRouter()

@router.get("/names")
def get_artist_names(db: Session = Depends(get_db)):
    """Fetch all artist names."""
    try:
        artists = db.query(Artist).all()
        return [{"first_name": artist.first_name, "last_name": artist.last_name} for artist in artists]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed.") from e

@router.get("/")
def get_all_artists(db: Session = Depends(get_db)):
    """Fetch all artist records."""
    try:
        artists = db.query(Artist).all()
        return [get_or_404(artist) for artist in artists]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed.") from e