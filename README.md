# Local Services Backend

A backend API for a Local Services Booking System, developed with FastAPI and PostgreSQL. This project provides features for user and admin authentication, service provider management, service bookings, reviews, notifications, advanced search/filtering, and robust payment and provider wallet handling.

---

## Features

### Authentication & Authorization
- JWT-based authentication for both users and admins.
- User registration, login, logout, password reset, and token refreshing.
- Role-Based Access Control (RBAC) with separate admin and user privileges.

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

### Search & Filters
- Search service providers by location or service type.
- Admins can filter bookings using various criteria.

### Notifications
- (Stub/extendable) Support for system and booking notifications.

---

## Payment & Wallet System

### Payment
- **Integrated with Razorpay** for secure, real-world payment processing.
- Payment model tracks status (`created`, `succeeded`, `failed`), amount, currency, and related booking.
- Endpoints for initiating payments, marking as successful, logging payments, and processing refunds.
- Payment verification and webhook handling via Razorpay.

### Provider Wallet
- Each service provider has a wallet account, automatically tracked and updated.
- Wallet tracks real-time balance, all earnings, withdrawals, and refunds as transactions.
- Automatic commission deduction and credit to provider wallet after successful bookings.
- Minimum withdrawal amount and balance checks enforced.

### Withdrawals
- Providers can request withdrawals to UPI.
- Withdrawal requests are tracked with statuses (`requested`, `approved`, `rejected`, `processed`, `failed`).
- Admins can approve/reject withdrawal requests.
- All wallet activity is transparently logged.

---

## Project Structure

```
api/
  └── ...         # API route handlers
models.py         # Database models (SQLAlchemy)
schemas/          # Pydantic schemas
crud/             # CRUD logic
routes/           # API route modules
utils/            # Utility functions (e.g., Razorpay client)
core/             # Core app logic (config, security, db)
alembic/          # Database migrations
tests/            # Test suites
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
- Razorpay (payment gateway)

---

## API Highlights

- **/payment/initiate:** Start a new payment for a booking.
- **/payment/booking/{booking_id}/payment_logs:** View all payment attempts for a booking.
- **/payment/complete_booking_and_credit_wallet:** Mark a booking as complete and automatically credit provider’s wallet.
- **/payment/refund:** Process refunds for bookings.
- **/wallet:** Provider wallet details and balance.
- **/transactions:** List all wallet transactions for a provider.
- **/withdraw:** Request withdrawal from provider wallet.

---

## Database Models

| Table                | Description                                    |
|----------------------|------------------------------------------------|
| users                | User info (id, name, email, etc.)              |
| admins               | Admin credentials & roles                      |
| service_providers    | Service provider profiles                      |
| bookings             | Bookings with user/provider link               |
| reviews              | User reviews for providers                     |
| provider_wallets     | Wallet per provider                            |
| wallet_transactions  | All wallet transactions (earnings, withdrawals, refunds) |
| withdrawal_requests  | Withdrawal requests by providers               |
| payments             | Payment records (linked to bookings & Razorpay)|

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
   - Copy `.env.example` to `.env` and fill in your configuration (DB credentials, JWT secret, Razorpay keys, etc).

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

## License

This project uses open source libraries (see `requirements.txt` and included licenses). See individual package licenses for details.

---

## Maintainer

Kushpatel11

---

## 🚀 Future Scope & Planned Features

- Mobile app support for users and providers
- Real-time chat and push notifications
- Advanced analytics and dashboards for admins/providers
- Multi-language and localization support
- Integration with additional payment gateways
- Loyalty, referral, and rewards systems
- Service scheduling and calendar sync
- Automated invoicing and tax compliance
- Caching and CDN for performance
- Containerization and Kubernetes orchestration
- Asynchronous task processing (Celery/RQ)
- API rate limiting and advanced security
- Centralized logging, monitoring, and alerting
- Blue/green and canary deployments
- Horizontal scaling and zero-downtime migrations
