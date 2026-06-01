from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    mongodb_connected: bool
    postgres_connected: bool

class MigrationStartRequest(BaseModel):
    collection_name: str
    target_table: str
    batch_size: Optional[int] = 1000

class MigrationStatusResponse(BaseModel):
    job_id: UUID
    status: str
    source_collection: str
    target_table: str
    records_processed: int
    records_failed: int
    checksum_before: Optional[str]
    checksum_after: Optional[str]
    error_message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]

class ValidationRequest(BaseModel):
    collection_name: str
    table_name: str

class ValidationResponse(BaseModel):
    is_balanced: bool
    checksum_match: bool
    source_count: int
    target_count: int