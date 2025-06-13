from collections import UserDict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app import models, schema                    
from app.database import get_db                  
from app.utils import hash                       
from app import oauth2

router = APIRouter(prefix="/posts", tags=["posts"] )    

@router.get("/", response_model=list[schema.post])
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.post)
def create_posts(post: schema.postCreate, db: Session = Depends(get_db), 
get_current_user: schema.UserOut = Depends(oauth2.get_current_user)):
    new_post = models.Post(
        **post.model_dump(),
        owner_id = get_current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

@router.get("/{id}", response_model=schema.post)
def get_posts(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
         detail=f'post {id} not found')
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
         detail=f'post with id: {id} was not found') 
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.post)
def update_post(id: int, updated_post: schema.postCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
         detail=f'post with id: {id} was not found') 
    
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return post_query.first()


    


