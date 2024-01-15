@echo off
SETLOCAL EnableDelayedExpansion
chcp 65001

echo 檢查 Python 是否已安裝...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 未安裝
    exit /b
)
goto checkVenv

:askRemoveVenv
set /p REMOVE_VENV="是否要移除現有的venv並重新創建？[Y/N]"
if /i "%REMOVE_VENV%"=="Y" (
    rmdir /s /q venv
    goto CreateVenv
) else (
    echo 繼續使用現有的 venv
    goto ActivateEnv
)

:checkVenv
echo 檢查 venv 資料夾是否存在
if exist venv (
    echo 虛擬環境 venv 已存在
    goto askRemoveVenv
)


:CreateVenv
echo 創建 Python 虛擬環境...
python -m venv venv
if errorlevel 1 (
    echo 創建虛擬環境失敗
    exit /b
)

:ActivateEnv
echo 進入 Python 虛擬環境...
CALL venv\Scripts\activate.bat

echo 檢查 requirement.txt 是否存在並安裝...
if not exist requirement.txt (
    echo requirement.txt 不存在
    exit /b
)
python -m pip install -r requirement.txt
if errorlevel 1 (
    echo 安裝 requirements 失敗
    exit /b
)

echo 所有步驟完成，退出...
ENDLOCAL