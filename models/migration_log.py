from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class MigrationLog(Base):
    __tablename__ = "migration_logs"

    source_collection = Column(String(255), nullable=False)
    target_table = Column(String(255), nullable=False)
    records_processed = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    status = Column(String(50), nullable=False)
    checksum_before = Column(String(64))
    checksum_after = Column(String(64))
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))