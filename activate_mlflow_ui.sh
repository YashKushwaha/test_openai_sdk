#!/usr/bin/env bash
set -e

# Resolve directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# MLflow backend database path relative to project root
MLFLOW_DIR="$SCRIPT_DIR/mlflow_logs"
DB_PATH="$MLFLOW_DIR/mlflow.db"

# Create directory if it doesn't exist
mkdir -p "$MLFLOW_DIR"

echo "Starting MLflow UI..."
echo "Backend store: sqlite:///$DB_PATH"

# Run MLflow UI
#mlflow ui --backend-store-uri "sqlite:///$DB_PATH" --host 0.0.0.0 --port 5000
mlflow ui --backend-store-uri "file:///$MLFLOW_DIR" --host 0.0.0.0 --port 5000

#mlflow ui --backend-store-uri "$POSTGRESQL" --host 0.0.0.0 --port 5000