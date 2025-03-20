#!/bin/bash

# Claude-LMStudio Bridge Installer
# This script will set up the Claude-LMStudio Bridge for use with Claude Desktop

echo "===== Claude-LMStudio Bridge Installer ====="
echo "This will configure the bridge to work with Claude Desktop"
echo

# Find Python location
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
  echo "❌ ERROR: Python 3 not found in your PATH"
  echo "Please install Python 3 first and try again"
  exit 1
fi

echo "✅ Found Python at: $PYTHON_PATH"

# Update the run_server.sh script with the correct Python path
echo "Updating run_server.sh with Python path..."
sed -i '' "s|PYTHON_PATH=.*|PYTHON_PATH=\"$PYTHON_PATH\"|g" run_server.sh
chmod +x run_server.sh

# Install required packages
echo "Installing required Python packages..."
"$PYTHON_PATH" -m pip install "mcp[cli]" httpx

# Check if installation was successful
if ! "$PYTHON_PATH" -c "import mcp" 2>/dev/null; then
  echo "❌ ERROR: Failed to install MCP package"
  echo "Try running manually: $PYTHON_PATH -m pip install \"mcp[cli]\" httpx"
  exit 1
fi

echo "✅ MCP package installed successfully"

# Get full path to the run_server.sh script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_PATH="$SCRIPT_DIR/run_server.sh"

# Create or update Claude Desktop config
CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

mkdir -p "$CONFIG_DIR"

if [ -f "$CONFIG_FILE" ]; then
  # Backup existing config
  cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
  echo "Created backup of existing config at $CONFIG_FILE.backup"
  
  # Check if JSON is valid and has mcpServers property
  if grep -q "\"mcpServers\"" "$CONFIG_FILE"; then
    # Add or update lmstudio-bridge entry
    TMP_FILE=$(mktemp)
    jq --arg path "$SCRIPT_PATH" '.mcpServers["lmstudio-bridge"] = {"command": "/bin/bash", "args": [$path]}' "$CONFIG_FILE" > "$TMP_FILE"
    mv "$TMP_FILE" "$CONFIG_FILE"
  else
    # Create mcpServers section
    TMP_FILE=$(mktemp)
    jq --arg path "$SCRIPT_PATH" '. + {"mcpServers": {"lmstudio-bridge": {"command": "/bin/bash", "args": [$path]}}}' "$CONFIG_FILE" > "$TMP_FILE"
    mv "$TMP_FILE" "$CONFIG_FILE"
  fi
else
  # Create new config file
  echo "{
  \"mcpServers\": {
    \"lmstudio-bridge\": {
      \"command\": \"/bin/bash\",
      \"args\": [
        \"$SCRIPT_PATH\"
      ]
    }
  }
}" > "$CONFIG_FILE"
fi

echo "✅ Updated Claude Desktop configuration at $CONFIG_FILE"

echo
echo "✅ Installation complete!"
echo "Please restart Claude Desktop to use the LMStudio bridge"
echo
echo "If you encounter any issues, edit run_server.sh to check settings"
echo "or refer to the README.md for troubleshooting steps."
