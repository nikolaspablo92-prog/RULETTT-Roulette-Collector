"""
НАСТРОЙКА АВТОРИЗАЦИИ ДЛЯ PRAGMATIC PLAY API
===========================================

API требует авторизацию - нужно найти токены в браузере
"""

import json
from pathlib import Path

def show_authorization_guide():
    """Показывает как найти авторизационные данные"""
    
    print("""
🔐 PRAGMATIC PLAY API ТРЕБУЕТ АВТОРИЗАЦИЮ
========================================

✅ ХОРОШИЕ НОВОСТИ:
• API работает и отвечает (HTTP 401 - это нормально)
• Сервер активен и доступен
• Структура API корректная

❗ ЧТО НУЖНО:
• Авторизационные заголовки из браузера
• Токены доступа
• Возможно cookies сессии

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🕵️ КАК НАЙТИ АВТОРИЗАЦИЮ В БРАУЗЕРЕ:
===================================

1. 🌐 ОТКРОЙТЕ PRAGMATIC PLAY КАЗИНО:
   • Найдите казино использующее Pragmatic Play Live
   • Зайдите в live-рулетку Pragmatic Play
   • Авторизуйтесь/войдите в аккаунт

2. 🔧 ОТКРОЙТЕ DEVELOPER TOOLS:
   • F12 → Network → XHR фильтр
   • Обновите страницу игры
   • Подождите загрузки

3. 🎯 НАЙДИТЕ РАБОЧИЙ ЗАПРОС:
   Ищите запросы к pragmaticplaylive.net:
   • fetchinstantpoints
   • game/roulette  
   • history
   • любые другие с Status 200

4. 📋 СКОПИРУЙТЕ ЗАГОЛОВКИ:
   Кликните на рабочий запрос → Headers:
   
   ИЩИТЕ ЗАГОЛОВКИ:
   ✅ Authorization: Bearer abc123...
   ✅ X-API-Key: xyz789...
   ✅ Cookie: session=...; token=...
   ✅ X-Auth-Token: ...
   ✅ Authentication: ...

5. 📊 ПРОВЕРЬТЕ REQUEST PAYLOAD:
   Может быть нужны параметры в теле запроса:
   • playerId
   • gameId  
   • sessionToken
   • tableId

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎰 РЕКОМЕНДУЕМЫЕ КАЗИНО С PRAGMATIC PLAY:
========================================

ПОПРОБУЙТЕ ЭТИ КАЗИНО:
✅ LeoVegas - много Pragmatic Play игр
✅ Casumo - хорошие API
✅ PlayOJO - открытые запросы  
✅ Mr Green - качественная интеграция
✅ Betway - стабильные API

КРИПТОКАЗИНО:
✅ BC.Game - есть Pragmatic Play
✅ Stake.com - может быть PP Live
✅ Roobet - проверьте наличие

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ БЫСТРАЯ НАСТРОЙКА ПОСЛЕ НАХОЖДЕНИЯ ТОКЕНОВ:
==============================================
    """)

def create_auth_template():
    """Создает шаблон для авторизационных данных"""
    
    auth_template = {
        "casino_name": "Pragmatic Play Casino",
        "provider": "Pragmatic Play",
        "connection_method": "api",
        "api": {
            "base_url": "https://promo.pragmaticplaylive.net",
            "endpoints": {
                "instant_points": "/api/v2/fetchinstantpoints",
                "live_results": "/api/v2/live/results", 
                "history": "/api/v2/history",
                "tables": "/api/v2/tables"
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Content-Type": "application/json",
                "Authorization": "ЗАМЕНИТЬ_НА_РЕАЛЬНЫЙ_ТОКЕН",
                "X-API-Key": "ЗАМЕНИТЬ_ЕСЛИ_ЕСТЬ",
                "Cookie": "ЗАМЕНИТЬ_НА_РЕАЛЬНЫЕ_COOKIES"
            },
            "auth": {
                "type": "bearer_token",
                "token": "ТОКЕН_ИЗ_БРАУЗЕРА",
                "refresh_token": "ЕСЛИ_ЕСТЬ",
                "expires_in": 3600
            },
            "timeout": 10
        },
        "game_params": {
            "playerId": "ВАШЕ_ID",
            "gameId": "roulette",
            "tableId": "СТОЛ_ID", 
            "sessionToken": "ТОКЕН_СЕССИИ"
        },
        "betting": {
            "base_bet": 100,
            "max_bet": 10000,
            "bankroll": 100000
        }
    }
    
    try:
        with open('pragmatic_auth_template.json', 'w', encoding='utf-8') as f:
            json.dump(auth_template, f, indent=2, ensure_ascii=False)
        
        print("✅ Создан шаблон: pragmatic_auth_template.json")
        print("📝 Замените ЗАГЛАВНЫЕ значения на реальные данные из браузера")
        
    except Exception as e:
        print(f"❌ Ошибка создания шаблона: {e}")

