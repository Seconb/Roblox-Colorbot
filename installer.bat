@echo off
title Installing Python...

:: Check if Python 3.11 is installed
python --version | findstr "3.11"
if %errorlevel%==0 (
    echo Python 3.11 is already installed
) else (
    echo Python 3.11 is not installed. Downloading...
    certutil -urlcache -split -f "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe" python-3.11.exe
    echo Installing Python 3.11...
    start /wait python-3.11.exe /quiet InstallAllUsers=1 Include_test=0
    del python-3.11.exe
    echo Python 3.11 has been installed
)

:: Change directory to the current directory
cd /d "%~dp0"

:: Install requirements
echo Installing Requirements...

:: List of packages to install
set PACKAGES=keyboard Pillow mss configparser opencv-python numpy colorama pywin32

:: Install each package silently
for %%i in (%PACKAGES%) do (
    echo Installing %%i...
    python -m pip install %%i --quiet
)

echo Requirements installed! Ready for use!
pause
