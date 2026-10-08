@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
(
echo === STEP 1 uv ===
python -m pip install --upgrade uv
echo === STEP 2 venv python 3.12 ===
python -m uv venv .venv-tts --python 3.12 --allow-existing
echo === STEP 3 install vieneu ===
python -m uv pip install --python .venv-tts\Scripts\python.exe vieneu
echo === STEP 4 list voices ===
.venv-tts\Scripts\python.exe vieneu_tts.py --list
echo === STEP 5 samples ===
.venv-tts\Scripts\python.exe vieneu_tts.py --samples
echo === ALL DONE ===
) > cai-giong-doc.log 2>&1
