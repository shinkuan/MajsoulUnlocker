@echo off
SETLOCAL EnableDelayedExpansion
chcp 65001

echo 檢查 venv\Scripts\activate.bat 是否存在
if not exist "venv\Scripts\activate.bat" (
    echo venv\Scripts\activate.bat 不存在
    exit /b
)

echo 啟動 venv 並進入 Python Venv
CALL venv\Scripts\activate.bat

echo 啟動 unlocker.py
python unlocker.py

echo 所有步驟完成，退出...
ENDLOCAL