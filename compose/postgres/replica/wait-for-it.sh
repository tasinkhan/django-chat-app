# wait-for-it.sh
#!/bin/bash
HOST=$1
PORT=$2
until pg_isready -h "$HOST" -p "$PORT"; do
  echo "Waiting for database at $HOST:$PORT..."
  sleep 2
done
echo "$HOST:$PORT is ready!"
