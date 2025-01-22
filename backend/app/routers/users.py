from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token  # Assuming this is the utility function you wrote earlier

router = APIRouter()

# User registration route
@router.post("/register")
def register_user(username: str, password: str, email: str, db: Session = Depends(get_db)):
    # Check if the username already exists
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before saving to the database
    hashed_password = hash_password(password)
    
    # Create a new user instance
    new_user = User(username=username, password=hashed_password, email=email)
    
    # Add the user to the database and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create JWT for the newly registered user
    user_data = {"username": new_user.username, "email": new_user.email, "is_admin": new_user.admin}
    access_token = create_access_token(data=user_data)

    return {
        "message": "User created successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"username": new_user.username, "email": new_user.email, "admin": new_user.admin}
    }

# Example login route
@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    # Retrieve the user by username
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the password
    if not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Create JWT with user info and admin status
    user_data = {"username": db_user.username, "email": db_user.email, "admin": db_user.admin}
    access_token = create_access_token(data=user_data)
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"username": db_user.username, "email": db_user.email, "is_admin": db_user.admin}
    }
