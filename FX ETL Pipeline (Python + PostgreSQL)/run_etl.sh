#!/bin/bash

# Fail fast
set -e

PROJECT_DIR="/home/sherif/data-engineering-projects/FX ETL Pipeline (Python + PostgreSQL)"
VENV_DIR="$PROJECT_DIR/venv"

# Go to project directory (IMPORTANT)
cd "$PROJECT_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Run the ETL script
python main.py
