@echo off
SETLOCAL

echo === Claude-LMStudio Bridge Setup ===
echo This script will prepare the environment for use with Claude Desktop
echo.

:: Try to install MCP globally to ensure it's available
echo Installing MCP package globally...
python -m pip install "mcp[cli]" httpx

:: Check if installation was successful
python -c "import mcp" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo X Failed to install MCP package. Please check your Python installation.
  EXIT /B 1
) ELSE (
  echo ✓ MCP package installed successfully
)

:: Create virtual environment if it doesn't exist
IF NOT EXIST venv (
  echo Creating virtual environment...
  python -m venv venv
  echo ✓ Created virtual environment
  
  :: Activate and install dependencies
  CALL venv\Scripts\activate.bat
  python -m pip install -r requirements.txt
  echo ✓ Installed dependencies in virtual environment
) ELSE (
  echo ✓ Virtual environment already exists
)

:: Display configuration instructions
echo.
echo === Configuration Instructions ===
echo 1. Open Claude Desktop preferences
echo 2. Navigate to the 'MCP Servers' section
echo 3. Add a new MCP server with the following configuration:
echo.
echo    Name: lmstudio-bridge
echo    Command: cmd.exe
echo    Arguments: /c %CD%\run_server.bat
echo.
echo 4. Start LM Studio and ensure the API server is running
echo 5. Restart Claude Desktop
echo.
echo Setup complete! You can now use the LMStudio bridge with Claude Desktop.

ENDLOCAL