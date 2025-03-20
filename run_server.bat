@echo off
SETLOCAL

:: Print current environment details
echo Current directory: %CD% 1>&2
where python 2>nul || echo Python not in PATH 1>&2

:: Activate virtual environment if it exists
IF EXIST venv\Scripts\activate.bat (
  echo Activating virtual environment... 1>&2
  CALL venv\Scripts\activate.bat
  echo Activated Python: 1>&2
  where python 2>nul || echo Python not in PATH 1>&2
)

:: Check if mcp is installed, if not, try to install it
python -c "import mcp" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo MCP package not found, attempting to install... 1>&2
  
  :: Try to install using python -m pip instead of direct pip call
  python -m pip install "mcp[cli]" httpx
  IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install MCP package. Please install manually with: 1>&2
    echo python -m pip install "mcp[cli]" 1>&2
    
    :: Additional guidance for Claude Desktop startup integration
    echo. 1>&2
    echo For Claude Desktop Startup Integration: 1>&2
    echo 1. Open Command Prompt and navigate to this directory 1>&2
    echo 2. Run: python -m pip install "mcp[cli]" httpx 1>&2
    EXIT /B 1
  )
  
  :: Check if installation was successful
  python -c "import mcp" >nul 2>&1
  IF %ERRORLEVEL% NEQ 0 (
    echo MCP package was installed but still can't be imported. 1>&2
    echo This might be due to a Python path issue. 1>&2
    EXIT /B 1
  )
)

:: Run the server script
echo Starting server.py with Python from %CD% 1>&2
python server.py

ENDLOCAL