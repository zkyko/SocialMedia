from fastapi import HTTPException, status, Response, APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.utils import hash
from app import oauth2
from app.schema import UserCreate, UserOut


router = APIRouter(prefix="/user", tags=["users"])



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username = user.username,
        email = user.email,
        password = hash(user.password)  
    )       
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
         detail=f'user with id: {id} was not found')
    return user
            


