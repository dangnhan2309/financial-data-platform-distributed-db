@echo off
title FastAPI Server - Vietfarm_API
echo ========================================
echo Dang khoi dong FastAPI Server...
echo ========================================

:: 1. Xac dinh duong dan thu muc hien tai cua script
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

:: 2. Chon Python executable (uu tien .venv o thu muc goc)
set "PYTHON_EXE="

if exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "%SCRIPT_DIR%venv\Scripts\python.exe" set "PYTHON_EXE=%SCRIPT_DIR%venv\Scripts\python.exe"

if not defined PYTHON_EXE (
    echo [LOI] Khong tim thay python.exe trong .venv hoac venv
    pause
    exit /b 1
)

:: 3. Di chuyen den thu muc du an
cd /d "%SCRIPT_DIR%"

:: 4. Mo trang Swagger de test CRUD
start "" "http://127.0.0.1:8011/docs"

:: 5. Chay uvicorn
"%PYTHON_EXE%" -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8011

echo..
echo Server da dung.
pause