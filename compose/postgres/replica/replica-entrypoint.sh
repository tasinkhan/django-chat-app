#!/bin/bash
set -e

REPLICA_DATA_DIR="/var/lib/postgresql/data"
PRIMARY_CONNINFO="host=db_master port=5432 user=replicator password=12345"

# Check if the replica has been initialized by looking for the PG_VERSION file
if [ ! -s "$REPLICA_DATA_DIR/PG_VERSION" ]; then
    echo "Replica not initialized. Performing base backup..."
    
    # Perform a base backup from the master
    pg_basebackup -h db_master -D "$REPLICA_DATA_DIR" -U replicator -v -P --wal-method=stream

    # Create recovery configuration for PostgreSQL 13+
    echo "Creating standby.signal and configuring primary_conninfo..."
    touch "$REPLICA_DATA_DIR/standby.signal"

    # Create a recovery configuration file with connection info to the master
    echo "primary_conninfo = 'host=db_master port=5432 user=replicator password=12345'" >> "$REPLICA_DATA_DIR/postgresql.auto.conf"
fi

# Execute the default entrypoint to start PostgreSQL
exec docker-entrypoint.sh postgres
