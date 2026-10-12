#!/usr/bin/env bash
set -e

docker compose up --build -d

echo "API available at http://localhost:8000/docs"