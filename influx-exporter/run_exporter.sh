#!/bin/bash

# Define the environment name and path
ENV_NAME="venv"
ENV_PATH="./$ENV_NAME"

# Check if the environment folder exists
if [ ! -d "$ENV_PATH" ]; then
    echo "Creating virtual environment..."
    python -m venv $ENV_NAME  # Create the virtual environment
    pip install -r requirements.txt # Install the requirement pip
fi

# Check the OS and activate the virtual environment accordingly
if [[ "$OSTYPE" == "linux-gnu" || "$OSTYPE" == "darwin"* ]]; then
    source $ENV_PATH/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    source $ENV_PATH/Scripts/activate
else
    echo "Unsupported OS for virtual environment activation."
    exit 1
fi

# Run the Python application
echo "Running the Python application..."
python query_influx.py