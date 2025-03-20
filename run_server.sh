#!/bin/bash

# Print current environment details
echo "Current directory: $(pwd)" >&2
echo "Python location: $(which python 2>/dev/null || echo 'Python not in PATH')" >&2

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  echo "Activating virtual environment..." >&2
  source venv/bin/activate
  echo "Activated Python: $(which python 2>/dev/null || echo 'Python not in PATH')" >&2
fi

# Check if mcp is installed, if not, try to install it
if ! python -c "import mcp" 2>/dev/null; then
  echo "MCP package not found, attempting to install..." >&2
  
  # Try to install using python -m pip instead of direct pip call
  python -m pip install "mcp[cli]" httpx || {
    echo "Failed to install MCP package. Please install manually with:" >&2
    echo "python -m pip install \"mcp[cli]\"" >&2
    
    # Additional guidance for Claude Desktop startup integration
    echo "" >&2
    echo "For Claude Desktop Startup Integration:" >&2
    echo "1. Open Terminal and navigate to this directory" >&2
    echo "2. Run: python -m pip install \"mcp[cli]\" httpx" >&2
    echo "3. Make sure this script is executable: chmod +x run_server.sh" >&2
    exit 1
  }
  
  # Check if installation was successful
  if ! python -c "import mcp" 2>/dev/null; then
    echo "MCP package was installed but still can't be imported." >&2
    echo "This might be due to a Python path issue." >&2
    exit 1
  fi
fi

# Run the server script
echo "Starting server.py with $(which python 2>/dev/null || echo 'Python')..." >&2
python server.py
