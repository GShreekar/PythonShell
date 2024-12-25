#!/bin/sh

# Exit on error
set -e

# Check if pipenv is installed
if ! command -v pipenv >/dev/null 2>&1; then
    echo "Error: pipenv is not installed"
    echo "Please install pipenv first: pip install pipenv"
    exit 1
fi

# Check if Pipfile exists
if [ ! -f "Pipfile" ]; then
    echo "Error: Pipfile not found"
    echo "Please ensure you are in the correct directory"
    exit 1
fi

# Ignore the current virtual environment
export PIPENV_IGNORE_VIRTUALENVS=1

# Run the Python program with pipenv
# Arguments are passed through using "$@"
exec pipenv run python3 -u -m app.main "$@"
