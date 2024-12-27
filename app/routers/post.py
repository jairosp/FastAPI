from .. import models, schemas
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    statement = select(models.Post)
    posts = db.exec(statement).all()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    statement = select(models.Post).filter(models.Post.id ==  id)
    post = db.exec(statement).one_or_none()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id = {id} does not exist")
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    statement = select(models.Post).filter(models.Post.id == id)
    results = db.exec(statement)
    post = results.one_or_none()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id = {id} does not exist")
    
    db.delete(post)
    db.commit()

    return {"message": "post was succesfully deleted"}

@router.put("/{id}")
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db)):
    # Fetch the existing post
    statement = select(models.Post).where(models.Post.id == id)
    result = db.exec(statement)
    existing_post = result.one_or_none()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} does not exist"
        )
    
    # Update the fields dynamically
    for key, value in post_data.model_dump().items():
        if hasattr(existing_post, key):
            setattr(existing_post, key, value)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field '{key}' is invalid"
            )

    # Commit the changes
    db.add(existing_post)
    db.commit()
    db.refresh(existing_post)

    return {"data": "success", "updated_post": existing_post}
