@echo off
chcp 65001 > nul
echo.
echo ====================================
echo 🎲 RULETTT - Запуск системы
echo ====================================
echo.

echo 🔍 Проверка портов...
netstat -an | findstr ":5000" > nul
if %errorlevel% equ 0 (
    echo ✅ API сервер уже запущен на порту 5000
) else (
    echo ⚠️  API сервер не запущен
    echo 🚀 Запускаю API сервер...
    start "RULETTT API Server" cmd /k "py api_server.py"
    timeout /t 3 > nul
)

netstat -an | findstr ":8080" > nul
if %errorlevel% equ 0 (
    echo ✅ Веб-сервер уже запущен на порту 8080
) else (
    echo ⚠️  Веб-сервер не запущен
    echo 🌐 Запускаю веб-сервер...
    start "RULETTT Web Server" cmd /k "cd webapp && py -m http.server 8080"
    timeout /t 3 > nul
)

echo.
echo ====================================
echo 🎉 Система запущена!
echo ====================================
echo.
echo 📡 API доступен:      http://localhost:5000
echo 🌐 Dashboard:         http://localhost:8080/logs_dashboard.html
echo 📊 Главная страница:  http://localhost:8080/dashboard.html
echo.
echo 🔍 Мониторинг:
echo    - Логи:            http://localhost:8080/logs_dashboard.html
echo    - Статистика:      http://localhost:5000/api/logs/stats
echo    - Ошибки:          http://localhost:5000/api/errors/unresolved
echo.
echo 📚 Документация:
echo    - QUICKSTART.md           - Быстрый старт
echo    - LOGGING_GUIDE.md        - Полное руководство
echo    - LOGGING_INTEGRATION_EXAMPLE.py - Примеры
echo.

choice /c OT /n /m "Нажмите [O] чтобы открыть Dashboard, [T] чтобы протестировать: "
if errorlevel 2 goto test
if errorlevel 1 goto open

:open
echo.
echo 🌐 Открываю Dashboard в браузере...
start http://localhost:8080/logs_dashboard.html
goto end

:test
echo.
echo 🧪 Запускаю тестовый пример...
py LOGGING_INTEGRATION_EXAMPLE.py
echo.
echo ✅ Тест завершён! Проверьте логи в dashboard.
timeout /t 3
start http://localhost:8080/logs_dashboard.html
goto end

:end
echo.
echo 💡 Совет: Для остановки сервисов закройте окна терминалов.
echo.
pause
