# MongoDB to PostgreSQL Migration

## Overview

A robust, production-ready database migration solution for moving from MongoDB to PostgreSQL with complete data integrity preservation.

## Features

- **Bidirectional Migration Support**: Extract from MongoDB, load to PostgreSQL
- **Data Integrity Validation**: Checksums, row counts, and schema validation at each stage
- **Incremental Migration**: Supports batch processing for large datasets
- **Rollback Capability**: Track migration state and rollback if needed
- **Type Mapping**: Automatic MongoDB BSON to PostgreSQL type conversion
- **Error Handling**: Detailed error reporting with retry logic

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    MongoDB     │────▶│  Migration Core  │────▶│   PostgreSQL   │
│  (Source DB)   │     │  (ETL Pipeline)  │     │  (Target DB)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │ Integrity Check  │
                        │   & Validation   │
                        └──────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- MongoDB 4.4+

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Set environment variables:

```bash
export MONGODB_URI="mongodb://localhost:27017"
export MONGODB_DATABASE="source_db"
export POSTGRES_URI="postgresql://user:pass@localhost:5432/target_db"
```

### Run Migration

```bash
# Initialize database schema
alembic upgrade head

# Run migration
python -m workers.migration_worker --full

# Validate data integrity
python -m services.validator --check-all
```

## Project Structure

```
├── api/                  # FastAPI routes and schemas
├── models/               # SQLAlchemy models
├── services/             # Business logic and migration engine
├── workers/              # Background job handlers
├── migrations/           # Alembic database migrations
├── tests/                # Unit and integration tests
├── Dockerfile            # Production container
├── docker-compose.yml    # Local development environment
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | Health check |
| POST | /api/v1/migrate/start | Start migration job |
| GET | /api/v1/migrate/status/{job_id} | Get migration status |
| POST | /api/v1/migrate/rollback | Rollback to version |
| GET | /api/v1/collections | List MongoDB collections |
| POST | /api/v1/validate | Run integrity validation |

## License

MIT
