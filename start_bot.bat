@echo off
setlocal
title Antigravity Telegram Bot Server
color 0A

echo ========================================================
echo        ANTIGRAVITY TELEGRAM CONTROLLER SERVER
echo ========================================================
echo.

cd /d "%~dp0"

:: Set UTF-8 encoding
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: Uu tien thu muc cai dat Python thuc vao dau PATH (tranh WindowsApps App Execution Alias)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python313;%LOCALAPPDATA%\Programs\Python\Python313\Scripts;%PATH%"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python310;%LOCALAPPDATA%\Programs\Python\Python310\Scripts;%PATH%"
)

:: Xac dinh lenh Python kha dung
set "PYTHON_CMD="

:: 1. Kiem tra python tren PATH (sau khi da prepend)
python -c "import sys" >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)

:: 2. Kiem tra qua Python Launcher (py -3 hoac py)
py -3 -c "import sys" >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
    goto :python_found
)

py -c "import sys" >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_found
)

:: 3. Kiem tra truc tiep cac duong dan mac dinh
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
) do (
    if exist %%P (
        %%P -c "import sys" >nul 2>nul
        if not errorlevel 1 (
            set "PYTHON_CMD=%%P"
            goto :python_found
        )
    )
)

echo [ERROR] Khong tim thay Python tren he thong hoac bi xung dot voi Windows App Execution Alias!
echo Vui long cai dat Python 3.10 tro len tai https://www.python.org/ (nho tich Add python.exe to PATH).
echo Neu da cai dat, vui long tat App Execution Aliases trong Windows Settings:
echo Settings ^> Apps ^> Advanced app settings ^> App execution aliases (tat python.exe va python3.exe)
goto :end

:python_found
:: Install requirements
echo [*] Kiem tra thu vien phu thuoc...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [CANH BAO] Khong the tu dong cai dat thu vien phu thuoc qua pip.
)

:: Tu dong dung cac phien bot cu de tranh loi 409 Conflict
echo [*] Kiem tra va dong cac tien trinh bot cu...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $PID -and $_.CommandLine -like '*bot.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo [*] Dang khoi dong Telegram Bot...
echo.
%PYTHON_CMD% bot.py

:end
echo.
echo ========================================================
echo Nhan phim bat ky de thoat...
echo ========================================================
pause
