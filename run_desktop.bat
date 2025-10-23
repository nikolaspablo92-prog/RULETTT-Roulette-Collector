@echo off
REM ============================================
REM 🎰 RULETTT Desktop - Quick Launch
REM ============================================

echo.
echo ════════════════════════════════════════════
echo    RULETTT Desktop Application
echo ════════════════════════════════════════════
echo.

REM Проверка PyQt5
python -c "import PyQt5" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5 не установлен!
    echo.
    echo Установите зависимости:
    echo    pip install -r requirements_desktop.txt
    echo.
    pause
    exit /b 1
)

REM Запуск приложения
echo 🚀 Запуск RULETTT Desktop...
echo.

REM Попробуем разные варианты Python
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe rulettt_desktop.py
) else if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe rulettt_desktop.py
) else (
    py rulettt_desktop.py
)

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска приложения
    echo.
    pause
    exit /b 1
)
