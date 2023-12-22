@echo off

:: Download the installer
powershell -Command "Start-BitsTransfer -Source https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"

:: Wait for download completion
:check_download
if not exist python-installer.exe goto :check_download

:: Install Python silently
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

:: Check if Python is installed and in PATH
where python
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH.
    pause
) else (
    echo Python installed successfully and added to PATH!
    pause
)