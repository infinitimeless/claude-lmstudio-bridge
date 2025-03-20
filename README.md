# Claude-LMStudio Bridge

An MCP server that bridges Claude with local LLMs running in LM Studio.

## Easy Installation

### Option 1: Automated Installation (Recommended)

Run the installation script for your platform:

#### For macOS/Linux:
```bash
# Clone the repository
git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
cd claude-lmstudio-bridge

# Make the installer executable and run it
chmod +x install.sh
./install.sh
```

#### For Windows:
```bash
# Clone the repository
git clone https://github.com/infinitimeless/claude-lmstudio-bridge.git
cd claude-lmstudio-bridge

# Run the installer
install.bat
```

The installation script will:
1. Find your Python installation automatically
2. Configure the wrapper scripts with the correct Python path
3. Install the required Python packages
4. Update your Claude Desktop configuration file

After installation, restart Claude Desktop to use the bridge.

### Option 2: Manual Installation

If the automated installation doesn't work, you can configure the bridge manually:

#### 1. Update Python Path in Wrapper Scripts

##### For macOS/Linux:
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

##### For Windows:
1. Find your Python path by running `where python` in Command Prompt
2. Edit `run_server.bat` and update the `PYTHON_PATH` variable with your path:
   ```batch
   :: Change to your actual Python path!
   SET PYTHON_PATH=C:\Python311\python.exe
   ```

#### 2. Install Required Packages

Use your Python path to install the required packages:

```bash
# macOS/Linux
/path/to/your/python -m pip install "mcp[cli]" httpx

# Windows
C:\path\to\your\python.exe -m pip install "mcp[cli]" httpx
```

#### 3. Configure Claude Desktop

Add this server to your Claude Desktop configuration:

##### For macOS/Linux:
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

##### For Windows:
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

## Features

- List available LLM models in LM Studio
- Generate text using local LLMs
- Send chat completions to local LLMs

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
