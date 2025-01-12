from .. import models, schemas, oauth2
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select, func
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

# DEBUG THIS
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
# @router.get("/", status_code=status.HTTP_200_OK)
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = ""
):
    statement = select(models.Post, func.count(models.Vote.post_id).label("votes"))\
                        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
                        .group_by(models.Post.id)\
                        .filter(models.Post.title.contains(search))\
                        .limit(limit)\
                        .offset(skip)
    
    results = db.exec(statement).all()

    for idx, row in enumerate(results):
        post, votes = row

        userout = schemas.UserOut(**post.owner.model_dump())
        new_post = schemas.Post(**post.model_dump(), owner=userout)
        post_out = schemas.PostOut(post = new_post, votes = votes)

        results[idx] = post_out
    # results = list(map(lambda x : x._mapping, results)) # This is line is given by a Youtube comment to fix this issue
    return results


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    statement = select(models.Post).filter(models.Post.id ==  id)
    post = db.exec(statement).one_or_none()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} does not exist")
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    statement = select(models.Post).filter(models.Post.id == id)
    results = db.exec(statement)
    post = results.one_or_none()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id = {id} does not exist")
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()

    return {"message": "post was succesfully deleted"}

@router.put("/{id}")
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Fetch the existing post
    statement = select(models.Post).where(models.Post.id == id)
    result = db.exec(statement)
    existing_post = result.one_or_none()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} does not exist"
        )
    if current_user.id != existing_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
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
