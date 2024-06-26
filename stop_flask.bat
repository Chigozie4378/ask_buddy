@echo off
set /p FLASK_PID=<C:\xampp\htdocs\ask_buddy\flask_pid.txt
taskkill /PID %FLASK_PID% /F
