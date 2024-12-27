from fastapi import FastAPI, status, HTTPException, Depends
from typing import Dict, Optional, List
import app.utils as utils

from sqlmodel import SQLModel, select, Session
from app.models import Post
from app.database import engine, create_db_and_tables, get_db
from app.models import Post, User
import app.schemas as schemas
from .routers import post, user, auth

create_db_and_tables()

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {"message": "Hello World"}
