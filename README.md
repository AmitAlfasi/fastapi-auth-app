# FastAPI Authentication System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

A robust authentication system built with FastAPI, featuring JWT-based authentication, email verification, and comprehensive test coverage.

---

## 📚 Table of Contents

- [FastAPI Authentication System](#fastapi-authentication-system)
  - [📚 Table of Contents](#-table-of-contents)
  - [🔧 Features](#-features)
  - [🛠️ Tech Stack](#️-tech-stack)
  - [⚙️ Prerequisites](#️-prerequisites)
  - [🚀 Installation](#-installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
    - [3. Install Backend Dependencies](#3-install-backend-dependencies)
    - [4. Create a `.env` File in the Project Root](#4-create-a-env-file-in-the-project-root)
    - [5. Create the MySQL Database](#5-create-the-mysql-database)
  - [▶️ Running the Application](#️-running-the-application)
  - [🔑 Key Endpoints](#-key-endpoints)
    - [Authentication](#authentication)
    - [Protected Routes](#protected-routes)
  - [🧪 Running Tests](#-running-tests)
  - [📁 Project Structure](#-project-structure)
  - [🔐 Security Features](#-security-features)
    - [✅ Implemented](#-implemented)
    - [🔜 Planned](#-planned)
  - [🌐 Frontend](#-frontend)
    - [Features](#features)
    - [Run the frontend](#run-the-frontend)
  - [🙌 Acknowledgments](#-acknowledgments)

---

## 🔧 Features

- 🔐 Secure user authentication with JWT tokens  
- 📧 Email verification system  
- 🔄 Access and refresh token flow  
- 🛡️ Protected routes with role-based access  
- 🔒 Secure password handling  
- 📝 Comprehensive test suite  
- 🚀 FastAPI with async support  
- 🗄️ SQLAlchemy ORM with async support  
- 📊 Pydantic v2 for data validation  

---

## 🛠️ Tech Stack

- **FastAPI** – Modern, fast web framework  
- **SQLAlchemy** – SQL toolkit and ORM  
- **Pydantic** – Data validation with type hints  
- **JWT** – JSON Web Tokens  
- **Pytest** – Testing framework  
- **FastAPI-Mail** – Email sending  
- **Python-jose** – JWT handling  
- **Passlib** – Password hashing  
- **MySQL** – Database engine  
- **python-multipart** – Form data parsing  

---

## ⚙️ Prerequisites

- Python 3.8+
- MySQL Server
- SMTP server for email verification
- Git (for version control)

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fastapi-auth-app.git
cd fastapi-auth-app
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.env\Scriptsctivate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Create a `.env` File in the Project Root
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

### 5. Create the MySQL Database
```sql
CREATE DATABASE fastapi_auth;
```

---

## ▶️ Running the Application

Start the FastAPI server:
```bash
uvicorn backend.app.main:app --reload
```

Access the API at:  
- Swagger UI → `http://localhost:8000/docs`  
- ReDoc → `http://localhost:8000/redoc`

---

## 🔑 Key Endpoints

### Authentication
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/verify-email`
- `POST /auth/resend-verification`
- `POST /auth/refresh`
- `POST /auth/logout`

### Protected Routes
- `GET /user/home` – Requires `Authorization: Bearer <token>`
- `GET /user/me`

---

## 🧪 Running Tests

```bash
# Run all tests
python backend/scripts/run_tests.py

# With coverage
python backend/scripts/run_tests.py -c

# Specific test file
python backend/scripts/run_tests.py -p backend/tests/test_login.py
```

---

## 📁 Project Structure

```
📁 fastapi-auth-app/
├── .env
├── .gitignore
├── README.md
├── structure.txt
├── backend/
│   ├── .coverage
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── mail_config.py
│   │   │   └── security.py
│   │   ├── dependencies/
│   │   │   └── auth.py
│   │   └── ... (routes, models, schemas, utils)
│   ├── scripts/
│   └── tests/
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── verify.html
│   ├── dashboard.html
│   ├── styles.css
│   └── script.js
```

```
fastapi-auth-app/
├── backend/
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── verify.html
│   ├── dashboard.html
│   ├── styles.css
```

---

## 🔐 Security Features

### ✅ Implemented
- Password hashing with bcrypt  
- JWT-based access and refresh token authentication  
- Token expiration and validation  
- Refresh token rotation and invalidation  
- Email verification  
- HTTP-only and SameSite cookies  
- Strong password validation  
- Input validation using Pydantic  

### 🔜 Planned
- Rate limiting  

---

## 🌐 Frontend

A simple HTML/CSS/JS frontend is included in the `frontend/` folder.

### Features
- Login & registration
- Email verification with resend
- Password confirmation & live validation
- Token-based protected dashboard
- Responsive UI

### Run the frontend
```bash
cd frontend
python -m http.server 5500
```

Then open [http://localhost:5500/index.html](http://localhost:5500/index.html)

---

## 🙌 Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Pydantic Docs](https://docs.pydantic.dev)
