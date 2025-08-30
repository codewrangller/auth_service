# Bill Station - User Authentication Service

A Django-based authentication service with JWT tokens, Redis-backed password reset, and PostgreSQL database.

## Features

- User Registration and Authentication
- JWT Token-based Authentication
- Password Reset with Redis Cache
- Rate Limiting for Security
- PostgreSQL Database
- Docker Support

## Setup Instructions

### Local Development Setup

1. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac/WSL2(Windows)
# or
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your local PostgreSQL database

4. Create a `.env` file in the settings folder (for local development) or create a `.env` file in the root directory (for docker development) with required variables (see Environment Variables section)

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

### Docker Setup

1. Make sure Docker and Docker Compose are installed

2. Create a `.env` file (see Environment Variables section)

3. Build and start the services:
```bash
docker-compose up --build
```

The application will be available at http://localhost:8000

## Environment Variables

Create a `.env` file with the following variables:

```plaintext
# Django
DEBUG=1
SECRET_KEY=your-secret-key-here
ENV=dev

# Database (Local)
DB_USER_=your_db_user
DB_PASSWORD_=your_db_password
For redis, I am using a local redis image from docker desktop to run this locally.

# Database (Docker)
POSTGRES_DB=bill_station
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis (Docker development)
REDIS_URI=redis://redis:6379/1
```

## API Endpoints

### Authentication

#### Register User
- **URL**: `/api/v1/register/`
- **Method**: POST
- **Body**:
```json
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "secure_password",
    "password2": "secure_password"
}
```

#### Login
- **URL**: `/api/v1/login/`
- **Method**: POST
- **Body**:
```json
{
    "email": "user@example.com",
    "password": "secure_password"
}
```
- **Response**: User data, JWT access and refresh tokens

### Password Reset

#### Request Reset
- **URL**: `/api/v1/password/reset/`
- **Method**: POST
- **Body**:
```json
{
    "email": "user@example.com"
}
```

#### Confirm Reset
- **URL**: `/api/v1/password/reset/confirm/`
- **Method**: POST
- **Body**:
```json
{
    "token": "received_token",
    "new_password": "new_secure_password",
    "confirm_password": "new_secure_password"
}
```

## Security Features

- Rate limiting on login and password reset endpoints
- JWT token authentication
- Redis-backed password reset tokens with expiry (10mins)
- Password validation and confirmation
- Email verification

## Development Tools

- **Testing**: `pytest` for unit tests
- **API Documentation**: Swagger UI available at `/swagger/`
- **Code Style**: Follow PEP 8 guidelines

## Deployment

[Add your deployment link here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
6. I will review and merge the PR request if approved.


