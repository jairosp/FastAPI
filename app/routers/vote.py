from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlmodel import Session, select


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    statement = select(models.Post).filter(models.Post.id == vote.post_id)
    query = db.exec(statement)
    post = query.one_or_none()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {vote.post_id} does not exist")

    statement = select(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    query = db.exec(statement)
    found_vote = query.one_or_none()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post with an id of {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        
        return {"message": "successfully added vote"}

    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        db.delete(found_vote)
        db.commit()

        return {"message": "successfully deleted vote"}
        