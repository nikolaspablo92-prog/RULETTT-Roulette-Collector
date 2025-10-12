@echo off
echo 🌐 НАСТРОЙКА ПУБЛИЧНОГО ДОСТУПА К RULETTT
echo ========================================
echo.

echo 📥 Устанавливаем ngrok для публичного доступа...
echo.

REM Проверяем есть ли ngrok
where ngrok >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ ngrok уже установлен
    goto :start_ngrok
)

echo ❌ ngrok не найден. Устанавливаем...
echo.

REM Скачиваем ngrok через PowerShell
powershell -Command "& {Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'}"
powershell -Command "& {Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force}"
del ngrok.zip

echo ✅ ngrok установлен локально
echo.

:start_ngrok
echo 🚀 Запускаем публичные туннели...
echo.

REM Создаем конфигурационный файл ngrok
echo version: "2" > ngrok.yml
echo authtoken: YOUR_NGROK_TOKEN >> ngrok.yml
echo tunnels: >> ngrok.yml
echo   api: >> ngrok.yml
echo     addr: 5000 >> ngrok.yml
echo     proto: http >> ngrok.yml
echo     bind-tls: true >> ngrok.yml
echo   web: >> ngrok.yml
echo     addr: 8080 >> ngrok.yml
echo     proto: http >> ngrok.yml
echo     bind-tls: true >> ngrok.yml

echo 📝 Конфигурация ngrok создана (ngrok.yml)
echo.

echo ⚠️  ВАЖНО: Зарегистрируйтесь на https://ngrok.com и получите authtoken
echo ⚠️  Замените YOUR_NGROK_TOKEN в файле ngrok.yml на ваш токен
echo.

echo 🎯 После настройки токена запустите:
echo    ngrok start --config ngrok.yml --all
echo.

echo 🌐 Это создаст публичные URL для:
echo    - API сервер (порт 5000)
echo    - Веб-интерфейсы (порт 8080)
echo.

echo 📤 Отправьте эти URL участникам команды!
echo.

pause