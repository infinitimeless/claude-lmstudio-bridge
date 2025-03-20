# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio.

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

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

4. **Install MCP and other dependencies:**
   ```bash
   # Using uv (recommended)
   pip install uv
   uv add "mcp[cli]" httpx

   # OR using pip
   pip install "mcp[cli]" httpx
   ```

5. Verify MCP installation:
   ```bash
   python -c "import mcp; print(mcp.__version__)"
   ```

6. Test the MCP package installation:
   ```bash
   python test_mcp.py
   ```

7. Start LM Studio and ensure the API server is running (usually on port 1234)

8. Configure Claude Desktop to use this MCP server

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md).

## Testing

Before configuring Claude to use the server, you can test it:

1. First, test if the MCP package is working:
   ```bash
   python test_mcp.py
   ```

2. Then try the debug server:
   ```bash
   python debug_server.py
   ```
   
3. If the debug server works, try the full server:
   ```bash
   python server.py
   ```

## Configuration

Add this server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "lmstudio-bridge": {
      "command": "python",
      "args": [
        "/absolute/path/to/server.py"
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

This is the most common error and indicates that the MCP package isn't installed in your current Python environment. To fix this:

```bash
# Make sure you're in the right virtual environment
source venv/bin/activate  # On macOS/Linux

# Install the MCP SDK
pip install "mcp[cli]"
```

For more troubleshooting steps, see [INSTALLATION.md](INSTALLATION.md).

### Additional Troubleshooting

If you encounter other issues with the server:

1. **Check Dependencies**:
   ```bash
   pip list | grep mcp
   pip list | grep httpx
   ```

2. **Check LM Studio**:
   - Make sure LM Studio is running
   - Ensure the API server is enabled (in Settings > API Server)
   - Verify the API is accessible at http://localhost:1234/v1/models

3. **Test Incrementally**:
   - Run `test_mcp.py` to verify MCP installation
   - Run `debug_server.py` to test minimal MCP server functionality
   - Then try the full `server.py`

4. **Error Logs**:
   - Check the Claude Desktop logs for any errors
   - The server outputs diagnostic information to stderr that should appear in the logs

5. **Python Version**:
   - Make sure you're using Python 3.8 or newer
   - Check your Python version with `python --version`

6. **Path Issues**:
   - Make sure the path to server.py in your Claude Desktop config is absolute
   - Example: `/Users/username/projects/claude-lmstudio-bridge/server.py`
