@echo off
cd /d C:\xampp\htdocs\ask_buddy\scripts
start /min cmd /c flask run
echo %ERRORLEVEL% > flask_pid.txt