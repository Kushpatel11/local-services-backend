from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from core.config import settings

# Replace with your actual PostgreSQL URL

database = Database(settings.DATABASE_URL)
# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a session to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
