#/bin/bash
#Fail fast
set -e

# Absoulte path to this script
PROJECT_DIR="/home/sherif/data-engineering-projects/FX\ ETL\ Pipeline\ \(Python\ +\ PostgreSQL\)"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON="$VENV_DIR/bin/python"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Run the ETL script
$PYTHON "$PROJECT_DIR/main.py"