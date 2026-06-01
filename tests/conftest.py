import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_mongodb():
    mongo = MagicMock()
    mongo.client = MagicMock()
    mongo.list_collections.return_value = ['users', 'products', 'orders']
    mongo.get_document_count.return_value = 100
    mongo.get_documents.return_value = [
        {'_id': '1', 'name': 'Test', 'email': 'test@example.com'},
        {'_id': '2', 'name': 'Test2', 'email': 'test2@example.com'},
    ]
    mongo.calculate_checksum.return_value = 'abc123'
    return mongo

@pytest.fixture
def mock_postgres():
    pg = MagicMock()
    pg.table_exists.return_value = True
    pg.row_count.return_value = 100
    pg.calculate_checksum.return_value = 'abc123'
    return pg
