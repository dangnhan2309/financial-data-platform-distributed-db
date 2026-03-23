@echo off
title FastAPI Server - HD_API
echo ========================================
echo Dang khoi dong FastAPI Server...
echo ========================================

:: 1. Di chuyen den thu muc du an
cd /d F:\financial-data-platform-distributed-db\HD_API

:: 2. Kich hoat moi truong ao (Dung 'call' de tiep tuc script)
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo [LOI] Khong tim thay moi truong ao venv!
    pause
    exit
)

:: 3. Chay uvicorn
:: Luu y: api.main tuong ung voi file F:\...\HD_API\api\main.py
uvicorn api.main:app --reload --host localhost --port 8000

echo.
echo Server da dung.
pause