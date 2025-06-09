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
    UniqueConstraint,
)
from core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import Enum as SQLAEnum
import enum


class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


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
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    user_addresses = relationship(
        "UserAddress", back_populates="user", cascade="all, delete-orphan"
    )
    bookings = relationship("Booking", back_populates="user", cascade="all, delete")
    ratings = relationship(
        "ServiceRating", back_populates="user", cascade="all, delete"
    )
    other_details = relationship(
        "UserOtherDetails",
        back_populates="user",
        uselist=False,
        cascade="all, delete",
        foreign_keys="[UserOtherDetails.user_id]",
    )


class UserOtherDetails(Base):
    __tablename__ = "user_other_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    profile_picture_url = Column(String(255))
    preferred_language = Column(String(50))
    notification_preferences = Column(String(255))  # Could store as JSON string
    date_of_birth = Column(Date)

    user = relationship("User", back_populates="other_details")


class UserAddress(Base):
    __tablename__ = "user_address"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_line = Column(String, nullable=True)
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    pincode = Column(String(6), nullable=True)
    latitude = Column(Float, nullable=True)  # Latitude coordinate (float)
    longitude = Column(Float, nullable=True)  # Longitude coordinate (float)
    label = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="user_addresses")


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("service_categories.id"), nullable=True)

    parent = relationship("ServiceCategory", remote_side=[id], backref="subcategories")

    providers = relationship(
        "ServiceProvider", back_populates="category", cascade="all, delete"
    )
    services = relationship("Service", back_populates="category")


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
    password_hash = Column(String, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

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
    service_category_id = Column(Integer, ForeignKey("service_categories.id"))
    title = Column(String, nullable=False)  # e.g., "Fix Electrical Wiring"
    description = Column(String, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
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
    category = relationship("ServiceCategory", back_populates="services")

    @validates("min_price", "max_price")
    def validate_prices(self, key, value):
        # Only validate if both prices are set (allow creation with one or both as None)
        if key == "min_price" and self.max_price is not None and value is not None:
            if value > self.max_price:
                raise ValueError("min_price cannot be greater than max_price")
        elif key == "max_price" and self.min_price is not None and value is not None:
            if value < self.min_price:
                raise ValueError("max_price cannot be less than min_price")
        return value


class ServiceRating(Base):
    __tablename__ = "service_ratings"
    __table_args__ = (UniqueConstraint("booking_id"),)

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, unique=True)

    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    service = relationship("Service", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
    booking = relationship("Booking", back_populates="rating")

    @validates("rating")
    def validate_rating(self, key, value):
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return value


class BookingStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time, nullable=False)

    status = Column(
        SQLAEnum(BookingStatus), default=BookingStatus.pending, nullable=False
    )
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
    rating = relationship(
        "ServiceRating",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
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
