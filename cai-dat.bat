@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Cai dat lan dau ===
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
echo.
echo Xong! Bay gio co the chay tao-video.bat
pause
