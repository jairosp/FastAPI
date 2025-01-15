from app.database import get_db
from fastapi import FastAPI
from .routers import post, user, auth, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# create_db_and_tables() NO LONGER NEEDED DUE TO ALEMBIC USAGE

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def root():
    return {"message": "Hello World!!!!!!!!"}
