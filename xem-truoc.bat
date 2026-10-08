@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if "%~1"=="" (
  echo Keo tha 1 file kich ban .json vao file nay de xem truoc.
) else (
  python make_video.py "%~1" --preview --force
)
pause
