from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import text
from datetime import datetime
from typing import List, Optional



class User(SQLModel, table = True):
    __tablename__ = "users"
    id: int = Field(nullable=False, primary_key = True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime =  Field(default_factory=None  ,
                                  sa_column_kwargs={"server_default": text("NOW()")},
                                  nullable=False)

class Post(SQLModel, table =  True):
    __tablename__ = "posts"
    id: int = Field(default=None, primary_key = True)
    title: str
    content: str
    published: bool = True
    created_at: datetime =  Field(default_factory=datetime.now  ,
                                  sa_column_kwargs={"server_default": text("NOW()")},
                                  nullable=False)
    owner_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")

    owner: Optional[User] = Relationship()

class Vote(SQLModel, table = True):
    __tablename__ = "votes"
    user_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE", primary_key= True)
    post_id: int = Field(foreign_key="posts.id", nullable=False, ondelete="CASCADE", primary_key= True)



    

