@echo off
setlocal

REM Change to the directory where the script is located
cd /d %~dp0

REM Check if this is a Git repository before running git pull
if exist ".git" (
    echo Updating the repository...
    git pull
    if %errorlevel% neq 0 (
        echo Failed to update the repository
        pause
        goto end
    )
) else (
    echo No .git directory found. Skipping git pull.
)


REM Set the path to the local Python executable
set PYTHON_DIR=%cd%\python
set PYTHON_PATH=%PYTHON_DIR%\python.exe

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

endlocal
pause
