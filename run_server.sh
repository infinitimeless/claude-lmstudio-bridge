#!/bin/bash

# Print current environment details
echo "Current directory: $(pwd)" >&2

# Find Python executable with absolute path
PYTHON_PATH=$(which python3 2>/dev/null || which python 2>/dev/null || echo "/usr/bin/python3")
echo "Using Python: $PYTHON_PATH" >&2

# Check if mcp is installed, if not, try to install it
if ! $PYTHON_PATH -c "import mcp" 2>/dev/null; then
  echo "MCP package not found, attempting to install..." >&2
  
  # Try to install using python -m pip instead of direct pip call
  $PYTHON_PATH -m pip install "mcp[cli]" httpx || {
    echo "Failed to install MCP package. Please install manually with:" >&2
    echo "$PYTHON_PATH -m pip install \"mcp[cli]\"" >&2
    
    # Additional guidance for Claude Desktop startup integration
    echo "" >&2
    echo "For Claude Desktop Startup Integration:" >&2
    echo "1. Open Terminal and navigate to this directory" >&2
    echo "2. Run: $PYTHON_PATH -m pip install \"mcp[cli]\" httpx" >&2
    echo "3. Make sure this script is executable: chmod +x run_server.sh" >&2
    exit 1
  }
  
  # Check if installation was successful
  if ! $PYTHON_PATH -c "import mcp" 2>/dev/null; then
    echo "MCP package was installed but still can't be imported." >&2
    echo "This might be due to a Python path issue." >&2
    exit 1
  fi
fi

# Run the server script
echo "Starting server.py with $PYTHON_PATH..." >&2
$PYTHON_PATH server.py
