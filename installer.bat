@echo off
setlocal

REM Change to the directory where the script is located
cd /d %~dp0

REM Set the virtual environment name
set VENV_NAME=localflux_venv

REM Set the download URL
REM set DOWNLOAD_URL=https://github.com/Ramxnan/LocalFlux/archive/refs/tags/latest.zip
set DOWNLOAD_URL=https://github.com/Ramxnan/LocalFlux/releases/download/latest/LocalFluxSetup.zip

REM Set the download and extract paths
set ZIP_FILE=LocalFlux-latest.zip
set EXTRACT_DIR=LocalFlux

REM Create the extraction directory
if not exist %EXTRACT_DIR% (
    mkdir %EXTRACT_DIR%
) else (
    echo Extraction directory already exists, please delete the directory and run the script again
    echo ----------------------------------------
    pause
    exit
)

REM Download the zip file
echo Downloading the zip file...
curl -L -o %ZIP_FILE% %DOWNLOAD_URL%
echo Zip file downloaded
echo ----------------------------------------

REM Extract the zip file into the extraction directory
echo Extracting the zip file...
tar -xf %ZIP_FILE% -C %EXTRACT_DIR%
echo Zip file extracted
echo ----------------------------------------


REM delete the setup script
del %ZIP_FILE%

REM Schedule deletion of the script and the zip file
echo $path = "%~f0" > delete_me.ps1
echo Start-Sleep -Seconds 2 >> delete_me.ps1
echo Remove-Item $path -Force >> delete_me.ps1

REM Run the PowerShell script to delete the batch file with appropriate execution policy
start powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File delete_me.ps1

endlocal
pause
