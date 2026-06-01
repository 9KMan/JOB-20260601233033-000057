from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    """Validates data consistency between MongoDB and PostgreSQL"""

    def __init__(self, mongodb_connector, postgres_connector):
        self.mongodb = mongodb_connector
        self.postgres = postgres_connector

    def validate_collection(self, collection_name: str, table_name: str) -> Dict[str, Any]:
        """Validate data between MongoDB collection and PostgreSQL table"""
        mongo_count = self.mongodb.get_document_count(collection_name)
        pg_count = self.postgres.row_count(table_name) if self.postgres.table_exists(table_name) else 0
        return {
            "collection": collection_name,
            "table": table_name,
            "mongo_count": mongo_count,
            "pg_count": pg_count,
            "match": mongo_count == pg_count
        }

    def validate_all(self) -> List[Dict[str, Any]]:
        """Validate all collections against their corresponding tables"""
        collections = self.mongodb.list_collections()
        return [self.validate_collection(c, c) for c in collections]