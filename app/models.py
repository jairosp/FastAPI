from sqlmodel import SQLModel, Field
from sqlalchemy import text
from datetime import datetime

class Post(SQLModel, table =  True):
    __tablename__ = "posts"
    id: int = Field(default=None, primary_key = True)
    title: str
    content: str
    published: bool = True
    created_at: datetime =  Field(default_factory=datetime.now  ,
                                  sa_column_kwargs={"server_default": text("NOW()")},
                                  nullable=False)

class User(SQLModel, table = True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key = True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime =  Field(default_factory=datetime.now  ,
                                  sa_column_kwargs={"server_default": text("NOW()")},
                                  nullable=False)

