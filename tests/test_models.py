import pytest
from models.base import Base
from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.migration_log import MigrationLog
from sqlalchemy import inspect

def test_user_model_has_required_columns():
    columns = [c.name for c in inspect(User).columns]
    assert 'id' in columns
    assert 'email' in columns
    assert 'username' in columns
    assert 'created_at' in columns
    assert 'updated_at' in columns

def test_product_model_has_required_columns():
    columns = [c.name for c in inspect(Product).columns]
    assert 'id' in columns
    assert 'name' in columns
    assert 'price' in columns
    assert 'sku' in columns

def test_order_model_has_foreign_key():
    columns = [c.name for c in inspect(Order).columns]
    assert 'user_id' in columns

def test_migration_log_model():
    columns = [c.name for c in inspect(MigrationLog).columns]
    assert 'source_collection' in columns
    assert 'target_table' in columns
    assert 'status' in columns
    assert 'checksum_before' in columns
    assert 'checksum_after' in columns
