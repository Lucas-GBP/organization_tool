#!/bin/sh

# Exit in case of error
set -e
clear

docker-compose exec backend "./scripts/mypy.sh"

echo "Running prettier and lint in the frontend..."
docker-compose exec frontend npm run fix