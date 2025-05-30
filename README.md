# Local Services Booking System

A backend API for a Local Services Booking System (e.g., electricians, plumbers, salons) built with FastAPI and PostgreSQL. Includes features for user/admin authentication, service provider management, bookings, reviews, and optional integrations like Google Maps and payment systems.

---

📌 Project Overview
The Local Services Booking System is a full-stack web application designed to streamline the booking and management of everyday services like electricians, plumbers, and salon appointments. It provides a robust platform where users can register, search for local service providers based on their location and service type, and book appointments effortlessly. Admins have separate access to manage bookings, providers, and users, making it a complete ecosystem for local service discovery and delivery.

🔐 Authentication and Authorization
The system uses token-based authentication (JWT) to ensure secure access for both regular users and admins. Users can register, log in, reset their passwords, and log out securely. Admins have a separate login and role-based access control to maintain system integrity. Token refresh and invalidation mechanisms are implemented for enhanced security, along with potential extensions like rate limiting and audit logs.

⚙️ Core Features
Key functionalities include viewing service providers, filtering them by location and service type (using Google Maps geocoding), and creating bookings with preferred providers. Users can view, update, or cancel their bookings, and also update their profile details. Admins can approve or reject bookings, manage providers, and view overall system statistics. Optional features like reviews, notifications (via email/SMS), and payment gateway integration provide a rich and extensible user experience.

🗄️ System Architecture
The backend is structured in a modular, scalable way using FastAPI (Python), and interacts with a PostgreSQL database. APIs are neatly grouped under authentication, user, provider, booking, and admin routes. Features like location-based filtering and distance-based matching use latitude/longitude values for accuracy. The system adheres to RESTful principles and supports auto-generated documentation via Swagger, ensuring easy API consumption and maintenance.

🚀 Scalability & Future Scope
This platform is designed with scalability and real-world application in mind. Advanced features like containerized deployment (Docker), asynchronous background tasks (Celery/RabbitMQ), centralized logging, and CI/CD integration make it a solid base for enterprise-level service booking solutions. In the future, the system can incorporate mobile apps, advanced analytics, real-time chat with service providers, and third-party integrations to create a seamless, end-to-end local service ecosystem.



## 📦 API Overview

### 1. Authentication & Authorization

| Endpoint                  | Method | Description                                  | Access       |
|--------------------------|--------|----------------------------------------------|--------------|
| /auth/register           | POST   | Register new user                            | Public       |
| /auth/login              | POST   | User login, get JWT                          | Public       |
| /auth/logout             | POST   | Logout user                                  | Authenticated|
| /auth/refresh            | POST   | Refresh JWT token                            | Authenticated|
| /auth/reset-password     | POST   | Start password reset                         | Public       |
| /admin/auth/login        | POST   | Admin login                                  | Public       |

### 2. User APIs

| Endpoint          | Method | Description              | Access       |
|------------------|--------|--------------------------|--------------|
| /users/me        | GET    | Get user profile         | Authenticated|
| /users/me        | PUT    | Update user profile      | Authenticated|
| /users/me        | DELETE | Delete user account      | Authenticated|

### 3. Service Provider APIs

| Endpoint                          | Method | Description                   | Access       |
|----------------------------------|--------|-------------------------------|--------------|
| /providers                       | GET    | List all providers            | Public       |
| /providers/{id}                  | GET    | Get provider details          | Public       |
| /providers/{id}/reviews          | GET    | Get provider reviews          | Public       |
| /admin/providers                 | POST   | Add service provider          | Admin only   |
| /admin/providers/{id}           | PUT    | Update provider               | Admin only   |
| /admin/providers/{id}           | DELETE | Delete provider               | Admin only   |
| /providers/{id}/reviews          | POST   | Submit review & rating        | Authenticated|

### 4. Booking APIs

| Endpoint                                  | Method | Description                       | Access       |
|------------------------------------------|--------|-----------------------------------|--------------|
| /bookings                                | POST   | Create a booking                  | Authenticated|
| /bookings                                | GET    | List user bookings                | Authenticated|
| /bookings/{id}                           | GET    | Get booking details               | Authenticated|
| /bookings/{id}                           | PUT    | Update booking                    | Authenticated|
| /bookings/{id}                           | DELETE | Cancel booking                    | Authenticated|
| /admin/bookings                          | GET    | List all bookings                 | Admin only   |
| /admin/bookings/{id}/approve            | POST   | Approve booking                   | Admin only   |
| /admin/bookings/{id}/reject             | POST   | Reject booking                    | Admin only   |

### 5. Search & Filters

| Endpoint                         | Method | Description                           |
|----------------------------------|--------|---------------------------------------|
| /search/providers                | GET    | Search providers by location/service  |
| /admin/bookings/search          | GET    | Filter bookings (admin)               |

### 6. Admin Dashboard APIs

| Endpoint               | Method | Description                  | Access     |
|------------------------|--------|------------------------------|------------|
| /admin/me              | GET    | Get admin profile            | Admin only |
| /admin/users           | GET    | List all users               | Admin only |
| /admin/users/{id}      | DELETE | Delete a user                | Admin only |
| /admin/stats           | GET    | Admin statistics             | Admin only |

### 7. Optional Features

- **Notifications API**: `/notifications/send`
- **Google Maps API Integration**:
  - Geocoding addresses to lat/lng
  - Distance-based provider filtering
- **Payment Gateway Integration** (Future)
- **Audit Logging** for tracking critical actions

---

## 🗃️ Database Models

| Table              | Description                      |
|--------------------|----------------------------------|
| users              | User info (id, name, email, etc.)|
| admins             | Admin credentials & roles        |
| service_providers  | Service provider profiles        |
| bookings           | Bookings with user/provider link |
| reviews            | User reviews for providers       |
| notifications      | Booking & system notifications   |

---

## 📌 Dev Notes

- FastAPI with PostgreSQL (Xata support optional)
- JWT Authentication with refresh tokens
- Role-based access control (RBAC)
- Geolocation using Google Maps API
- Modular project structure: `api`, `crud`, `models`, `schemas`, `utils`, `core`

---

## 🧪 Testing

- Unit tests for business logic (service layer)
- Integration tests for API endpoints

---

## 🚀 Deployment

- Deploy on: Render, Heroku, AWS, DigitalOcean
- Use `.env` for secrets and configs
- Auto-generated API docs at `/docs` or `/swagger`

---

## 📬 Contact

Project maintained by Kush Gamdha (Full Stack Developer)

---

## 🧠 Recommended Learning

| Area                   | What to Learn                                |
|------------------------|----------------------------------------------|
| Advanced Security      | OAuth2, rate limiting, encryption            |
| Scalability            | Redis, async jobs (Celery), caching          |
| DevOps & Cloud         | Docker, CI/CD, Kubernetes                    |
| Realtime               | WebSockets, push notifications               |
| Architecture           | DDD, SOLID, Clean Code, Design Patterns      |
