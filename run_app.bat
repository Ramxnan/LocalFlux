@echo off
setlocal

REM Set the virtual environment name
set VENV_NAME=localflux_venv

REM Check if Python is installed
echo Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed, installing now...
    echo ---------------------------------------- 

    REM Install Python
    echo Installing Python...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
    echo Python installer downloaded, running installer...
    echo ----------------------------------------

    REM Run Python installer
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo Python installed successfully
    echo ----------------------------------------

    REM Remove Python installer
    del python-installer.exe
    echo Python installer deleted
    echo ----------------------------------------
) else (
    echo Python is already installed
    echo ----------------------------------------
)

REM Check if virtual environment exists
if exist %VENV_NAME% (
    echo Virtual environment already exists
) else (
    echo Virtual environment does not exist, creating now...
    python -m venv %VENV_NAME%
    echo Virtual environment created
)

REM Activate the virtual environment
call %VENV_NAME%\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo ----------------------------------------

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
echo Required packages installed
echo ----------------------------------------

REM Run the Django server
echo Running the Django application...

REM Pause for 2 seconds
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8000"
python manage.py runserver
echo ----------------------------------------

endlocal
pause
