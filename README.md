# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio.

## ⚠️ Important Setup Step Required

Before using this bridge, you **must** configure the Python path in the wrapper scripts:

### For macOS/Linux Users:
1. Find your Python path by running `which python3` in Terminal
2. Edit `run_server.sh` and update the `PYTHON_PATH` variable with your path:
   ```bash
   # Change this to your actual Python path!
   PYTHON_PATH="/usr/local/bin/python3"
   ```
3. Make the wrapper executable:
   ```bash
   chmod +x run_server.sh
   ```

### For Windows Users:
1. Find your Python path by running `where python` in Command Prompt
2. Edit `run_server.bat` and update the `PYTHON_PATH` variable with your path:
   ```batch
   :: Change to your actual Python path!
   SET PYTHON_PATH=C:\Python311\python.exe
   ```

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

2. **Important:** Update the Python path in the wrapper script as described above

3. Install the MCP package:
   ```bash
   # macOS/Linux
   python3 -m pip install "mcp[cli]" httpx
   
   # Windows
   python -m pip install "mcp[cli]" httpx
   ```

4. Start LM Studio and ensure the API server is running (in Settings > API Server)

5. Configure Claude Desktop to use this MCP server (see Configuration section below)

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

**"Python not found" or Script Errors**

The most common issue is an incorrect Python path in the wrapper scripts. To fix this:

1. Open a terminal or command prompt
2. Run `which python3` (macOS/Linux) or `where python` (Windows)
3. Copy the full path to your Python executable 
4. Update the `PYTHON_PATH` variable in `run_server.sh` or `run_server.bat`
5. Make the script executable: `chmod +x run_server.sh` (macOS/Linux only)
6. Restart Claude Desktop

**"No module named 'mcp'"**

If you see this error, you need to install the MCP package in the same Python environment:

```bash
# Use your Python path from the wrapper script
/path/to/your/python -m pip install "mcp[cli]" httpx
```

**Connection Issues with LM Studio**

- Make sure LM Studio is running
- Ensure the API server is enabled (in Settings > API Server)
- Default API server address is http://localhost:1234

For more troubleshooting steps, see [INSTALLATION.md](INSTALLATION.md).
