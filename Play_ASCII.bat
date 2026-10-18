@echo off
title Video to ASCII Player
chcp 65001 >nul
cd /d "%~dp0"

:: Kiểm tra Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] Máy tính chưa cài đặt Python hoặc chưa thêm vào PATH.
    echo Vui lòng cài đặt Python tại https://www.python.org/
    pause
    exit /b
)

:: Nếu người dùng KÉO THẢ file video vào biểu tượng file .bat này (%1)
if not "%~1"=="" (
    python ascii_player.py "%~1"
    pause
    exit /b
)

:: Nếu click đúp mở file .bat
python ascii_player.py
pause
