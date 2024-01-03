@echo off
title Seconb Colorbot Installer!
echo Installing requirements for the colorbot... make sure Python is downloaded and you checked "Add Python.exe to PATH" before installing!
pip install keyboard Pillow mss configparser opencv-python numpy colorama pywin32 pygetwindow
echo Requirements installed! If aimsource.py crashes, manually run "pip install keyboard Pillow mss configparser opencv-python numpy colorama pywin32 pygetwindow".
pause
