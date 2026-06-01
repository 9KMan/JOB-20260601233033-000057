from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)