from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class PostgresConnector:
    def __init__(self, uri: str):
        self.engine = create_engine(uri, poolclass=NullPool)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def execute_raw(self, query: str) -> None:
        with self.engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

    def table_exists(self, table_name: str) -> bool:
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}'"))
            return result.scalar() is not None

    def row_count(self, table_name: str) -> int:
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            return result.scalar()

    def calculate_checksum(self, table_name: str) -> str:
        """Calculate MD5 checksum of table contents"""
        import hashlib
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name} ORDER BY id"))
            rows = [dict(row) for row in result]
            content = str(sorted(rows, key=lambda x: str(x.get('id', ''))))
            return hashlib.md5(content.encode()).hexdigest()