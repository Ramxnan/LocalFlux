@echo off
setlocal

REM Set the virtual environment name
set VENV_NAME=localflux_venv

REM Set the download URL
set DOWNLOAD_URL=https://github.com/Ramxnan/LocalFlux/archive/refs/tags/latest.zip

REM Set the download and extract paths
set ZIP_FILE=LocalFlux-latest.zip
set EXTRACT_DIR=LocalFlux-latest

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

@REM REM Create the extraction directory
@REM if not exist %EXTRACT_DIR% (
@REM     mkdir %EXTRACT_DIR%
@REM ) else (
@REM     echo Extraction directory already exists, please delete the directory and run the script again
@REM     echo ----------------------------------------
@REM     pause
@REM     exit
@REM )

REM Download the zip file
echo Downloading the zip file...
curl -L -o %ZIP_FILE% %DOWNLOAD_URL%
echo Zip file downloaded
echo ----------------------------------------

REM Extract the zip file into the extraction directory
echo Extracting the zip file...
tar -xf %ZIP_FILE%
echo Zip file extracted
echo ----------------------------------------


REM Change to the extracted directory
cd %EXTRACT_DIR%

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

REM Go back to the parent directory and delete the setup script
cd ..
del %ZIP_FILE%

REM Schedule deletion of the script and the zip file
echo $path = "%~f0" > delete_me.ps1
echo Start-Sleep -Seconds 2 >> delete_me.ps1
echo Remove-Item $path -Force >> delete_me.ps1

REM Run the PowerShell script to delete the batch file with appropriate execution policy
start powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File delete_me.ps1

endlocal
pause

endlocal
pause
