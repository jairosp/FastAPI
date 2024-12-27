from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import Session, select
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

@router.get("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):
    statement = select(models.User).filter(models.User.email == user_credentials.username)
    results = db.exec(statement)
    user = results.one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # Create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # Return a token
    return {
            "access_token": access_token,    
            "token_type": "bearer"
    }

    
