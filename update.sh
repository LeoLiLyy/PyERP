#!/bin/bash

# Set variables
REPO_URL="https://github.com/LeoLiLyy/PyERP.git"
FLASK_APP="wsgi.py"  # or your main app file

# Function to print messages
print_message() {
    echo "=================================="
    echo $1
    echo "=================================="
}

# Step 1: Backup current state
print_message "Backing up current state..."
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d%H%M)
tar -czf $BACKUP_DIR/erp_backup_$DATE.tar.gz -C $PROJECT_DIR .

# Step 2: Pull latest changes from GitHub
print_message "Pulling latest changes from GitHub..."
# shellcheck disable=SC2164
cd $PROJECT_DIR
git pull origin main

# Step 3: Install new dependencies if any
print_message "Installing new dependencies..."
pip install -r requirements.txt

# Step 4: Apply database changes without deleting data
print_message "Applying database changes..."
# Run a Python script to update the database schema without deleting data
python update_db.py

print_message "Update completed successfully! Please then manually restart the docker container"