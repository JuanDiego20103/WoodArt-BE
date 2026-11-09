@echo off
title WoodArt BACKEND (puerto 5000)
cd /d "%~dp0"
".venv\Scripts\python.exe" -m src.app
pause
