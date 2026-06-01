from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class MongoDBConnector:
    def __init__(self, uri: str, database: str):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.uri = uri
        self.database_name = database

    def connect(self) -> None:
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database_name]
        logger.info(f"Connected to MongoDB: {self.database_name}")

    def disconnect(self) -> None:
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

    def list_collections(self) -> List[str]:
        return self.db.list_collection_names()

    def get_collection(self, name: str):
        return self.db[name]

    def get_documents(self, collection: str, query: Dict = None, limit: int = None) -> List[Dict]:
        coll = self.get_collection(collection)
        cursor = coll.find(query or {})
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    def get_document_count(self, collection: str, query: Dict = None) -> int:
        coll = self.get_collection(collection)
        return coll.count_documents(query or {})

    def calculate_checksum(self, collection: str) -> str:
        """Calculate MD5 checksum of all documents for integrity tracking"""
        import hashlib
        docs = self.get_documents(collection)
        content = str(sorted(docs, key=lambda x: str(x.get('_id', ''))))
        return hashlib.md5(content.encode()).hexdigest()