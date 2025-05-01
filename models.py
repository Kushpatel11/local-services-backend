from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Boolean,
    Date,
    Time,
)
from core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    mobile = Column(String(15), unique=True, index=True)
    role = Column(String(50), nullable=False)  # 'customer', 'service_provider', 'admin'
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user_addresses = relationship(
        "UserAddress", back_populates="user", cascade="all, delete"
    )
    bookings = relationship("Booking", back_populates="user", cascade="all, delete")
    ratings = relationship(
        "ServiceRating", back_populates="user", cascade="all, delete"
    )


class UserAddress(Base):
    __tablename__ = "user_address"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    pincode = Column(String(6), nullable=False)
    latitude = Column(Float, nullable=False)  # Latitude coordinate (float)
    longitude = Column(Float, nullable=False)  # Longitude coordinate (float)
    label = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="user_addresses")


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)

    providers = relationship(
        "ServiceProvider", back_populates="category", cascade="all, delete"
    )


class ServiceProvider(Base):
    __tablename__ = "service_providers"

    id = Column(Integer, primary_key=True, index=True)
    service_category_id = Column(
        Integer, ForeignKey("service_categories.id"), nullable=False
    )
    experience_years = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    mobile = Column(String(15), nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    addresses = relationship(
        "ProviderAddress", back_populates="provider", cascade="all, delete"
    )
    services = relationship("Service", back_populates="provider", cascade="all, delete")
    category = relationship("ServiceCategory", back_populates="providers")


class ProviderAddress(Base):
    __tablename__ = "provider_addresses"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("service_providers.id"), nullable=False)

    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    pincode = Column(String(6), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    label = Column(String, nullable=True)  # e.g., "Workshop", "Head Office"

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    provider = relationship("ServiceProvider", back_populates="addresses")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("service_providers.id"), nullable=False)

    title = Column(String, nullable=False)  # e.g., "Fix Electrical Wiring"
    description = Column(String, nullable=True)
    price_range = Column(
        String, nullable=False
    )  # Or define min_price/max_price if needed

    available = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    bookings = relationship("Booking", back_populates="service", cascade="all, delete")
    ratings = relationship(
        "ServiceRating", back_populates="service", cascade="all, delete"
    )
    provider = relationship("ServiceProvider", back_populates="services")


class ServiceRating(Base):
    __tablename__ = "service_ratings"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    service = relationship("Service", back_populates="ratings")
    user = relationship("User", back_populates="ratings")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time, nullable=False)

    status = Column(String, default="pending", nullable=False)
    # Choices: 'pending', 'approved', 'rejected', 'completed', 'cancelled'

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    booking_address = relationship(
        "BookingAddress", back_populates="booking", uselist=False, cascade="all, delete"
    )


class BookingAddress(Base):
    __tablename__ = "booking_address"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)

    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    pincode = Column(String(6), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    label = Column(String, nullable=True)

    booking = relationship("Booking", back_populates="booking_address")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
