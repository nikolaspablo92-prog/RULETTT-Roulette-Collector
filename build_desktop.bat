@echo off
REM ============================================
REM 🎰 RULETTT Desktop - Windows Builder
REM ============================================

echo.
echo ════════════════════════════════════════════
echo    RULETTT Desktop Application Builder
echo ════════════════════════════════════════════
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python найден

REM Установка зависимостей
echo.
echo [2/5] Установка зависимостей...
pip install -r requirements_desktop.txt
if errorlevel 1 (
    echo ⚠️ Ошибка установки зависимостей
    pause
    exit /b 1
)
echo ✅ Зависимости установлены

REM Создание иконки (если нужно)
echo.
echo [3/5] Подготовка ресурсов...
if not exist "icon.ico" (
    echo ℹ️ icon.ico не найден, будет использована стандартная иконка
) else (
    echo ✅ icon.ico найден
)

REM Очистка предыдущей сборки
echo.
echo [4/5] Очистка...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
echo ✅ Старые файлы удалены

REM Сборка приложения
echo.
echo [5/5] Сборка приложения...
echo ⏳ Это может занять 2-3 минуты...
pyinstaller --clean rulettt_desktop.spec
if errorlevel 1 (
    echo ❌ Ошибка сборки!
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════
echo ✅ СБОРКА ЗАВЕРШЕНА УСПЕШНО!
echo ════════════════════════════════════════════
echo.
echo 📁 Готовое приложение: dist\RULETTT\RULETTT.exe
echo.
echo 💡 Следующие шаги:
echo    1. Откройте папку: dist\RULETTT
echo    2. Запустите: RULETTT.exe
echo    3. Создайте ярлык на рабочем столе
echo.
echo 📦 Для создания инсталлятора запустите: build_installer.bat
echo.
pause
