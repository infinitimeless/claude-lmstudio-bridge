@echo off
echo ===== Claude-LMStudio Bridge Installer =====
echo This will configure the bridge to work with Claude Desktop
echo.

:: Find Python location
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_PATH=%%i
    goto :found_python
)

echo X ERROR: Python not found in your PATH
echo Please install Python first and try again
exit /b 1

:found_python
echo v Found Python at: %PYTHON_PATH%

:: Update the run_server.bat script with the correct Python path
echo Updating run_server.bat with Python path...
powershell -Command "(Get-Content run_server.bat) -replace 'SET PYTHON_PATH=.*', 'SET PYTHON_PATH=%PYTHON_PATH%' | Set-Content run_server.bat"

:: Install required packages
echo Installing required Python packages...
"%PYTHON_PATH%" -m pip install "mcp[cli]" httpx

:: Check if installation was successful
"%PYTHON_PATH%" -c "import mcp" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X ERROR: Failed to install MCP package
    echo Try running manually: "%PYTHON_PATH%" -m pip install "mcp[cli]" httpx
    exit /b 1
)

echo v MCP package installed successfully

:: Get full path to the run_server.bat script
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%run_server.bat
echo Script path: %SCRIPT_PATH%

:: Create or update Claude Desktop config
set CONFIG_DIR=%APPDATA%\Claude
set CONFIG_FILE=%CONFIG_DIR%\claude_desktop_config.json

if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

if exist "%CONFIG_FILE%" (
    :: Backup existing config
    copy "%CONFIG_FILE%" "%CONFIG_FILE%.backup" >nul
    echo Created backup of existing config at %CONFIG_FILE%.backup
    
    :: Create new config file - we'll use a simple approach for Windows
    echo {> "%CONFIG_FILE%"
    echo   "mcpServers": {>> "%CONFIG_FILE%"
    echo     "lmstudio-bridge": {>> "%CONFIG_FILE%"
    echo       "command": "cmd.exe",>> "%CONFIG_FILE%"
    echo       "args": [>> "%CONFIG_FILE%"
    echo         "/c",>> "%CONFIG_FILE%"
    echo         "%SCRIPT_PATH:\=\\%">> "%CONFIG_FILE%"
    echo       ]>> "%CONFIG_FILE%"
    echo     }>> "%CONFIG_FILE%"
    echo   }>> "%CONFIG_FILE%"
    echo }>> "%CONFIG_FILE%"
) else (
    :: Create new config file
    echo {> "%CONFIG_FILE%"
    echo   "mcpServers": {>> "%CONFIG_FILE%"
    echo     "lmstudio-bridge": {>> "%CONFIG_FILE%"
    echo       "command": "cmd.exe",>> "%CONFIG_FILE%"
    echo       "args": [>> "%CONFIG_FILE%"
    echo         "/c",>> "%CONFIG_FILE%"
    echo         "%SCRIPT_PATH:\=\\%">> "%CONFIG_FILE%"
    echo       ]>> "%CONFIG_FILE%"
    echo     }>> "%CONFIG_FILE%"
    echo   }>> "%CONFIG_FILE%"
    echo }>> "%CONFIG_FILE%"
)

echo v Updated Claude Desktop configuration at %CONFIG_FILE%

echo.
echo v Installation complete!
echo Please restart Claude Desktop to use the LMStudio bridge
echo.
echo If you encounter any issues, edit run_server.bat to check settings
echo or refer to the README.md for troubleshooting steps.

pause