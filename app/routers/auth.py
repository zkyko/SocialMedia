from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schema                      
from app.database import get_db                    
from app.utils import verify                         
from app import oauth2 
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user_in: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_in.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid Credentials")
    
    if not verify(user_in.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})    
    return {"access_token": access_token, "token_type": "bearer"}
