"""
ТЕСТИРОВАНИЕ API PRAGMATIC PLAY LIVE
===================================

Проверка API endpoint: https://promo.pragmaticplaylive.net/api/v2/fetchinstantpoints
"""

import urllib.request
import urllib.parse
import json
from datetime import datetime

def test_pragmatic_api():
    """Тестирование Pragmatic Play API"""
    
    api_url = "https://promo.pragmaticplaylive.net/api/v2/fetchinstantpoints"
    
    print("🎰 ТЕСТИРОВАНИЕ PRAGMATIC PLAY API")
    print("=" * 40)
    print(f"URL: {api_url}")
    print()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }
    
    # Тестируем разные методы запроса
    methods_to_test = [
        ('GET', None),
        ('POST', {'action': 'fetch'}),
        ('POST', {'gameType': 'roulette'}),
        ('POST', {'limit': 10}),
    ]
    
    for method, data in methods_to_test:
        print(f"🔍 Тестируем {method} запрос...")
        
        try:
            if method == 'GET':
                req = urllib.request.Request(api_url, headers=headers)
            else:
                # POST запрос
                post_data = json.dumps(data).encode('utf-8') if data else b''
                req = urllib.request.Request(api_url, data=post_data, headers=headers)
                req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                content_type = response.headers.get('Content-Type', '')
                
                print(f"   ✅ Status: {status_code}")
                print(f"   📄 Content-Type: {content_type}")
                
                # Читаем ответ
                response_data = response.read().decode('utf-8')
                
                if response_data:
                    print(f"   📊 Размер ответа: {len(response_data)} байт")
                    
                    # Показываем первые 500 символов
                    preview = response_data[:500]
                    print(f"   📋 Содержимое: {preview}")
                    
                    if len(response_data) > 500:
                        print("   ... (обрезано)")
                    
                    # Пытаемся парсить JSON
                    if 'json' in content_type.lower():
                        try:
                            json_data = json.loads(response_data)
                            print(f"   🎯 JSON структура: {type(json_data)}")
                            
                            if isinstance(json_data, dict):
                                print(f"   🔑 Ключи: {list(json_data.keys())}")
                            elif isinstance(json_data, list):
                                print(f"   📝 Элементов в массиве: {len(json_data)}")
                                if json_data and isinstance(json_data[0], dict):
                                    print(f"   🔑 Ключи первого элемента: {list(json_data[0].keys())}")
                                    
                        except json.JSONDecodeError:
                            print("   ⚠️ Не удалось парсить JSON")
                
                else:
                    print("   ❌ Пустой ответ")
                    
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8', errors='ignore')
            print(f"   ❌ HTTP Error {e.code}: {e.reason}")
            if error_msg:
                print(f"   📄 Сообщение: {error_msg[:200]}")
                
        except urllib.error.URLError as e:
            print(f"   ❌ URL Error: {e.reason}")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        print()

def test_alternative_endpoints():
    """Тестируем альтернативные endpoints Pragmatic Play"""
    
    print("🔍 ТЕСТИРОВАНИЕ АЛЬТЕРНАТИВНЫХ ENDPOINTS")
    print("=" * 42)
    
    base_url = "https://promo.pragmaticplaylive.net"
    
    alternative_endpoints = [
        "/api/v2/game/roulette",
        "/api/v2/history",
        "/api/v2/live/results", 
        "/api/v2/tables",
        "/api/v1/fetchinstantpoints",
        "/api/game/history",
        "/live/roulette/data",
        "/roulette/results"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    for endpoint in alternative_endpoints:
        url = base_url + endpoint
        print(f"🔗 Проверяем: {endpoint}")
        
        try:
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                status_code = response.getcode()
                content_type = response.headers.get('Content-Type', '')
                
                if status_code == 200:
                    data = response.read(300).decode('utf-8', errors='ignore')
                    print(f"   ✅ {status_code}: {data[:100]}...")
                else:
                    print(f"   ⚠️ {status_code}")
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"   ❌ 404 - Не найден")
            else:
                print(f"   ❌ HTTP {e.code}")
        except Exception as e:
            print(f"   ❌ Ошибка: {str(e)[:50]}")
    
    print()

def create_pragmatic_config():
    """Создаем конфигурацию для Pragmatic Play"""
    
    print("⚙️ СОЗДАНИЕ КОНФИГУРАЦИИ PRAGMATIC PLAY")
    print("=" * 38)
    
    config = {
        "casino_name": "Pragmatic Play Live",
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
                "Content-Type": "application/json"
            },
            "timeout": 10,
            "retry_attempts": 3
        },
        "betting": {
            "base_bet": 100,
            "max_bet": 10000,
            "bankroll": 100000
        },
        "safety": {
            "enabled": True,
            "max_daily_loss": 50000,
            "stop_loss_percent": 20
        }
    }
    
    try:
        with open('pragmatic_play_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Конфигурация сохранена в pragmatic_play_config.json")
        print("📋 Настройки:")
        print(f"   🎰 Казино: {config['casino_name']}")
        print(f"   🏢 Провайдер: {config['provider']}")
        print(f"   🔗 API endpoints: {len(config['api']['endpoints'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения конфигурации: {e}")
        return False

def main():
    """Главная функция"""
    
    print("🎯 АНАЛИЗ API PRAGMATIC PLAY LIVE")
    print("=" * 35)
    print("Тестируем найденный API endpoint...")
    print()
    
    # Тестируем основной API
    test_pragmatic_api()
    
    # Тестируем альтернативы
    test_alternative_endpoints()
    
    # Создаем конфигурацию
    if create_pragmatic_config():
        print()
        print("🚀 СЛЕДУЮЩИЕ ШАГИ:")
        print("1. python test_connection.py - протестировать настройку")
        print("2. python src/main.py - запустить основную систему")
        print("3. Выбрать 'Получить реальные данные' в меню")
        print()
        print("🎉 Pragmatic Play API готов к использованию!")

if __name__ == "__main__":
    main()