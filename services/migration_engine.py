from datetime import datetime
from typing import Dict, List, Optional, Any
from models.migration_log import MigrationLog
import logging
import uuid

logger = logging.getLogger(__name__)

class MigrationEngine:
    """
    Core migration engine that orchestrates data migration from MongoDB to PostgreSQL.
    Handles batching, error recovery, and progress tracking.
    """
    
    BATCH_SIZE = 1000
    
    TYPE_MAPPING = {
        'string': 'VARCHAR(255)',
        'int': 'INTEGER',
        'long': 'BIGINT',
        'double': 'DOUBLE PRECISION',
        'boolean': 'BOOLEAN',
        'date': 'TIMESTAMP',
        'datetime': 'TIMESTAMP',
        'array': 'JSONB',
        'object': 'JSONB',
        'null': 'VARCHAR(255)',
    }
    
    def __init__(self, mongodb_client, postgres_client):
        self.mongodb = mongodb_client
        self.postgres = postgres_client
        self.migration_id = str(uuid.uuid4())
    
    def migrate_collection(self, collection_name: str, target_table: str) -> MigrationLog:
        """
        Migrate a single MongoDB collection to PostgreSQL table.
        Returns MigrationLog with statistics.
        """
        log = MigrationLog(
            id=uuid.uuid4(),
            source_collection=collection_name,
            target_table=target_table,
            status='started',
            started_at=datetime.utcnow()
        )
        
        try:
            # Get total count
            total = self.mongodb.get_document_count(collection_name)
            log.records_processed = 0
            log.records_failed = 0
            
            # Calculate source checksum
            log.checksum_before = self.mongodb.calculate_checksum(collection_name)
            
            # Process in batches
            processed = 0
            failed = 0
            
            while processed < total:
                batch = self.mongodb.get_documents(collection_name, limit=self.BATCH_SIZE)
                if not batch:
                    break
                
                # Transform and insert batch
                success, fail = self._process_batch(batch, target_table)
                processed += success
                failed += fail
                
                logger.info(f"Migrated {processed}/{total} from {collection_name}")
            
            log.records_processed = processed
            log.records_failed = failed
            log.status = 'completed'
            log.completed_at = datetime.utcnow()
            
            # Calculate target checksum
            if self.postgres.table_exists(target_table):
                log.checksum_after = self.postgres.calculate_checksum(target_table)
            
            logger.info(f"Migration complete: {processed} success, {failed} failed")
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            logger.error(f"Migration failed: {e}")
        
        return log
    
    def _process_batch(self, documents: List[Dict], target_table: str) -> tuple:
        """Process a batch of documents, return (success_count, failed_count)"""
        success = 0
        failed = 0
        
        for doc in documents:
            try:
                # Transform MongoDB document to PostgreSQL format
                transformed = self._transform_document(doc)
                self._insert_into_postgres(transformed, target_table)
                success += 1
            except Exception as e:
                logger.error(f"Failed to migrate document {doc.get('_id')}: {e}")
                failed += 1
        
        return success, failed
    
    def _transform_document(self, doc: Dict) -> Dict:
        """Transform MongoDB BSON document to PostgreSQL-compatible format"""
        from bson import ObjectId
        from bson.errors import InvalidId
        
        result = {}
        for key, value in doc.items():
            if key == '_id':
                try:
                    result['id'] = str(ObjectId(value)) if isinstance(value, str) else str(value)
                except InvalidId:
                    result['id'] = str(value)
            elif isinstance(value, list):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = str(value)
            else:
                result[key] = value
        return result
    
    def _insert_into_postgres(self, document: Dict, table: str) -> None:
        """Insert transformed document into PostgreSQL"""
        # Build dynamic insert - simplified for generic migration
        columns = ', '.join(document.keys())
        placeholders = ', '.join([f':{k}' for k in document.keys()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.postgres.execute_raw(query, document)
    
    def validate_migration(self, collection: str, table: str) -> Dict[str, Any]:
        """Validate migration integrity"""
        mongo_count = self.mongodb.get_document_count(collection)
        pg_count = self.postgres.row_count(table) if self.postgres.table_exists(table) else 0
        
        return {
            'source_collection': collection,
            'target_table': table,
            'source_count': mongo_count,
            'target_count': pg_count,
            'is_balanced': mongo_count == pg_count,
            'checksum_match': self.mongodb.calculate_checksum(collection) == self.postgres.calculate_checksum(table)
        }