# FastAPI Authentication System

A robust authentication system built with FastAPI, featuring JWT-based authentication, email verification, and comprehensive test coverage.

## Features

- 🔐 Secure user authentication with JWT tokens
- 📧 Email verification system
- 🔄 Access and refresh token flow
- 🛡️ Protected routes with role-based access
- 🔒 Secure password handling
- 📝 Comprehensive test suite
- 🚀 FastAPI with async support
- 🗄️ SQLAlchemy ORM with async support
- 📊 Pydantic v2 for data validation

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **Pytest** - Testing framework
- **FastAPI-Mail** - Email functionality
- **Python-jose** - JWT token handling
- **Passlib** - Password hashing
- **Python-multipart** - Form data handling
- **MySQL** - Database (with mysql-connector-python)

## Prerequisites

- Python 3.8+
- MySQL Server
- SMTP server for email verification

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-auth-app.git
cd fastapi-auth-app
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
# JWT Settings
JWT_SECRET=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (MySQL)
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/database_name

# Email Settings
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=your-email@gmail.com
EMAILS_FROM_NAME=Your Name
```

5. Create the MySQL database:
```sql
CREATE DATABASE fastapi_auth;
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access/refresh tokens
- `POST /auth/verify-email` - Verify email with code
- `POST /auth/resend-verification` - Resend verification code
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout and invalidate refresh token

### Protected Routes
- `GET /user/home` - Protected home endpoint
- `GET /user/me` - Get current user info

## Running Tests

Run all tests:
```bash
python scripts/run_tests.py
```

Run tests with coverage:
```bash
python scripts/run_tests.py -c
```

Run specific test file:
```bash
python scripts/run_tests.py -p tests/test_login.py
```

## Project Structure

```
fastapi-auth-app/
├── app/
│   ├── core/            # Core functionality
│   ├── dependencies/    # FastAPI dependencies
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # API routes
│   ├── schemas/        # Pydantic models
│   └── main.py         # Application entry point
├── scripts/            # Utility scripts
├── tests/              # Test suite
├── .env               # Environment variables
├── pytest.ini         # Pytest configuration
└── requirements.txt   # Project dependencies
```

## Security Features

### Implemented
- Password hashing with bcrypt
- JWT token-based authentication
- Refresh token rotation
- Email verification
- Secure password requirements
- Input validation with Pydantic
- HTTP-only cookies for refresh tokens
- SameSite cookie policy
- Token expiration and validation

### Planned Features
- Rate limiting (to prevent brute force attacks)
- CORS protection (to restrict cross-origin requests)


## Acknowledgments

- FastAPI documentation and community
- SQLAlchemy documentation
- Pydantic documentation