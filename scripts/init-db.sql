-- Space Threat Intelligence Exchange - Database Initialization
-- This script runs automatically on first PostgreSQL startup in Docker

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Initial schema is managed by Alembic migrations
-- This file ensures extensions are available
