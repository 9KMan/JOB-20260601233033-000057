from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class IntegrityChecker:
    """Checks data integrity by comparing checksums between MongoDB and PostgreSQL"""

    def __init__(self, mongodb_connector, postgres_connector):
        self.mongodb = mongodb_connector
        self.postgres = postgres_connector

    def check_integrity(self, collection_name: str, table_name: str) -> Dict[str, Any]:
        """Compare checksums to verify data integrity"""
        mongo_checksum = self.mongodb.calculate_checksum(collection_name)
        pg_checksum = self.postgres.calculate_checksum(table_name)
        return {
            "collection": collection_name,
            "table": table_name,
            "mongo_checksum": mongo_checksum,
            "pg_checksum": pg_checksum,
            "integrity_valid": mongo_checksum == pg_checksum
        }

    def check_all(self) -> List[Dict[str, Any]]:
        """Check integrity of all collections against their corresponding tables"""
        collections = self.mongodb.list_collections()
        return [self.check_integrity(c, c) for c in collections]