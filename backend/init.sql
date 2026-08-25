-- PratiBimb Praman — Database Initialization
-- This runs on first container start to set up pgvector and schemas

-- Enable pgvector extension for CLIP embedding similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable pg_trgm for fuzzy text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
