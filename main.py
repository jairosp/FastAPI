from fastapi import FastAPI, status, HTTPException, Depends
from typing import Dict, Optional, List
import utils

from sqlmodel import SQLModel, select, Session
from models import Post
from database import engine, create_db_and_tables, get_db
from models import Post, User
import schemas

create_db_and_tables()

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    statement = select(Post)
    posts = db.exec(statement).all()
    return posts

@app.post("/createposts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    statement = select(Post).filter(Post.id ==  id)
    post = db.exec(statement).one()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id = {id} does not exist")
    return post

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    statement = select(Post).filter(Post.id == id)
    results = db.exec(statement)
    post = results.one()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id = {id} does not exist")
    
    db.delete(post)
    db.commit()

    return {"message": "post was succesfully deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db)):
    # Fetch the existing post
    statement = select(Post).where(Post.id == id)
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

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    statement = select(User).filter(User.id == id)
    results = db.exec(statement)
    user = results.one()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"User with id = {id} does not exist")
    

    return user