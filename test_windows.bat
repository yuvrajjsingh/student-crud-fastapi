@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run start_windows.bat once first to install project dependencies.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m pytest -v
pause
