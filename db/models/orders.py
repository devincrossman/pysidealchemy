from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False, default="Pending")

    # Relationships
    products = relationship(
        "OrderProduct", back_populates="order", cascade="all, delete-orphan"
    )
    user = relationship("User")

    @property
    def total(self):
        return sum(op.product.price * op.quantity for op in self.products)
