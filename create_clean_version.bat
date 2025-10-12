@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      🧹 СОЗДАНИЕ ЧИСТОЙ ВЕРСИИ ПРОЕКТА ДЛЯ ДРУГА          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Создаем чистую папку
if exist "CLEAN_PROJECT" rmdir /s /q "CLEAN_PROJECT"
mkdir "CLEAN_PROJECT"

echo 📋 Копирую ТОЛЬКО нужные файлы...

:: Основные файлы для работы
copy "auto_collector_console_code.js" "CLEAN_PROJECT\" >nul
copy "console_to_analysis.py" "CLEAN_PROJECT\" >nul

:: Инструкции и документация
copy "FOR_FRIEND.txt" "CLEAN_PROJECT\" >nul
copy "START_COLLECTOR.txt" "CLEAN_PROJECT\" >nul
copy "SAVE_STATS_GUIDE.txt" "CLEAN_PROJECT\" >nul
copy "QUICK_START.txt" "CLEAN_PROJECT\" >nul
copy "README.md" "CLEAN_PROJECT\" >nul

:: Примеры данных
copy "roulette_console_data.json" "CLEAN_PROJECT\" >nul
copy "roulette_console_data_example.json" "CLEAN_PROJECT\" >nul

:: Создаем файл с описанием
echo # 🎰 Сборщик Данных Рулетки - Чистая Версия > "CLEAN_PROJECT\README_CLEAN.txt"
echo. >> "CLEAN_PROJECT\README_CLEAN.txt"
echo Это упрощенная версия проекта только с нужными файлами: >> "CLEAN_PROJECT\README_CLEAN.txt"
echo. >> "CLEAN_PROJECT\README_CLEAN.txt"
echo 📁 ФАЙЛЫ В ЭТОЙ ПАПКЕ: >> "CLEAN_PROJECT\README_CLEAN.txt"
echo ✅ auto_collector_console_code.js - Главный сборщик для браузера >> "CLEAN_PROJECT\README_CLEAN.txt"
echo ✅ console_to_analysis.py - Анализатор стратегий >> "CLEAN_PROJECT\README_CLEAN.txt"
echo ✅ FOR_FRIEND.txt - НАЧНИТЕ С ЭТОГО ФАЙЛА! >> "CLEAN_PROJECT\README_CLEAN.txt"
echo ✅ START_COLLECTOR.txt - Подробные инструкции >> "CLEAN_PROJECT\README_CLEAN.txt"
echo ✅ SAVE_STATS_GUIDE.txt - Как сохранять статистику >> "CLEAN_PROJECT\README_CLEAN.txt"
echo ✅ roulette_console_data.json - Пример данных >> "CLEAN_PROJECT\README_CLEAN.txt"
echo. >> "CLEAN_PROJECT\README_CLEAN.txt"
echo 🚀 НАЧАЛО РАБОТЫ: >> "CLEAN_PROJECT\README_CLEAN.txt"
echo 1. Прочитайте FOR_FRIEND.txt >> "CLEAN_PROJECT\README_CLEAN.txt"
echo 2. Откройте рулетку в браузере >> "CLEAN_PROJECT\README_CLEAN.txt"
echo 3. Скопируйте код из auto_collector_console_code.js в консоль >> "CLEAN_PROJECT\README_CLEAN.txt"
echo 4. Начинайте сбор данных! >> "CLEAN_PROJECT\README_CLEAN.txt"

:: Создаем архив
echo 📦 Создаю архив чистой версии...
powershell Compress-Archive -Path "CLEAN_PROJECT\*" -DestinationPath "CLEAN_Roulette_Collector.zip" -Force

echo.
echo ✅ ГОТОВО! Создана чистая версия:
echo.
echo 📁 Папка: CLEAN_PROJECT\ (только 9 нужных файлов)
echo 📦 Архив: CLEAN_Roulette_Collector.zip (компактный)
echo.
echo 🎯 Теперь другу будет легче разобраться!
echo.
echo 📋 В чистой версии только:
echo    - Основной JavaScript сборщик
echo    - Python анализатор  
echo    - Инструкции для новичка
echo    - Примеры данных
echo.
pause