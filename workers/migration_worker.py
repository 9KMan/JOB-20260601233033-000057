"""
Background worker for running MongoDB to PostgreSQL migrations.
Can be run standalone or via Celery/BullMQ.
"""
import argparse
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import MongoDBConnector, PostgresConnector, MigrationEngine
from api.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_full_migration():
    """Run full migration of all collections"""
    logger.info("Starting full migration...")
    
    mongo = MongoDBConnector(settings.mongodb_uri, settings.mongodb_database)
    mongo.connect()
    
    pg = PostgresConnector(settings.postgres_uri)
    engine = MigrationEngine(mongo, pg)
    
    collections = mongo.list_collections()
    logger.info(f"Found collections: {collections}")
    
    results = []
    for collection in collections:
        # Skip system collections
        if collection.startswith('system.'):
            continue
        logger.info(f"Migrating collection: {collection}")
        log = engine.migrate_collection(collection, collection)
        results.append({
            'collection': collection,
            'status': log.status,
            'processed': log.records_processed,
            'failed': log.records_failed
        })
    
    mongo.disconnect()
    logger.info(f"Migration complete. Results: {results}")
    return results

def run_collection_migration(collection_name: str, target_table: str = None):
    """Migrate a specific collection"""
    logger.info(f"Migrating {collection_name}...")
    
    mongo = MongoDBConnector(settings.mongodb_uri, settings.mongodb_database)
    mongo.connect()
    
    pg = PostgresConnector(settings.postgres_uri)
    engine = MigrationEngine(mongo, pg)
    
    target = target_table or collection_name
    log = engine.migrate_collection(collection_name, target)
    
    mongo.disconnect()
    logger.info(f"Migration complete: {log.status}")
    return log

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MongoDB to PostgreSQL Migration Worker')
    parser.add_argument('--full', action='store_true', help='Run full migration')
    parser.add_argument('--collection', type=str, help='Migrate specific collection')
    parser.add_argument('--target', type=str, help='Target table name')
    
    args = parser.parse_args()
    
    if args.full:
        run_full_migration()
    elif args.collection:
        run_collection_migration(args.collection, args.target)
    else:
        parser.print_help()