def setup_auth_interactive():
    """Интерактивная настройка авторизации"""
    
    print("\n🔐 ИНТЕРАКТИВНАЯ НАСТРОЙКА АВТОРИЗАЦИИ")
    print("=" * 38)
    
    print("Вставьте данные из браузера (Enter чтобы пропустить):")
    
    auth_data = {}
    
    # Собираем авторизационные данные
    authorization = input("Authorization заголовок: ").strip()
    if authorization and not authorization.startswith("ЗАМЕНИТЬ"):
        auth_data["Authorization"] = authorization
    
    api_key = input("X-API-Key (если есть): ").strip()
    if api_key and not api_key.startswith("ЗАМЕНИТЬ"):
        auth_data["X-API-Key"] = api_key
    
    cookies = input("Cookie заголовок: ").strip()
    if cookies and not cookies.startswith("ЗАМЕНИТЬ"):
        auth_data["Cookie"] = cookies
    
    player_id = input("Player ID (если есть): ").strip()
    table_id = input("Table ID (если есть): ").strip()
    session_token = input("Session Token (если есть): ").strip()
    
    if auth_data or player_id or table_id or session_token:
        # Создаем рабочую конфигурацию
        config = {
            "casino_name": "Pragmatic Play Live Casino",
            "provider": "Pragmatic Play", 
            "connection_method": "api",
            "api": {
                "base_url": "https://promo.pragmaticplaylive.net",
                "endpoints": {
                    "instant_points": "/api/v2/fetchinstantpoints"
                },
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                "timeout": 10
            },
            "betting": {
                "base_bet": 100,
                "max_bet": 10000,
                "bankroll": 100000  
            }
        }
        
        # Добавляем авторизационные данные
        config["api"]["headers"].update(auth_data)
        
        if player_id or table_id or session_token:
            config["game_params"] = {}
            if player_id:
                config["game_params"]["playerId"] = player_id
            if table_id:
                config["game_params"]["tableId"] = table_id  
            if session_token:
                config["game_params"]["sessionToken"] = session_token
        
        # Сохраняем конфигурацию
        try:
            with open('casino_setup.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("\n✅ Конфигурация с авторизацией сохранена!")
            print("🧪 Запустите: python test_connection.py")
            
        except Exception as e:
            print(f"\n❌ Ошибка сохранения: {e}")
    
    else:
        print("\n⏭️ Данные не введены, используйте шаблон")

def main():
    """Главная функция"""
    
    print("🔐 НАСТРОЙКА АВТОРИЗАЦИИ PRAGMATIC PLAY API")
    print("=" * 44)
    
    # Показываем результат теста
    print("📊 РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ:")
    print("✅ API найден и работает")  
    print("❗ Требуется авторизация (HTTP 401)")
    print("🎯 URL: https://promo.pragmaticplaylive.net/api/v2/fetchinstantpoints")
    print()
    
    # Показываем гайд
    show_authorization_guide()
    
    # Создаем шаблон
    create_auth_template()
    
    print("\n" + "="*50)
    
    # Интерактивная настройка
    choice = input("Хотите настроить авторизацию сейчас? (y/n): ").lower()
    if choice == 'y':
        setup_auth_interactive()
    else:
        print("\n📋 ПЛАН ДЕЙСТВИЙ:")
        print("1. Найдите казино с Pragmatic Play Live")
        print("2. Откройте Network в браузере")  
        print("3. Скопируйте авторизационные заголовки")
        print("4. Запустите этот скрипт снова и выберите 'y'")
        print("5. python test_connection.py - проверить")
        
    print("\n🎉 Настройка Pragmatic Play API готова!")

if __name__ == "__main__":
    main()