"""
Test configuration and fixtures for the FastAPI authentication application.
This module sets up the test environment including:
- In-memory SQLite database for testing
- Test client fixture
- Database session fixture
- Dependency overrides for testing
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.database import Base, get_db
from backend.app.main import app

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    """
    Override the database dependency for testing.
    
    Yields:
        Session: A test database session
        
    Note:
        This function is used to override the get_db dependency
        in the FastAPI application for testing purposes.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    Test client fixture that provides a FastAPI TestClient instance.
    
    This fixture:
    1. Creates fresh database tables before each test
    2. Provides a test client instance
    3. Cleans up database tables after each test
    
    Yields:
        TestClient: A FastAPI test client instance
    """
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up after test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Database session fixture for direct database access in tests.
    
    Yields:
        Session: A SQLAlchemy database session
        
    Note:
        The session is automatically closed after each test
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close() 