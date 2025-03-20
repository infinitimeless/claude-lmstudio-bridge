# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio.

## Features

- List available LLM models in LM Studio
- Generate text using local LLMs
- Send chat completions to local LLMs

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Start LM Studio and ensure the API server is running (usually on port 1234)
6. Configure Claude Desktop to use this MCP server

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