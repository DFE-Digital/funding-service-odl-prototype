#!/bin/bash

# Initalise dolt in root and create gias database
cd /home/smapplebeck/odl-prototype
dolt init
dolt sql -q "CREATE DATABASE IF NOT EXISTS gias;"

# Start Dolt in the background and save its Process ID
echo "Starting Dolt Server..."
dolt sql-server --host 127.0.0.1 --port 3306 > /dev/null 2>&1 &
DOLT_PID=$!

# Allow time for startup
sleep 2

# Run Gias_ingestion script
echo "Running Python ingestion script..."
source .venv/bin/activate
python /home/smapplebeck/odl-prototype/prototype/app/data/GIAS_ingestion.py

# Get exit status of python script
SCRIPT_STATUS=$?

# Kill the background Dolt instance if still running
echo "Stopping Dolt Server..."
if kill -0 $DOLT_PID 2>/dev/null; then
    kill $DOLT_PID
else
    echo "Dolt server already stopped."
fi

# Exit with same status as python script
exit $SCRIPT_STATUS