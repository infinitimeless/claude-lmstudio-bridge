@echo off
SETLOCAL

:: Configuration - CHANGE THESE TO MATCH YOUR SYSTEM
:: Find your Python path with "where python" in command prompt
SET PYTHON_PATH=C:\Python311\python.exe
:: Change to your actual Python path!

:: Print current environment details
echo Current directory: %CD% 1>&2
echo Using Python at: %PYTHON_PATH% 1>&2

:: Check if Python exists at the specified path
IF NOT EXIST "%PYTHON_PATH%" (
  echo ERROR: Python not found at %PYTHON_PATH% 1>&2
  echo Please edit run_server.bat and set PYTHON_PATH to the correct location of your Python installation 1>&2
  echo You can find this by running 'where python' in a command prompt 1>&2
  EXIT /B 1
)

:: Check if mcp is installed, if not, try to install it
"%PYTHON_PATH%" -c "import mcp" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo MCP package not found, attempting to install... 1>&2
  
  :: Try to install using python -m pip
  "%PYTHON_PATH%" -m pip install "mcp[cli]" httpx
  IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install MCP package. Please install manually with: 1>&2
    echo "%PYTHON_PATH%" -m pip install "mcp[cli]" 1>&2
    
    :: Additional guidance for Claude Desktop startup integration
    echo. 1>&2
    echo For Claude Desktop Startup Integration: 1>&2
    echo 1. Open Command Prompt and navigate to this directory 1>&2
    echo 2. Run: "%PYTHON_PATH%" -m pip install "mcp[cli]" httpx 1>&2
    EXIT /B 1
  )
  
  :: Check if installation was successful
  "%PYTHON_PATH%" -c "import mcp" >nul 2>&1
  IF %ERRORLEVEL% NEQ 0 (
    echo MCP package was installed but still can't be imported. 1>&2
    echo This might be due to a Python path issue. 1>&2
    EXIT /B 1
  )
)

:: Run the server script
echo Starting server.py with %PYTHON_PATH% from %CD% 1>&2
"%PYTHON_PATH%" server.py

ENDLOCAL