#!/bin/bash
#
# This script prepares the Claude-LMStudio Bridge for use with Claude Desktop
# It installs required packages and ensures everything is ready to run
#

echo "=== Claude-LMStudio Bridge Setup ==="
echo "This script will prepare the environment for use with Claude Desktop"
echo

# Make the run script executable
chmod +x run_server.sh
echo "✅ Made run_server.sh executable"

# Try to install MCP globally to ensure it's available
echo "Installing MCP package globally..."
python -m pip install "mcp[cli]" httpx

# Check if installation was successful
if python -c "import mcp" 2>/dev/null; then
  echo "✅ MCP package installed successfully"
else
  echo "❌ Failed to install MCP package. Please check your Python installation."
  exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
  echo "✅ Created virtual environment"
  
  # Activate and install dependencies
  source venv/bin/activate
  python -m pip install -r requirements.txt
  echo "✅ Installed dependencies in virtual environment"
else
  echo "✅ Virtual environment already exists"
fi

# Display configuration instructions
echo
echo "=== Configuration Instructions ==="
echo "1. Open Claude Desktop preferences"
echo "2. Navigate to the 'MCP Servers' section"
echo "3. Add a new MCP server with the following configuration:"
echo
echo "   Name: lmstudio-bridge"
echo "   Command: /bin/bash"
echo "   Arguments: $(pwd)/run_server.sh"
echo
echo "4. Start LM Studio and ensure the API server is running"
echo "5. Restart Claude Desktop"
echo
echo "Setup complete! You can now use the LMStudio bridge with Claude Desktop."
