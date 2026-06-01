from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class Product(Base):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)