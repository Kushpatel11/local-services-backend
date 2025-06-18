# Local Services Backend

A backend API for a Local Services Booking System, developed with FastAPI and PostgreSQL. This project provides features for user and admin authentication, service provider management, service bookings, reviews, notifications, and advanced search/filtering.

---

## Features

### Authentication & Authorization
- Implements JWT-based authentication for both users and admins.
- Supports user registration, login, logout, password reset, and token refreshing.
- Role-Based Access Control (RBAC) with separate admin and user privileges.
- Admin authentication endpoints for administrative actions.

### User Management
- Retrieve, update, and delete user profiles.
- Admins can manage user accounts (view and delete users).

### Service Provider Management
- List all service providers.
- Retrieve detailed profiles and reviews for each provider.
- Admins can add, update, or delete service providers.
- Users can submit ratings and reviews for providers.

### Booking System
- Authenticated users can create, view, update, and cancel bookings.
- Admin endpoints to list, approve, or reject any booking.
- Bookings are linked to both users and service providers.

### Reviews & Ratings
- Users can submit and view reviews for service providers.
- Review data associated with providers for transparent feedback.

### Search & Filters
- Search service providers by location or service type.
- Admins can filter bookings using various criteria.

### Notifications
- Support for system and booking notifications (email/SMS hooks present, actual integrations depend on configuration).

### Geolocation
- Uses Google Maps API for geocoding addresses and distance-based provider searches.

### Database Models
- Models include users, admins, service_providers, bookings, reviews, and notifications.
- Designed for relational data integrity and extensibility.

### Modular Project Structure
- Organized into modules: `api`, `models`, `schemas`, `crud`, `utils`, and `core`.
- Follows scalable and maintainable Python backend architecture.

### Testing
- Unit tests for core business logic.
- Integration tests for API endpoints.
- Test suites present in dependencies for cryptography/security (e.g., passlib, greenlet).

### Security
- Secure password storage with bcrypt and passlib.
- JWT tokens for access and refresh.
- Environment-based secret management.
- Audit logging and rate limiting hooks present for future extension.

### Deployment & Configuration
- Designed for deployment on platforms like Render, Heroku, AWS, and DigitalOcean.
- Uses environment variables for configuration and secrets.
- Auto-generated interactive API documentation available at `/docs` (Swagger UI).
- Docker and containerized deployment support.

---

## Getting Started

> Note: This section assumes you are familiar with Python, FastAPI, and PostgreSQL.

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Kushpatel11/local-services-backend.git
   cd local-services-backend
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   - Copy `.env.example` to `.env` and fill in your configuration (DB credentials, JWT secret, etc).

4. **Run database migrations:**
   ```sh
   alembic upgrade head
   ```

5. **Start the server:**
   ```sh
   uvicorn main:app --reload
   ```

6. **Access API docs:**
   - Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Project Structure

```
api/
  └── ...         # API route handlers
models/
  └── ...         # Database models (SQLAlchemy)
schemas/
  └── ...         # Pydantic schemas
crud/
  └── ...         # CRUD logic
utils/
  └── ...         # Utility functions
core/
  └── ...         # Core app logic (config, security, etc)
tests/
  └── ...         # Test suites
```

---

## Technologies Used

- Python 3.x
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic (migrations)
- Passlib, bcrypt (security)
- JWT (authentication)
- Docker (deployment)
- Celery/RabbitMQ (background tasks, optional)
- Google Maps API (geolocation)

---

## License

This project uses open source libraries (see `requirements.txt` and included licenses in `venv/Lib/site-packages`). See individual package licenses for details.

---

## Maintainer

Kushpatel11

---
