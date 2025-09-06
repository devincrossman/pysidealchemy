from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from db.base import Base, SessionLocal, engine
from db.models.users import User
from utils.config import DEFAULT_ADMIN_PASSWORD


def create_db():
    """Ensures all database tables are created"""
    # import all models
    from db.models.orders import Order  # noqa: F401
    from db.models.products import Product  # noqa: F401
    from db.models.users import User  # noqa: F401

    # create all tables.
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        ensure_default_admin(session)


def ensure_default_admin(session: Session):
    """Create a default admin user if none exists."""
    admin = session.query(User).filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password_hash=generate_password_hash(DEFAULT_ADMIN_PASSWORD),
            email="admin@example.com",
            role="admin",
        )
        session.add(admin)
        session.commit()
        print("✅ Default admin user created (username='admin').")
