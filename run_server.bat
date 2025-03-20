@echo off
SETLOCAL

:: Activate virtual environment if it exists
IF EXIST venv\Scripts\activate.bat (
  echo Activating virtual environment... 1>&2
  CALL venv\Scripts\activate.bat
)

:: Check if mcp is installed, if not, try to install it
python -c "import mcp" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo MCP package not found, attempting to install... 1>&2
  pip install "mcp[cli]" httpx
  
  :: Check if installation was successful
  python -c "import mcp" >nul 2>&1
  IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install MCP package. Please install manually with: 1>&2
    echo pip install "mcp[cli]" 1>&2
    EXIT /B 1
  )
)

:: Run the server script
echo Starting server.py with %PYTHON% from %CD% 1>&2
python server.py

ENDLOCAL