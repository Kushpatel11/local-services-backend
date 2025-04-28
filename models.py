from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(15))
    address = Column(String)
    role = Column(String(50), nullable=False)  # 'customer', 'service_provider', 'admin'
    location_coordinates = Column(String, nullable=True)  # For location-based filtering
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    bookings = relationship("Booking", back_populates="user")
    service_provider = relationship("Provider", back_populates="user", uselist=False)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    provider = relationship("Provider", back_populates="services")
    bookings = relationship("Booking", back_populates="service")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15))
    address = Column(String)
    bio = Column(String(255), nullable=True)
    rating = Column(Float, default=0.0)  # Average rating from reviews
    availability_schedule = Column(
        String, nullable=True
    )  # JSON format or string for availability (e.g., "Mon: 9-5, Tue: 10-4")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    services = relationship("Service", back_populates="provider")
    bookings = relationship("Booking", back_populates="provider")
    user = relationship("User", back_populates="service_provider", uselist=False)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    status = Column(
        String(50), nullable=False
    )  # 'pending', 'approved', 'rejected', 'completed'
    address = Column(
        String, nullable=True
    )  # Optional for user-specific address for booking
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    provider = relationship("Provider", back_populates="bookings")


class Service_Provider_Review(Base):
    __tablename__ = "service_provider_reviews"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    rating = Column(Float, nullable=False)  # 1 to 5 scale
    review = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

    booking = relationship("Booking", back_populates="reviews")
    provider = relationship("Provider")
    customer = relationship("User")


class Admin_Approval(Base):
    __tablename__ = "admin_approvals"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # 'approved', 'rejected'
    reason = Column(String(255), nullable=True)
    approved_at = Column(DateTime, nullable=False)

    booking = relationship("Booking", back_populates="admin_approval")
    admin = relationship("User")


class Payment_Record(Base):
    __tablename__ = "payment_records"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    payment_status = Column(String(50), nullable=False)  # 'pending', 'completed'
    payment_method = Column(String(50), nullable=False)  # 'credit_card', 'upi', etc.
    payment_amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    transaction_id = Column(String(100), nullable=False)

    booking = relationship("Booking")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    type = Column(
        String(50), nullable=False
    )  # 'booking_confirmation', 'booking_rejection', etc.
    status = Column(String(50), nullable=False)  # 'read', 'unread'
    created_at = Column(DateTime, nullable=False)

    user = relationship("User")


class Admin_Log(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(
        String(100), nullable=False
    )  # 'approve_booking', 'reject_booking', etc.
    action_details = Column(String(255), nullable=True)
    timestamp = Column(DateTime, nullable=False)

    admin = relationship("User")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User")


class Service_Schedule(Base):
    __tablename__ = "service_schedules"

    id = Column(Integer, primary_key=True, index=True)
    service_provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    day_of_week = Column(String(50), nullable=False)  # 'Monday', 'Tuesday', etc.
    start_time = Column(String(5), nullable=False)  # '09:00'
    end_time = Column(String(5), nullable=False)  # '17:00'

    provider = relationship("Provider")
