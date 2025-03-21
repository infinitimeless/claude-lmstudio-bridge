@echo off
REM setup.bat - Simplified setup script for Claude-LMStudio Bridge

echo === Claude-LMStudio Bridge Setup ===
echo.

REM Create and activate virtual environment
if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
  echo ✓ Created virtual environment
) else (
  echo ✓ Virtual environment already exists
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo ✓ Installed dependencies

REM Create default configuration
if not exist .env (
  echo Creating default configuration...
  (
    echo LMSTUDIO_HOST=127.0.0.1
    echo LMSTUDIO_PORT=1234
    echo DEBUG=false
  ) > .env
  echo ✓ Created .env configuration file
) else (
  echo ✓ Configuration file already exists
)

REM Check if LM Studio is running
set PORT_CHECK=0
netstat -an | findstr "127.0.0.1:1234" > nul && set PORT_CHECK=1
if %PORT_CHECK%==1 (
  echo ✓ LM Studio is running on port 1234
) else (
  echo ⚠ LM Studio does not appear to be running on port 1234
  echo   Please start LM Studio and enable the API server (Settings ^> API Server)
)

echo.
echo ✓ Setup complete!
echo.
echo To start the bridge, run:
echo   venv\Scripts\activate.bat ^&^& python server.py
echo.
echo To configure with Claude Desktop:
echo 1. Open Claude Desktop preferences
echo 2. Navigate to the 'MCP Servers' section
echo 3. Add a new MCP server with the following configuration:
echo    - Name: lmstudio-bridge
echo    - Command: cmd.exe
echo    - Arguments: /c %CD%\run_server.bat
echo.
echo Make sure LM Studio is running with API server enabled on port 1234.

REM Keep the window open
pause
