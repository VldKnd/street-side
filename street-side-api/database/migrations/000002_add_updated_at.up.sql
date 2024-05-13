CREATE SCHEMA IF NOT EXISTS "v1";

-- Company
ALTER TABLE "v1"."companies"
    ADD COLUMN "updated_at" timestamptz DEFAULT (now());