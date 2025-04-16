#!/bin/bash
set -e

REPLICA_DATA_DIR="/var/lib/postgresql/data"

if [ ! -s "$REPLICA_DATA_DIR/PG_VERSION" ]; then
    echo "Replica not initialized. Performing base backup..."
    pg_basebackup -h db_master -D "$REPLICA_DATA_DIR" -U replicator -v -P --wal-method=stream
fi

exec docker-entrypoint.sh postgres
