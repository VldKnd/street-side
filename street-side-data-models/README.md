
# Migrations

## Development

Generating migration is done with [go migrate](https://github.com/golang-migrate/migrate).

`./wet-collab-api/database/migrate create -ext sql -dir ../wet-collab-api/database/migrations
-seq $(name)` will create a new migration.
The change then needs to be added to the file.

## Dev / Prod environment

Upon deployment, the migration is run on the specific environment as the first step of the docker
entrypoint

