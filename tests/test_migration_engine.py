import pytest
from services.migration_engine import MigrationEngine

def test_migration_engine_initialization(mock_mongodb, mock_postgres):
    engine = MigrationEngine(mock_mongodb, mock_postgres)
    assert engine.mongodb == mock_mongodb
    assert engine.postgres == mock_postgres
    assert engine.BATCH_SIZE == 1000

def test_validate_migration(mock_mongodb, mock_postgres):
    engine = MigrationEngine(mock_mongodb, mock_postgres)
    result = engine.validate_migration('users', 'users')
    assert result['is_balanced'] == True
    assert result['source_count'] == 100
    assert result['target_count'] == 100

def test_transform_document_handles_objectid():
    engine = MigrationEngine(None, None)
    doc = {'_id': '507f1f77bcf86cd799439011', 'name': 'Test'}
    result = engine._transform_document(doc)
    assert 'id' in result
    assert result['id'] == '507f1f77bcf86cd799439011'
