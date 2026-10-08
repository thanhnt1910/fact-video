@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if "%~1"=="" (
  echo Dang tao tat ca video chua lam trong thu muc scripts...
  python make_video.py scripts
) else (
  python make_video.py "%~1" %2 %3
)
pause
