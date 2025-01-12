from sqlmodel import SQLModel, create_engine, Session
from .config import settings


DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(DATABASE_URL)

# NO LONGER NEEDED BECAUSE OF ALEMBIC !!!
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
  
def get_db():   
    with Session(engine) as session:
        yield session
