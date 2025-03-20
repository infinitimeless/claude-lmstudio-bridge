# Installation Guide for Claude-LMStudio Bridge

This guide provides detailed instructions for setting up the Claude-LMStudio Bridge MCP server.

## Installing the MCP Python SDK

The primary issue users face is not having the MCP module installed properly. Here are different ways to install it:

### Using uv (Recommended)

`uv` is a modern Python package installer that's recommended for MCP development:

```bash
# Install uv if you don't have it
pip install uv

# Install the MCP SDK with CLI support
uv add "mcp[cli]"
```

### Using pip

Alternatively, you can use pip:

```bash
pip install "mcp[cli]"
```

## Verifying Installation

After installation, verify that the module is correctly installed:

```bash
python -c "import mcp; print(mcp.__version__)"
```

This should print the version of the MCP SDK if it's installed correctly.

## Ensuring the Correct Environment

Make sure you're using the correct Python environment:

1. If using a virtual environment, activate it before running your script:

   ```bash
   # Activate virtual environment
   source venv/bin/activate  # For Mac/Linux
   # or
   venv\Scripts\activate  # For Windows
   ```

2. Verify the Python path to ensure you're using the expected Python interpreter:

   ```bash
   which python  # On Mac/Linux
   where python  # On Windows
   ```

## Testing the Installation

Run the test script to verify your setup:

```bash
python test_mcp.py
```

If this works successfully, you should be ready to run the server.

## Common Issues and Solutions

1. **ModuleNotFoundError: No module named 'mcp'**
   - The MCP module isn't installed in your current Python environment
   - Solution: Install the MCP SDK as described above

2. **MCP installed but still getting import errors**
   - You might be running Python from a different environment
   - Solution: Check which Python is being used with `which python` and make sure your virtual environment is activated

3. **Error loading the server in Claude**
   - Make sure you're using absolute paths in your Claude Desktop configuration
   - Check that the server is executable and that Python has permission to access it
