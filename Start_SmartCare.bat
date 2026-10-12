@echo off
title SmartCare App Launcher
echo ==========================================
echo Starting SmartCare Hospital System...
echo ==========================================

:: Start the Server in a new window
start "SmartCare Server" cmd /k "cd server & python queue_server.py"

:: Wait 2 seconds to let the server fully boot up
timeout /t 2 /nobreak > NUL

:: Start the Receptionist GUI in a new window
start "Receptionist Dashboard" cmd /k "cd clients & python receptionist_gui.py"

:: Start the Doctor GUI in a new window
start "Doctor Dashboard" cmd /k "cd clients & python doctor_gui.py"

exit