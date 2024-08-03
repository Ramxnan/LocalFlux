@echo off
setlocal

REM Change to the directory where the script is located
cd /d %~dp0

REM Set the path to the local Python executable
set PYTHON_DIR=%cd%\python
set PYTHON_PATH=%PYTHON_DIR%\python.exe

REM Check if local Python is installed
echo Checking if Python is installed...
if exist "%PYTHON_PATH%" (
    echo Local Python is already installed at %PYTHON_PATH%
    echo ----------------------------------------
) else (
    echo Embedded Python is not found, please ensure the python folder exists in the repository.
    pause
    goto end
)

REM Install required packages
echo Installing required packages...
"%PYTHON_DIR%"\python.exe -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install required packages
    pause
    goto end
)
echo Required packages installed
echo ----------------------------------------

REM Run the Django server
echo Running the Django application...
start "" "http://127.0.0.1:8000"
"%PYTHON_DIR%"\python.exe manage.py runserver
if %errorlevel% neq 0 (
    echo Failed to start Django server
    pause
    goto end
)
echo ----------------------------------------

:end
endlocal
pause
