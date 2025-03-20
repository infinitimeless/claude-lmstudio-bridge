# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio.

## ⚠️ Important Update for Setup

If you're getting a "No module named 'mcp'" error, there are two ways to fix it:

**Option 1: Use the wrapper scripts (Recommended)**
- On macOS/Linux: Use `run_server.sh` instead of `server.py` in your Claude Desktop config
- On Windows: Use `run_server.bat` instead of `server.py` in your Claude Desktop config

These wrapper scripts will:
- Activate the virtual environment if it exists
- Attempt to install the MCP package if it's missing
- Run the server with the correct Python environment

**Option 2: Install MCP globally**
- Run `pip install "mcp[cli]" httpx` in your system Python (not in a virtual environment)
- This ensures the MCP package is available to Claude Desktop

## Features

- List available LLM models in LM Studio
- Generate text using local LLMs
- Send chat completions to local LLMs

## Setup

1. Clone this repository
   ```bash
   git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
   cd claude-lmstudio-bridge
   ```

2. Make the wrapper script executable (macOS/Linux only):
   ```bash
   chmod +x run_server.sh
   ```

3. Start LM Studio and ensure the API server is running (in Settings > API Server)

4. Configure Claude Desktop to use this MCP server (see Configuration section below)

## Configuration

Add this server to your Claude Desktop configuration:

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

## Troubleshooting

### Common Errors

**"ModuleNotFoundError: No module named 'mcp'"**

This error means that the MCP package isn't installed in the Python environment that Claude Desktop is using to run the server.

Solutions:
1. Use the wrapper scripts as described above
2. Install MCP globally on your system with `pip install "mcp[cli]"`
3. Set up a virtual environment, install dependencies, and make sure Claude Desktop is configured to use that environment's Python

**Error: "No module named 'httpx'"**

Run:
```bash
pip install httpx
```

For more troubleshooting steps, see [INSTALLATION.md](INSTALLATION.md).

### Additional Troubleshooting

If you encounter other issues with the server:

1. **Check LM Studio**:
   - Make sure LM Studio is running
   - Ensure the API server is enabled (in Settings > API Server)
   - Default API server address is http://localhost:1234

2. **Test the Server Manually**:
   ```bash
   # Test if MCP is installed
   python -c "import mcp; print(mcp.__version__)"
   
   # Run the wrapper script directly
   ./run_server.sh  # macOS/Linux
   run_server.bat   # Windows
   ```

3. **Check the Claude Desktop logs** for detailed error messages
