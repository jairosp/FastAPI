from sqlmodel import SQLModel, create_engine, Session
  # Import your models here

# Define the database URL
DATABASE_URL = "postgresql://postgres:kasparovsabe@localhost:5432/postgres"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Function to create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
  
def get_db():   
    with Session(engine) as session:
        yield session
