#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  echo "Activating virtual environment..." >&2
  source venv/bin/activate
fi

# Check if mcp is installed, if not, try to install it
if ! python -c "import mcp" 2>/dev/null; then
  echo "MCP package not found, attempting to install..." >&2
  pip install "mcp[cli]" httpx
  
  # Check if installation was successful
  if ! python -c "import mcp" 2>/dev/null; then
    echo "Failed to install MCP package. Please install manually with:" >&2
    echo "pip install \"mcp[cli]\"" >&2
    exit 1
  fi
fi

# Run the server script
echo "Starting server.py with $(which python)..." >&2
python server.py
