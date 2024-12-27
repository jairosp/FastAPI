from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import Session, select
from .. import database, schemas, models, utils


router = APIRouter(tags=["Authentication"])
def login(user_credentials: schemas.UserLogin ,db: Session = Depends(database.get_db)):
    statement = select(models.User).filter(models.User.email == user_credentials.email)
    results = db.exec(statement)
    user = results.one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Create a token

    # Return a token
    return {"token": "example token"}

    
