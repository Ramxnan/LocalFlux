@echo off
setlocal

REM Change to the directory where the script is located
cd /d %~dp0

REM Set the virtual environment name
set VENV_NAME=localflux_venv

REM Set the path to the local Python executable
set PYTHON_DIR=%cd%\python
set PYTHON_PATH=%PYTHON_DIR%\python.exe

REM Check if local Python is installed
echo Checking if Python is installed...
if exist "%PYTHON_PATH%" (
    echo Local Python is already installed at %PYTHON_PATH%
    echo ----------------------------------------
) else (
    echo Local Python is not installed, installing now...
    echo ----------------------------------------

    REM Download the full Python installer
    echo Downloading Python installer...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
    if %errorlevel% neq 0 (
        echo Failed to download Python installer
        pause
        goto end
    )
    echo Python installer downloaded
    echo ----------------------------------------

    echo creating python directory...
    mkdir python

    REM Run Python installer with target directory as the local folder
    echo Installing Python...
    echo Navigate to the python directory in LocalFlux folder and run the installer
    python-installer.exe InstallAllUsers=0 TargetDir=%PYTHON_DIR% PrependPath=0 Include_test=0
    if %errorlevel% neq 0 (
        echo Failed to install Python
        pause
        goto end
    )
    echo Python installed to the 'python' directory at %PYTHON_PATH%
    echo ----------------------------------------

)


REM Check if virtual environment exists
if exist "%VENV_NAME%" (
    echo Virtual environment already exists at %VENV_NAME%
    echo ----------------------------------------
) else (
    echo Virtual environment does not exist, creating now...
    "%PYTHON_PATH%" -m venv "%VENV_NAME%"
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment
        pause
        goto end
    )
    echo Virtual environment created at %VENV_NAME%
    echo ----------------------------------------
)

REM Activate the virtual environment
call "%VENV_NAME%"\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment
    pause
    goto end
)

REM Upgrade pip
echo Upgrading pip...
%VENV_NAME%\Scripts\python.exe -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Failed to upgrade pip
    pause
    goto end
)
echo ----------------------------------------

REM Install required packages
echo Installing required packages...
%VENV_NAME%\Scripts\pip.exe install -r requirements.txt
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
%VENV_NAME%\Scripts\python.exe manage.py runserver
if %errorlevel% neq 0 (
    echo Failed to start Django server
    pause
    goto end
)
echo ----------------------------------------

:end
endlocal
pause
