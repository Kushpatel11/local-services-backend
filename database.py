from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database


# Replace with your actual PostgreSQL URL
DATABASE_URL = (
    "postgresql+psycopg2://postgres:Kush%4097252@localhost:5432/localservicesdb"
)
database = Database(DATABASE_URL)
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

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
