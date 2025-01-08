from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import artworks, artists
from dependencies import get_db
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

# Include routers
app.include_router(artists.router, prefix="/artists", tags=["artists"])
app.include_router(artworks.router, prefix="/artworks", tags=["artworks"])

# app.include_router(mediums.router, prefix="/mediums", tags=["mediums"])
# app.include_router(users.router, prefix="/users", tags=["users"])