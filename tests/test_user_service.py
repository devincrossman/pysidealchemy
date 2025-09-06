import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from db.base import Base
from db.models.users import User
from services.user_service import UserService


@pytest.fixture(scope="module")
def session():
    """Fixture for creating a new database session for each test module."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="module")
def user_service(session):
    """Fixture for creating an instance of the UserService."""
    return UserService(session)


@pytest.fixture(scope="function", autouse=True)
def seed_db(session):
    """Fixture to seed the database with test data."""
    session.query(User).delete()
    hashed_password = generate_password_hash("password", method="pbkdf2:sha256")
    user1 = User(
        username="testuser1",
        password_hash=hashed_password,
        role="user",
        email="test1@test.com",
    )
    user2 = User(
        username="testuser2",
        password_hash=hashed_password,
        role="admin",
        email="test2@test.com",
    )
    session.add(user1)
    session.add(user2)
    session.commit()


def test_add_user(user_service, session):
    """Test creating a new user."""
    user = user_service.add_user("newuser", "newpassword", "newuser@test.com", "user")
    assert user is not None
    assert user.username == "newuser"
    assert user.role == "user"

    # Verify the user is in the database
    db_user = session.query(User).filter_by(username="newuser").first()
    assert db_user is not None
    assert db_user.username == "newuser"


def test_get_all_users(user_service):
    """Test getting all users."""
    users = user_service.get_all_users()
    assert len(users) == 2
    usernames = [user.username for user in users]
    assert "testuser1" in usernames
    assert "testuser2" in usernames
