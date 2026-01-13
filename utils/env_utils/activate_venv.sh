#!/bin/bash

PROJECT_ROOT="$(pwd)"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source "$PROJECT_ROOT/venv/bin/activate"

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo "Virtual environment activated with project root in PYTHONPATH"
echo "Project root: $PROJECT_ROOT"
