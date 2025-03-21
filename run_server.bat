@echo off
SETLOCAL

REM Configuration - Auto-detect Python path
IF "%PYTHON_PATH%"=="" (
  FOR /F "tokens=*" %%i IN ('where python') DO (
    SET PYTHON_PATH=%%i
    GOTO :found_python
  )
  
  echo ERROR: Python not found in your PATH 1>&2
  echo Please install Python first and make sure it's in your PATH 1>&2
  EXIT /B 1
  
  :found_python
)

REM Print current environment details
echo Current directory: %CD% 1>&2
echo Using Python at: %PYTHON_PATH% 1>&2

REM Check if Python exists at the specified path
IF NOT EXIST "%PYTHON_PATH%" (
  echo ERROR: Python not found at %PYTHON_PATH% 1>&2
  echo Please install Python or set the correct path in this script. 1>&2
  EXIT /B 1
)

REM Check if mcp is installed, if not, try to install it
"%PYTHON_PATH%" -c "import mcp" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo MCP package not found, attempting to install... 1>&2
  
  REM Try to install using python -m pip
  "%PYTHON_PATH%" -m pip install "mcp[cli]" httpx
  IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install MCP package. Please install manually with: 1>&2
    echo "%PYTHON_PATH%" -m pip install "mcp[cli]" httpx 1>&2
    EXIT /B 1
  )
  
  REM Check if installation was successful
  "%PYTHON_PATH%" -c "import mcp" >nul 2>&1
  IF %ERRORLEVEL% NEQ 0 (
    echo MCP package was installed but still can't be imported. 1>&2
    echo This might be due to a Python path issue. 1>&2
    EXIT /B 1
  )
)

REM Check if httpx is installed
"%PYTHON_PATH%" -c "import httpx" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo httpx package not found, attempting to install... 1>&2
  "%PYTHON_PATH%" -m pip install httpx
  IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install httpx package. 1>&2
    EXIT /B 1
  )
)

REM Check if dotenv is installed (for .env file support)
"%PYTHON_PATH%" -c "import dotenv" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo python-dotenv package not found, attempting to install... 1>&2
  "%PYTHON_PATH%" -m pip install python-dotenv
  IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install python-dotenv package. 1>&2
    EXIT /B 1
  )
)

REM Check if virtual environment exists and use it if it does
IF EXIST "venv\Scripts\python.exe" (
  echo Using Python from virtual environment 1>&2
  SET PYTHON_PATH=%CD%\venv\Scripts\python.exe
  echo Updated Python path to: %PYTHON_PATH% 1>&2
)

REM Attempt to check if LM Studio is running before starting
netstat -an | findstr "127.0.0.1:1234" >nul
IF %ERRORLEVEL% NEQ 0 (
  echo WARNING: LM Studio does not appear to be running on port 1234 1>&2
  echo Please make sure LM Studio is running with the API server enabled 1>&2
) ELSE (
  echo ✓ LM Studio API server appears to be running on port 1234 1>&2
)

REM Run the server script
echo Starting server.py with %PYTHON_PATH%... 1>&2
"%PYTHON_PATH%" server.py

ENDLOCAL
