from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class Order(Base):
    __tablename__ = "orders"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    shipping_address = Column(Text)
    notes = Column(Text)
    is_deleted = Column(Boolean, default=False)