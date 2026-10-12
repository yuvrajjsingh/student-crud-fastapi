@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  set PYTHON=python
) else (
  set PYTHON=py
)
if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating virtual environment...
  %PYTHON% -m venv .venv
  if errorlevel 1 goto :error
)
echo [2/3] Installing required packages...
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto :error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error
echo [3/3] Starting the API. Keep this window open.
echo Swagger documentation: http://127.0.0.1:8000/docs
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
if errorlevel 1 goto :error
goto :eof
:error
echo.
echo Something went wrong. Check that Python 3.10+ is installed and available in PATH.
pause
exit /b 1
