from fastapi.testclient import TestClient
import pytest
from app.main import app

from app.config import settings
from sqlmodel import SQLModel, create_engine, Session
from app.database import get_db 


DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

testing_engine = create_engine(DATABASE_URL)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(testing_engine)


def get_overrride_db():   
    with Session(testing_engine) as session:
        yield session

app.dependency_overrides[get_db] = get_overrride_db
 
@pytest.fixture()
def session():
    print("my session fixture run")
    SQLModel.metadata.drop_all(testing_engine)
    SQLModel.metadata.create_all(testing_engine)

    with Session(testing_engine) as session:
        yield session

@pytest.fixture()
def client(session):
    def get_overrride_db():   
        with Session(testing_engine) as session:
            yield session
            
    app.dependency_overrides[get_db] = get_overrride_db
    yield TestClient(app)