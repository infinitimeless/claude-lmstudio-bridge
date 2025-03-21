# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio.

## Overview

This tool allows Claude to interact with your local LLMs running in LM Studio, providing:

- Access to list all available models in LM Studio
- The ability to generate text using your local LLMs
- Support for chat completions through your local models
- A health check tool to verify connectivity with LM Studio

## Prerequisites

- [Claude Desktop](https://claude.ai/desktop) with MCP support
- [LM Studio](https://lmstudio.ai/) installed and running locally with API server enabled
- Python 3.8+ installed

## Quick Start (Recommended)

### For macOS/Linux:

1. Clone the repository
```bash
git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
cd claude-lmstudio-bridge
```

2. Run the setup script
```bash
chmod +x setup.sh
./setup.sh
```

3. Follow the setup script's instructions to configure Claude Desktop

### For Windows:

1. Clone the repository
```cmd
git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
cd claude-lmstudio-bridge
```

2. Run the setup script
```cmd
setup.bat
```

3. Follow the setup script's instructions to configure Claude Desktop

## Manual Setup

If you prefer to set things up manually:

1. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages
```bash
pip install -r requirements.txt
```

3. Configure Claude Desktop:
   - Open Claude Desktop preferences
   - Navigate to the 'MCP Servers' section
   - Add a new MCP server with the following configuration:
     - **Name**: lmstudio-bridge
     - **Command**: /bin/bash (on macOS/Linux) or cmd.exe (on Windows)
     - **Arguments**: 
       - macOS/Linux: /path/to/claude-lmstudio-bridge/run_server.sh
       - Windows: /c C:\path\to\claude-lmstudio-bridge\run_server.bat

## Usage with Claude

After setting up the bridge, you can use the following commands in Claude:

1. Check the connection to LM Studio:
```
Can you check if my LM Studio server is running?
```

2. List available models:
```
List the available models in my local LM Studio
```

3. Generate text with a local model:
```
Generate a short poem about spring using my local LLM
```

4. Send a chat completion:
```
Ask my local LLM: "What are the main features of transformers in machine learning?"
```

## Troubleshooting

### Diagnosing LM Studio Connection Issues

Use the included debugging tool to check your LM Studio connection:

```bash
python debug_lmstudio.py
```

For more detailed tests:
```bash
python debug_lmstudio.py --test-chat --verbose
```

### Common Issues

**"Cannot connect to LM Studio API"**
- Make sure LM Studio is running
- Verify the API server is enabled in LM Studio (Settings > API Server)
- Check that the port (default: 1234) matches what's in your .env file

**"No models are loaded"**
- Open LM Studio and load a model
- Verify the model is running successfully

**"MCP package not found"**
- Try reinstalling: `pip install "mcp[cli]" httpx python-dotenv`
- Make sure you're using Python 3.8 or later

**"Claude can't find the bridge"**
- Check Claude Desktop configuration
- Make sure the path to run_server.sh or run_server.bat is correct and absolute
- Verify the server script is executable: `chmod +x run_server.sh` (on macOS/Linux)

## Advanced Configuration

You can customize the bridge behavior by creating a `.env` file with these settings:

```
LMSTUDIO_HOST=127.0.0.1
LMSTUDIO_PORT=1234
DEBUG=false
```

Set `DEBUG=true` to enable verbose logging for troubleshooting.

## License

MIT
