from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    mobile = Column(String(15), unique=True)
    role = Column(String(50), nullable=False)  # 'customer', 'service_provider', 'admin'
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
