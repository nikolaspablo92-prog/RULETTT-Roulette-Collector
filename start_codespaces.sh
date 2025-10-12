#!/bin/bash

# 🎲 АВТОЗАПУСК RULETTT В GITHUB CODESPACES
# ========================================

echo "🎲 Запуск системы RULETTT в Codespaces..."
echo "=========================================="

# Установка зависимостей Python
echo "📦 Установка зависимостей Python..."
pip install flask flask-cors pandas aiohttp sqlite3 || true

# Создание необходимых папок
echo "📁 Создание структуры папок..."
mkdir -p data exports webapp/icons

# Проверка что файлы существуют
if [ ! -f "api_server.py" ]; then
    echo "❌ Файл api_server.py не найден!"
    exit 1
fi

if [ ! -f "webapp/dashboard.html" ]; then
    echo "❌ Веб-интерфейсы не найдены!"
    exit 1
fi

# Запуск API сервера в фоне
echo "🚀 Запуск API сервера (порт 5000)..."
python api_server.py &
API_PID=$!

# Ждем запуска API
sleep 5

# Запуск веб-сервера для интерфейсов
echo "🌐 Запуск веб-сервера (порт 8080)..."
cd webapp
python -m http.server 8080 &
WEB_PID=$!
cd ..

# Ждем запуска веб-сервера
sleep 3

echo ""
echo "✅ RULETTT успешно запущен в Codespaces!"
echo "=========================================="
echo ""
echo "🔗 Доступные интерфейсы:"
echo "  - API Health: /api/health (порт 5000)"
echo "  - Dashboard: /dashboard.html (порт 8080)"
echo "  - Mobile: /mobile.html (порт 8080)"
echo "  - Analytics: /advanced_analytics.html (порт 8080)"
echo "  - Communication: /communication.html (порт 8080)"
echo ""
echo "📡 VS Code автоматически создаст публичные ссылки для портов"
echo "🌐 Нажмите 'Make Public' когда появятся уведомления о портах"
echo ""
echo "🎯 Для остановки сервисов используйте:"
echo "  kill $API_PID  # Остановить API"
echo "  kill $WEB_PID  # Остановить веб-сервер"
echo ""

# Сохраняем PID процессов для возможности остановки
echo $API_PID > .api_pid
echo $WEB_PID > .web_pid

echo "🎉 Готово! Система RULETTT работает в Codespaces!"
echo "📋 Инструкция для участников команды в файле TEAM_INVITATION.md"

# Держим скрипт активным
wait