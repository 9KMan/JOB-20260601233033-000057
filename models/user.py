from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)