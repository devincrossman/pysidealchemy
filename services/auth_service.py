# services/auth_service.py
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from db.models.users import User


class AuthService:
    """Authentication and authorization service using SQLAlchemy User model."""

    roles = {"user": 1, "admin": 2}  # role hierarchy

    def __init__(self, session: Session):
        self.session = session
        self.current_user: User | None = None

    def authenticate_user(self, username: str, password: str) -> bool:
        """Verify username + password. Sets current_user if valid."""
        user = self.session.query(User).filter_by(username=username).first()
        if user and check_password_hash(str(user.password_hash), password):
            self.current_user = user
            return True
        return False

    def logout(self):
        """Clear the current user."""
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def is_authorized(self, required_role: str = "user") -> bool:
        """Check if current_user has the required role."""
        if not self.is_authenticated():
            return False
        user_role = str(self.current_user.role) # type: ignore
        return self.roles.get(user_role, 0) >= self.roles.get(required_role, 0)

auth_service: AuthService | None = None

def init_auth_service(session: Session):
    global auth_service
    if auth_service is None:
        auth_service = AuthService(session)
    return auth_service

def get_auth_service():
    global auth_service
    return auth_service
