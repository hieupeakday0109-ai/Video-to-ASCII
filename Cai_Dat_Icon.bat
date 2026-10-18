@echo off
title Cài đặt Video to ASCII Player
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================
echo   🎬 CÀI ĐẶT VIDEO TO ASCII PLAYER RA MÀN HÌNH CHÍNH
echo ======================================================
echo.

:: 1. Kiểm tra Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] Máy tính chưa cài đặt Python hoặc chưa bật PATH.
    echo     Vui lòng tải và cài đặt Python tại: https://www.python.org/
    echo     (Lưu ý: Tích chọn "Add python.exe to PATH" khi cài đặt)
    echo.
    pause
    exit /b 1
)

:: 2. Cài đặt các thư viện
echo [*] Đang kiểm tra và cài đặt thư viện cần thiết...
python -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo [*] Thử cài đặt trực tiếp:
    python -m pip install -r requirements.txt
)

:: 3. Tạo icon shortcut ra Desktop
echo [*] Đang tạo biểu tượng ra màn hình Desktop...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_desktop_shortcut.ps1"

echo.
echo ======================================================
echo   🎉 CÀI ĐẶT HOÀN TẤT!
echo   Biểu tượng "Video to ASCII Player" đã có trên Desktop!
echo ======================================================
echo.

set /p choice="👉 Bạn có muốn mở ứng dụng ngay bây giờ không? (Y/n): "
if /i "%choice%"=="n" goto end

start "" pythonw "%~dp0gui_launcher.py"

:end
