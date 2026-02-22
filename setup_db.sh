#!/bin/bash

echo "Setting up PostgreSQL database for Event Manager..."

echo "Step 1: Creating PostgreSQL user 'ivan' (if it doesn't exist)..."
sudo -u postgres psql -c "CREATE USER ivan WITH PASSWORD 'postgres';" 2>/dev/null || echo "User might already exist, continuing..."

echo "Step 2: Creating database 'event_manager_db'..."
sudo -u postgres psql -c "CREATE DATABASE event_manager_db OWNER ivan;" 2>/dev/null || echo "Database might already exist, continuing..."

echo "Step 3: Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE event_manager_db TO ivan;" 2>/dev/null

echo ""
echo "Database setup complete!"
echo ""
echo "If you need to change the database password, update it in event_manager/settings.py"
echo "Then run: python manage.py makemigrations && python manage.py migrate"

