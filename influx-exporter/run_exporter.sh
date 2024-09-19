#!/bin/bash

# Define the environment name and path
ENV_NAME="venv"
ENV_PATH="./$ENV_NAME"
STATUS_ENV="The env is activated"

# Check if the environment folder exists
if [ ! -d "$ENV_PATH" ]; then
    echo "Creating virtual environment..."
    python -m venv $ENV_NAME  # Create the virtual environment
fi

# Check the OS and activate the virtual environment accordingly
if [[ "$OSTYPE" == "linux-gnu" || "$OSTYPE" == "darwin"* ]]; then
    source $ENV_PATH/bin/activate
    echo $STATUS_ENV
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    source $ENV_PATH/Scripts/activate
    echo $STATUS_ENV
else
    echo "Unsupported OS for virtual environment activation."
    exit 1
fi

echo "Install the requirements"
pip install -r requirements.txt # Install the requirement pip

# Run the Python application
echo "Running the Python application..."
python query_influx.py