#!/bin/bash

# Start Docker containers
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Activate virtual environment and run the seed data script
source venv/bin/activate
python -m src.seed_data

echo "Database setup and seeding completed!"