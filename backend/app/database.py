import os
from sqlmodel import create_engine, SQLModel, Session

# Database URL can be configured via environment variable.
# Default is SQLite for local development.
db_url = os.getenv("DATABASE_URL", "sqlite:///./library.db")
engine = create_engine(db_url, echo=False)

# Create database tables from SQLModel models.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Session generator for FastAPI dependency injection.
def get_session():
    with Session(engine) as session:
        yield session
