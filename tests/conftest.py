from fastapi.testclient import TestClient
import pytest
from app.main import app

from app.config import settings
from sqlmodel import SQLModel, create_engine, Session
from app.database import get_db 
from app.oauth2 import create_access_token
from app import models


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

@pytest.fixture
def test_user(client):
    user_data = {"email": "he@email.com", "password": "password123"}
    res = client.post(
        "/users/", json=user_data)
    
    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello@email.com", "password": "password123"}
    res = client.post(
        "/users/", json=user_data)
    
    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
    {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, 
    {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "title": "3rd party post",
        "content": "Some content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
