from fastapi import APIRouter, HTTPException, Depends
from api.schemas import (
    HealthResponse, MigrationStartRequest, MigrationStatusResponse,
    ValidationRequest, ValidationResponse
)
from api.config import settings
from services import MongoDBConnector, PostgresConnector, MigrationEngine
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
api_router = APIRouter()

_mongo_client = None
_postgres_client = None

def get_mongo():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoDBConnector(settings.mongodb_uri, settings.mongodb_database)
        _mongo_client.connect()
    return _mongo_client

def get_postgres():
    global _postgres_client
    if _postgres_client is None:
        _postgres_client = PostgresConnector(settings.postgres_uri)
    return _postgres_client

@api_router.get("/health", response_model=HealthResponse)
async def health_check():
    mongo = get_mongo()
    pg = get_postgres()
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        mongodb_connected=mongo.client is not None,
        postgres_connected=True
    )

@api_router.post("/migrate/start")
async def start_migration(request: MigrationStartRequest):
    mongo = get_mongo()
    pg = get_postgres()
    engine = MigrationEngine(mongo, pg)
    result = engine.migrate_collection(request.collection_name, request.target_table)
    return {"message": "Migration completed", "log_id": str(result.id)}

@api_router.get("/migrate/status/{log_id}")
async def get_migration_status(log_id: str):
    return {"status": "completed", "log_id": log_id}

@api_router.get("/collections")
async def list_collections():
    mongo = get_mongo()
    return {"collections": mongo.list_collections()}

@api_router.post("/validate", response_model=ValidationResponse)
async def validate_migration(request: ValidationRequest):
    mongo = get_mongo()
    pg = get_postgres()
    engine = MigrationEngine(mongo, pg)
    result = engine.validate_migration(request.collection_name, request.table_name)
    return ValidationResponse(**result)