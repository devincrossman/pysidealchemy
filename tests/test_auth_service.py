import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models.users import User
from services.auth_service import AuthService
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def session():
    """Fixture for creating a new database session for each test module."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def auth_service(session):
    """Fixture for creating an instance of the AuthService."""
    return AuthService(session)


@pytest.fixture(scope="module", autouse=True)
def seed_db(session):
    """Fixture to seed the database with test data."""
    hashed_password = generate_password_hash("password", method="pbkdf2:sha256")
    user = User(username="testuser", password_hash=hashed_password, role="user")
    admin = User(username="admin", password_hash=hashed_password, role="admin")
    session.add(user)
    session.add(admin)
    session.commit()


def test_authenticate_user_success(auth_service):
    """Test successful user authentication."""
    assert auth_service.authenticate_user("testuser", "password") is True
    assert auth_service.current_user is not None
    assert auth_service.current_user.username == "testuser"


def test_authenticate_user_failure(auth_service):
    """Test failed user authentication."""
    assert auth_service.authenticate_user("testuser", "wrongpassword") is False
    assert auth_service.current_user is None


def test_logout(auth_service):
    """Test logging out."""
    auth_service.authenticate_user("testuser", "password")
    assert auth_service.is_authenticated() is True
    auth_service.logout()
    assert auth_service.is_authenticated() is False


def test_is_authenticated(auth_service):
    """Test the is_authenticated method."""
    auth_service.logout()
    assert auth_service.is_authenticated() is False
    auth_service.authenticate_user("testuser", "password")
    assert auth_service.is_authenticated() is True


def test_is_authorized_user(auth_service):
    """Test authorization for a regular user."""
    auth_service.authenticate_user("testuser", "password")
    assert auth_service.is_authorized("user") is True
    assert auth_service.is_authorized("admin") is False


def test_is_authorized_admin(auth_service):
    """Test authorization for an admin user."""
    auth_service.authenticate_user("admin", "password")
    assert auth_service.is_authorized("user") is True
    assert auth_service.is_authorized("admin") is True


def test_is_authorized_not_authenticated(auth_service):
    """Test authorization when not authenticated."""
    auth_service.logout()
    assert auth_service.is_authorized("user") is False


def test_failed_login_does_not_logout_existing_user(auth_service):
    """Test that a failed login attempt does not log out an existing user."""
    # First, log in as a regular user
    auth_service.authenticate_user("testuser", "password")
    assert auth_service.is_authenticated() is True
    assert auth_service.current_user.username == "testuser"

    # Now, attempt to log in as admin with the wrong password
    auth_service.authenticate_user("admin", "wrongpassword")

    # Verify that the original user is still logged in
    assert auth_service.is_authenticated() is True
    assert auth_service.current_user.username == "testuser"
