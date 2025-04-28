from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual PostgreSQL URL
DATABASE_URL = (
    "postgresql+psycopg2://postgres:Kush%4097252@localhost:5432/localservicesdb"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
