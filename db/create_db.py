from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from db.base import Base, SessionLocal, engine
from db.models.order_products import OrderProduct  # noqa: F401
from db.models.orders import Order  # noqa: F401
from db.models.products import Product  # noqa: F401
from db.models.users import User  # noqa: F401
from utils.config import DEFAULT_ADMIN_PASSWORD


def create_db():
    """Ensures all database tables are created"""
    # import all models

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
        add_sample_data(session)


def add_sample_data(session: Session):
    """Add sample data"""
    # Create a sample user
    alice = User(
        username="alice",
        password_hash=generate_password_hash(DEFAULT_ADMIN_PASSWORD),
        email="alice@example.com",
        role="user",
    )
    bob = User(
        username="bob",
        password_hash=generate_password_hash(DEFAULT_ADMIN_PASSWORD),
        email="bob@example.com",
        role="user",
    )
    session.add(alice)
    session.add(bob)

    # Create some products
    product1 = Product(name="Laptop", price=1200.0, stock=10)
    product2 = Product(name="Mouse", price=25.0, stock=100)
    product3 = Product(name="Keyboard", price=45.0, stock=50)
    session.add_all([product1, product2, product3])

    session.flush()  # flush so we get IDs assigned

    # Create an order
    order = Order(user_id=alice.id, status="Pending")
    session.add(order)
    session.flush()

    # Link products to the order
    order_product1 = OrderProduct(order_id=order.id, product_id=product1.id, quantity=1)
    order_product2 = OrderProduct(order_id=order.id, product_id=product2.id, quantity=2)
    session.add_all([order_product1, order_product2])

    # Commit everything
    session.commit()
    print("Sample data added.")
