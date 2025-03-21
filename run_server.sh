#!/bin/bash

# Configuration - Auto-detect Python path
if [ -z "$PYTHON_PATH" ]; then
  PYTHON_PATH=$(which python3 2>/dev/null || which python 2>/dev/null)
  if [ -z "$PYTHON_PATH" ]; then
    echo "ERROR: Python not found. Please install Python 3." >&2
    exit 1
  fi
fi

# Print current environment details
echo "Current directory: $(pwd)" >&2
echo "Using Python at: $PYTHON_PATH" >&2

# Check if Python exists at the specified path
if [ ! -f "$PYTHON_PATH" ]; then
  echo "ERROR: Python not found at $PYTHON_PATH" >&2
  echo "Please install Python or set the correct path in this script." >&2
  exit 1
fi

# Check if mcp is installed, if not, try to install it
if ! $PYTHON_PATH -c "import mcp" 2>/dev/null; then
  echo "MCP package not found, attempting to install..." >&2
  
  # Try to install using python -m pip
  $PYTHON_PATH -m pip install "mcp[cli]" httpx || {
    echo "Failed to install MCP package. Please install manually with:" >&2
    echo "$PYTHON_PATH -m pip install \"mcp[cli]\" httpx" >&2
    exit 1
  }
  
  # Check if installation was successful
  if ! $PYTHON_PATH -c "import mcp" 2>/dev/null; then
    echo "MCP package was installed but still can't be imported." >&2
    echo "This might be due to a Python path issue." >&2
    exit 1
  fi
fi

# Check if httpx is installed
if ! $PYTHON_PATH -c "import httpx" 2>/dev/null; then
  echo "httpx package not found, attempting to install..." >&2
  $PYTHON_PATH -m pip install httpx || {
    echo "Failed to install httpx package." >&2
    exit 1
  }
fi

# Check if dotenv is installed (for .env file support)
if ! $PYTHON_PATH -c "import dotenv" 2>/dev/null; then
  echo "python-dotenv package not found, attempting to install..." >&2
  $PYTHON_PATH -m pip install python-dotenv || {
    echo "Failed to install python-dotenv package." >&2
    exit 1
  }
fi

# Check if virtual environment exists and use it if it does
if [ -d "venv" ] && [ -f "venv/bin/python" ]; then
  echo "Using Python from virtual environment" >&2
  PYTHON_PATH=$(pwd)/venv/bin/python
  echo "Updated Python path to: $PYTHON_PATH" >&2
fi

# Attempt to check if LM Studio is running before starting
if command -v nc &> /dev/null; then
  if ! nc -z localhost 1234 2>/dev/null; then
    echo "WARNING: LM Studio does not appear to be running on port 1234" >&2
    echo "Please make sure LM Studio is running with the API server enabled" >&2
  else
    echo "✓ LM Studio API server appears to be running on port 1234" >&2
  fi
fi

# Run the server script
echo "Starting server.py with $PYTHON_PATH..." >&2
$PYTHON_PATH server.py
