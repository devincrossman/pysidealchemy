from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    stock = Column(Integer, nullable=False, default=0)
    image_path = Column(String, nullable=True)

    orders = relationship("OrderProduct", back_populates="product")
