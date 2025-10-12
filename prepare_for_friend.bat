@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║        🚀 ПОДГОТОВКА ПРОЕКТА ДЛЯ ПЕРЕДАЧИ ДРУГУ            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📁 Создаю папку для друга...
if not exist "FOR_FRIEND" mkdir FOR_FRIEND

echo 📋 Копирую основные файлы...
copy "auto_collector_console_code.js" "FOR_FRIEND\" >nul
copy "console_to_analysis.py" "FOR_FRIEND\" >nul
copy "START_COLLECTOR.txt" "FOR_FRIEND\" >nul
copy "FOR_FRIEND.txt" "FOR_FRIEND\" >nul
copy "SAVE_STATS_GUIDE.txt" "FOR_FRIEND\" >nul
copy "QUICK_START.txt" "FOR_FRIEND\" >nul
copy "README.md" "FOR_FRIEND\" >nul

echo 📊 Копирую примеры данных...
if exist "roulette_console_data.json" copy "roulette_console_data.json" "FOR_FRIEND\" >nul
if exist "roulette_console_data_example.json" copy "roulette_console_data_example.json" "FOR_FRIEND\" >nul

echo 📦 Создаю архив...
powershell Compress-Archive -Path "FOR_FRIEND\*" -DestinationPath "Roulette_Collector_for_Friend.zip" -Force

echo.
echo ✅ ГОТОВО! Файлы подготовлены:
echo.
echo 📁 Папка: FOR_FRIEND\ 
echo 📦 Архив: Roulette_Collector_for_Friend.zip
echo.
echo 🎯 Отправьте другу:
echo    - Архив Roulette_Collector_for_Friend.zip
echo    - Или всю папку FOR_FRIEND
echo.
echo 💡 В архиве есть файл FOR_FRIEND.txt с инструкциями!
echo.
pause