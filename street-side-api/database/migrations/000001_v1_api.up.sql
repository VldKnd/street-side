CREATE SCHEMA IF NOT EXISTS "v1";

-- Company
CREATE TABLE "v1"."companies" (
    "hash_id" text PRIMARY KEY,
    "short_name" TEXT NOT NULL,
    "full_name" TEXT NOT NULL,
    "home_url" TEXT NOT NULL,
    "created_at" timestamptz NOT NULL DEFAULT (now())
);

-- Document_Type
CREATE TABLE "v1"."document_types" (
    "company_hash_id" TEXT,
    "full_name" TEXT,
    "short_name" TEXT,
    "is_quaterly" BOOLEAN,
    "is_yearly" BOOLEAN,
    "hash_id" TEXT PRIMARY KEY,
    "created_at" timestamptz NOT NULL DEFAULT (now())
);

-- Document
CREATE TABLE "v1"."documents" (
    "document_type_id" TEXT,
    "date_published" timestamptz,
    "quater" TEXT,
    "year" TEXT,
    "remote_url" TEXT,
    "extension" TEXT,
    "hash_id" TEXT PRIMARY KEY,
    "created_at" timestamptz NOT NULL DEFAULT (now())
);
