@echo off
echo 🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ RULETTT
echo ===============================

echo.
echo 📡 Проверка API сервера...
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API сервер работает
) else (
    echo ❌ API сервер недоступен
    echo 🔧 Запустите: python api_server.py
)

echo.
echo 🌐 Проверка веб-сервера...
curl -s http://localhost:8080 >nul 2>&1  
if %errorlevel% equ 0 (
    echo ✅ Веб-сервер работает
) else (
    echo ❌ Веб-сервер недоступен
    echo 🔧 Запустите в папке webapp: python -m http.server 8080
)

echo.
echo 🏠 Проверка локальной сети...
curl -s http://192.168.88.216:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Локальная сеть доступна (192.168.88.216)
) else (
    echo ⚠️ Локальная сеть может быть недоступна извне
)

echo.
echo 🌍 Проверка ngrok конфигурации...
if exist "ngrok.yml" (
    findstr "YOUR_NGROK_TOKEN" ngrok.yml >nul
    if %errorlevel% equ 0 (
        echo ⚠️ ngrok токен не настроен (найден YOUR_NGROK_TOKEN)
        echo 🔧 Замените токен в ngrok.yml
    ) else (
        echo ✅ ngrok конфигурация готова
        
        echo 🔍 Проверяем активные туннели ngrok...
        curl -s http://127.0.0.1:4040/api/tunnels >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ ngrok туннели активны
        ) else (
            echo ⚠️ ngrok туннели не активны
            echo 🔧 Запустите: start_public_rulettt.bat
        )
    )
) else (
    echo ❌ Файл ngrok.yml не найден
)

echo.
echo 📁 Проверка файлов...
set "files_ok=1"

if not exist "api_server.py" (
    echo ❌ api_server.py не найден
    set "files_ok=0"
)

if not exist "webapp\dashboard.html" (
    echo ❌ webapp\dashboard.html не найден  
    set "files_ok=0"
)

if not exist "auto_collector_console_code.js" (
    echo ❌ auto_collector_console_code.js не найден
    set "files_ok=0"
)

if %files_ok% equ 1 (
    echo ✅ Все основные файлы на месте
)

echo.
echo 🎯 ИТОГОВЫЙ СТАТУС:
echo ==================
echo.
echo 📱 Доступные интерфейсы:
echo   - Dashboard: http://localhost:8080/dashboard.html
echo   - Mobile: http://localhost:8080/mobile.html  
echo   - Analytics: http://localhost:8080/advanced_analytics.html
echo   - Communication: http://localhost:8080/communication.html
echo.
echo 🔗 API endpoints (localhost:5000):
echo   - /api/health - Проверка работы
echo   - /api/games - Список игр
echo   - /api/results - Результаты рулетки
echo   - /api/stats - Статистика
echo.
echo 🌐 Для команды из интернета:
if exist "ngrok.yml" (
    findstr "YOUR_NGROK_TOKEN" ngrok.yml >nul
    if not %errorlevel% equ 0 (
        echo   ✅ Готово - запустите start_public_rulettt.bat
    ) else (
        echo   ⚠️ Настройте токен в ngrok.yml
    )
) else (
    echo   ❌ Настройте ngrok.yml
)
echo.
echo 👥 Для команды из офиса:
echo   ✅ Готово - используйте IP 192.168.88.216
echo.
echo 🔧 Для Codespaces:
echo   ✅ Готово - выполните ./start_codespaces.sh
echo.

pause