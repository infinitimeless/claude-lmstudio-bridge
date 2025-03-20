# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio. This bridge allows Claude to interact with your local language models.

## 🚀 Quick Setup

For the **easiest setup** that ensures the bridge works with Claude Desktop:

### On macOS/Linux:
```bash
# Clone the repository
git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
cd claude-lmstudio-bridge

# Run the setup script
chmod +x prepare_for_claude.sh
./prepare_for_claude.sh
```

### On Windows:
```cmd
# Clone the repository
git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
cd claude-lmstudio-bridge

# Run the setup script
prepare_for_claude.bat
```

The setup scripts will:
1. Install the MCP package globally
2. Set up a virtual environment with dependencies
3. Make the wrapper scripts executable (on macOS/Linux)
4. Show you exactly how to configure Claude Desktop

## Features

- List available LLM models in LM Studio
- Generate text using local LLMs
- Send chat completions to local LLMs

## Configuration for Claude Desktop

### For macOS/Linux:

```json
{
  "mcpServers": {
    "lmstudio-bridge": {
      "command": "/bin/bash",
      "args": [
        "/absolute/path/to/claude-lmstudio-bridge/run_server.sh"
      ]
    }
  }
}
```

### For Windows:

```json
{
  "mcpServers": {
    "lmstudio-bridge": {
      "command": "cmd.exe",
      "args": [
        "/c",
        "C:\\absolute\\path\\to\\claude-lmstudio-bridge\\run_server.bat"
      ]
    }
  }
}
```

## Usage

After configuring Claude Desktop, you can use commands like:

- "List available models in LM Studio"
- "Generate text about [topic] using my local LLM"
- "Send this chat to my local LLM: [messages]"

## Auto-starting with Claude Desktop

For the bridge to start automatically with Claude Desktop:

1. Make sure you've run the `prepare_for_claude.sh` (macOS/Linux) or `prepare_for_claude.bat` (Windows) script first
2. Configure Claude Desktop as shown in the Configuration section
3. Ensure LM Studio is running with its API server enabled when you start Claude Desktop
4. Restart Claude Desktop to apply the changes

## Troubleshooting

### Common Errors

**"ModuleNotFoundError: No module named 'mcp'"**

If you see this error in the Claude Desktop logs:

1. Run the setup script again:
   ```bash
   # macOS/Linux
   ./prepare_for_claude.sh
   
   # Windows
   prepare_for_claude.bat
   ```

2. Make sure you're using the wrapper scripts:
   - `run_server.sh` on macOS/Linux
   - `run_server.bat` on Windows

**"pip: command not found"**

This occurs when the Python environment doesn't have pip in its PATH. The updated wrapper scripts use `python -m pip` instead, which should resolve this issue.

For more troubleshooting steps, see [INSTALLATION.md](INSTALLATION.md).

## Manual Installation and Advanced Configuration

For advanced users or custom setups, see [INSTALLATION.md](INSTALLATION.md) for manual installation steps and detailed configuration options.
