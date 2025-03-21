#!/bin/bash
# setup.sh - Simplified setup script for Claude-LMStudio Bridge

echo "=== Claude-LMStudio Bridge Setup ==="

# Create and activate virtual environment
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
  echo "✅ Created virtual environment"
else
  echo "✅ Virtual environment already exists"
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Installed dependencies"

# Create default configuration
if [ ! -f ".env" ]; then
  echo "Creating default configuration..."
  cat > .env << EOL
LMSTUDIO_HOST=127.0.0.1
LMSTUDIO_PORT=1234
DEBUG=false
EOL
  echo "✅ Created .env configuration file"
else
  echo "✅ Configuration file already exists"
fi

# Make run_server.sh executable
chmod +x run_server.sh
echo "✅ Made run_server.sh executable"

# Check if LM Studio is running
if nc -z localhost 1234 2>/dev/null; then
  echo "✅ LM Studio is running on port 1234"
else
  echo "⚠️ LM Studio does not appear to be running on port 1234"
  echo "   Please start LM Studio and enable the API server (Settings > API Server)"
fi

echo
echo "✅ Setup complete!"
echo
echo "To start the bridge, run:"
echo "  source venv/bin/activate && python server.py"
echo
echo "To configure with Claude Desktop:"
echo "1. Open Claude Desktop preferences"
echo "2. Navigate to the 'MCP Servers' section"
echo "3. Add a new MCP server with the following configuration:"
echo "   - Name: lmstudio-bridge"
echo "   - Command: /bin/bash"
echo "   - Arguments: $(pwd)/run_server.sh"
echo
echo "Make sure LM Studio is running with API server enabled on port 1234."
