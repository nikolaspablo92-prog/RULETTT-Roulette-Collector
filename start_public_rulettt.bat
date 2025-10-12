@echo off
title RULETTT - Публичный доступ через ngrok
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║           🎲 RULETTT - ПУБЛИЧНЫЙ ЗАПУСК 🌐           ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Проверяем что серверы не запущены
echo ⚡ Проверяем состояние портов...
netstat -an | find "5000" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ API сервер уже запущен на порту 5000
) else (
    echo 🚀 Запускаем API сервер...
    start "RULETTT API Server" /MIN C:/Users/Pablo/RULETTT/Scripts/python.exe api_server.py
    timeout /t 3 /nobreak >nul
)

netstat -an | find "8080" >nul  
if %ERRORLEVEL% EQU 0 (
    echo ✅ Веб-сервер уже запущен на порту 8080
) else (
    echo 🌐 Запускаем веб-сервер...
    cd /d "C:\Users\Pablo\RULETTT\webapp"
    start "RULETTT Web Server" /MIN C:/Users/Pablo/RULETTT/Scripts/python.exe -m http.server 8080
    cd /d "C:\Users\Pablo\RULETTT"
    timeout /t 5 /nobreak >nul
)

REM Проверяем настройку ngrok
if not exist "ngrok.yml" (
    echo ❌ Файл ngrok.yml не найден!
    echo 📋 Сначала настройте ngrok по инструкции NGROK_SETUP_GUIDE.md
    pause
    exit /b 1
)

REM Проверяем есть ли токен
findstr "YOUR_NGROK_TOKEN" ngrok.yml >nul
if %ERRORLEVEL% EQU 0 (
    echo ❌ Токен ngrok не настроен!
    echo.
    echo 📋 Инструкция по настройке:
    echo 1. Зарегистрируйтесь на https://ngrok.com
    echo 2. Получите authtoken в личном кабинете  
    echo 3. Замените YOUR_NGROK_TOKEN в ngrok.yml на ваш токен
    echo 4. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo.
echo 🌍 Создаем публичные туннели через ngrok...
echo ⏳ Это может занять 10-15 секунд...
echo.

REM Запуск ngrok
ngrok start --config ngrok.yml --all

REM Если дошли сюда, значит ngrok завершился
echo.
echo ⚠️  ngrok завершил работу
echo 🔄 Перезапустите скрипт для повторного подключения
echo.
pause