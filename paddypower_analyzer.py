"""
АНАЛИЗАТОР API ИЗ КОНСОЛИ БРАУЗЕРА
=================================

Этот инструмент анализирует найденные API из консоли браузера
и создает конфигурацию для системы рулетки.
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path

class APIAnalyzer:
    """Анализатор найденных API"""
    
    def __init__(self):
        self.found_apis = []
        self.roulette_apis = []
        
    def analyze_paddypower_apis(self):
        """Анализируем найденные API от Paddy Power"""
        print("🎯 АНАЛИЗ API PADDY POWER")
        print("=" * 26)
        
        # Основные API которые мы нашли
        apis = {
            "tables_details": {
                "url": "https://games.paddypower.com/api/tables-details",
                "method": "GET",
                "description": "Информация о столах live-казино",
                "priority": "HIGH"
            },
            "pragmatic_statistics": {
                "url": "https://games.pragmaticplaylive.net/api/ui/statisticHistory",
                "method": "GET", 
                "description": "История статистики рулетки (500 игр)",
                "priority": "VERY HIGH",
                "params": "tableId=roulettestura541&numberOfGames=500"
            },
            "table_config": {
                "url": "https://games.pragmaticplaylive.net/cgibin/tableconfig.jsp",
                "method": "GET",
                "description": "Конфигурация стола рулетки",
                "priority": "HIGH",
                "params": "table_id=roulettestura541"
            },
            "player_config": {
                "url": "https://games.pragmaticplaylive.net/cgibin/playerconfig.jsp", 
                "method": "GET",
                "description": "Конфигурация игрока",
                "priority": "MEDIUM",
                "params": "table_id=roulettestura541"
            },
            "balance": {
                "url": "https://games.pragmaticplaylive.net/cgibin/balance.jsp",
                "method": "GET", 
                "description": "Баланс игрока",
                "priority": "LOW"
            },
            "instant_points": {
                "url": "https://promo.pragmaticplaylive.net/api/v2/fetchinstantpoints",
                "method": "GET",
                "description": "Мгновенные очки/промо",
                "priority": "LOW"
            }
        }
        
        print("🔍 НАЙДЕННЫЕ API:")
        for name, api in apis.items():
            print(f"✅ {name}:")
            print(f"   URL: {api['url']}")
            print(f"   Метод: {api['method']}")
            print(f"   Описание: {api['description']}")
            print(f"   Приоритет: {api['priority']}")
            if 'params' in api:
                print(f"   Параметры: {api['params']}")
            print()
        
        return apis
    
    def extract_auth_headers(self):
        """Извлекаем заголовки авторизации"""
        print("🔐 НАЙДЕННЫЕ ЗАГОЛОВКИ АВТОРИЗАЦИИ:")
        
        headers = {
            "pragmatic_session": "_fnL3MJVfFXHrua4kCzrnZt9R2iRB6dtjIwd5J35sO2tbm7gU1n_!-428929514-77fbc135",
            "pragmatic_bearer": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcGMxNzM1MjEzMzYzMzU5IiwicHBpZCI6MTI0NDUyMTk1LCJjYyI6IkdCIiwiY3NpZCI6InBwY2RrMDAwMDAwMDMyNTUiLCJqc2lkIjoiX2ZuTDNNSlZmRlhIcnVhNGtDenJuWnQ5UjJpUkI2ZHRqSXdkNUozNXNPMnRibTdnVTFuXyEtNDI4OTI5NTE0LTc3ZmJjMTM1IiwiZXBpZCI6IjU0NjAyNjMzIiwiZW52SWQiOjEsIm9waWQiOjE2NzksImpkIjoiVUsiLCJjdXIiOiJHQlAiLCJzbiI6ImxvbGE3NiIsInBhIjp0cnVlLCJzY3NpZCI6MzI1NSwidWNpZCI6MTM4NDAwMiwiaWF0IjoxNzYwMDYxODY5LCJleHAiOjE3NjAwNjU0Njl9.nztC0hgkedA1yqoNpmOKeknSa1GltLTftuNw7YK8XF57ZnVqeBtGdy-YbiZN33fjbxTDr_aIfPMX2wtt2hn_tw",
            "paddypower_auth": "zPMBVXgcjQ47fQ8OOE+hdHP7JsdZ1UPhODFaPQYlSbA=",
            "paddypower_application": "SRbxTcviudtb943"
        }
        
        print("🔑 JSESSIONID:", headers["pragmatic_session"][:50] + "...")
        print("🎫 Bearer Token:", headers["pragmatic_bearer"][:50] + "...")
        print("🏷️ PP Auth:", headers["paddypower_auth"])
        print("📱 PP Application:", headers["paddypower_application"])
        
        return headers
    
    def test_api_endpoints(self, apis, headers):
        """Тестируем найденные API endpoints"""
        print("\n🧪 ТЕСТИРОВАНИЕ API ENDPOINTS")
        print("=" * 30)
        
        results = {}
        
        for name, api in apis.items():
            print(f"\n🔍 Тестирую {name}...")
            
            try:
                # Строим URL с параметрами
                url = api['url']
                if 'params' in api:
                    url += '?' + api['params']
                
                # Добавляем timestamp для некоторых API
                if 'pragmaticplaylive.net' in url:
                    separator = '&' if '?' in url else '?'
                    url += f"{separator}JSESSIONID={headers['pragmatic_session']}&ck=1760061900000&game_mode=lobby_desktop"
                
                # Создаем запрос
                req = urllib.request.Request(url)
                
                # Добавляем заголовки
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                req.add_header('Accept', 'application/json, text/plain, */*')
                req.add_header('Accept-Language', 'ru,en-US;q=0.9,en;q=0.8,lt;q=0.7')
                
                if 'promo.pragmaticplaylive.net' in url:
                    req.add_header('Authorization', f"Bearer {headers['pragmatic_bearer']}")
                
                # Выполняем запрос
                with urllib.request.urlopen(req, timeout=10) as response:
                    status_code = response.getcode()
                    content_type = response.headers.get('Content-Type', '')
                    data = response.read(1000).decode('utf-8', errors='ignore')
                    
                    results[name] = {
                        'status': status_code,
                        'content_type': content_type,
                        'data_preview': data[:200],
                        'success': status_code == 200
                    }
                    
                    if status_code == 200:
                        print(f"   ✅ Успешно: HTTP {status_code}")
                        print(f"   📊 Тип: {content_type}")
                        print(f"   📄 Данные: {data[:100]}...")
                        
                        # Проверяем на рулеточные данные
                        if self.contains_roulette_data(data):
                            print(f"   🎰 СОДЕРЖИТ ДАННЫЕ РУЛЕТКИ!")
                            self.roulette_apis.append(name)
                    else:
                        print(f"   ⚠️ HTTP {status_code}")
                        
            except urllib.error.HTTPError as e:
                print(f"   ❌ HTTP Error {e.code}: {e.reason}")
                if e.code == 401:
                    print(f"   🔐 Требуется авторизация")
                results[name] = {'status': e.code, 'success': False, 'error': str(e)}
                
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                results[name] = {'status': 0, 'success': False, 'error': str(e)}
        
        return results
    
    def contains_roulette_data(self, data):
        """Проверяет, содержат ли данные информацию о рулетке"""
        roulette_indicators = [
            'roulette', 'wheel', 'spin', 'number', 'red', 'black',
            'winning', 'history', 'result', 'ball', 'sector',
            '"0"', '"1"', '"2"', '"3"', '"4"', '"5"', '"6"', '"7"', '"8"', '"9"'
        ]
        
        data_lower = data.lower()
        found_indicators = [indicator for indicator in roulette_indicators if indicator in data_lower]
        
        return len(found_indicators) >= 2
    
    def create_casino_config(self, apis, headers, results):
        """Создаем конфигурацию казино"""
        print("\n⚙️ СОЗДАНИЕ КОНФИГУРАЦИИ")
        print("=" * 24)
        
        # Выбираем только успешные API
        working_apis = {name: api for name, api in apis.items() 
                       if results.get(name, {}).get('success', False)}
        
        if not working_apis:
            print("❌ Нет работающих API для конфигурации")
            return None
        
        config = {
            "casino_name": "Paddy Power + Pragmatic Play Live",
            "connection_method": "api",
            "api": {
                "base_url": "https://games.pragmaticplaylive.net",
                "endpoints": {},
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,lt;q=0.7"
                },
                "auth": {
                    "jsessionid": headers["pragmatic_session"],
                    "bearer_token": headers["pragmatic_bearer"],
                    "pp_auth": headers["paddypower_auth"],
                    "pp_application": headers["paddypower_application"]
                }
            },
            "betting": {
                "base_bet": 100,
                "max_bet": 10000,
                "bankroll": 100000
            },
            "safety": {
                "enabled": True,
                "max_daily_loss": 50000
            },
            "table_info": {
                "table_id": "roulettestura541",
                "game_id": "952a1"
            }
        }
        
        # Добавляем рабочие endpoints
        for name, api in working_apis.items():
            endpoint_path = api['url']
            if 'params' in api:
                endpoint_path += '?' + api['params']
            
            config['api']['endpoints'][name] = {
                'url': endpoint_path,
                'method': api['method'],
                'description': api['description'],
                'priority': api['priority']
            }
        
        # Сохраняем конфигурацию
        try:
            config_path = Path(__file__).parent / "paddypower_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Конфигурация сохранена в {config_path}")
            print(f"🎯 Найдено {len(working_apis)} рабочих API")
            print(f"🎰 Рулеточных API: {len(self.roulette_apis)}")
            
            return config
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return None
    
    def show_usage_instructions(self):
        """Показываем инструкции по использованию"""
        print("\n📋 ИНСТРУКЦИИ ПО ИСПОЛЬЗОВАНИЮ")
        print("=" * 30)
        
        print("""
🎯 СЛЕДУЮЩИЕ ШАГИ:

1. 📁 ОБНОВИТЕ ОСНОВНУЮ КОНФИГУРАЦИЮ:
   cp paddypower_config.json casino_setup.json

2. 🧪 ПРОТЕСТИРУЙТЕ ПОДКЛЮЧЕНИЕ:
   python test_connection.py

3. 🚀 ЗАПУСТИТЕ СИСТЕМУ:
   python src/main.py

4. 📊 В МЕНЮ ВЫБЕРИТЕ:
   "Управление данными" → "Получить реальные данные"

⚠️ ВАЖНО:
• Токены авторизации имеют срок действия
• Обновляйте их каждые несколько часов
• Не делайте слишком частые запросы

🔧 НАСТРОЙКА АВТООБНОВЛЕНИЯ:
Создайте скрипт для регулярного обновления токенов
из браузера или используйте автоматический парсинг.
        """)
    
    def run(self):
        """Запуск анализа"""
        print("🔍 АНАЛИЗАТОР API ИЗ КОНСОЛИ БРАУЗЕРА")
        print("=" * 38)
        
        # Анализируем найденные API
        apis = self.analyze_paddypower_apis()
        
        # Извлекаем заголовки авторизации
        headers = self.extract_auth_headers()
        
        # Тестируем API
        results = self.test_api_endpoints(apis, headers)
        
        # Создаем конфигурацию
        config = self.create_casino_config(apis, headers, results)
        
        if config:
            # Показываем инструкции
            self.show_usage_instructions()
            
            print("\n🎉 АНАЛИЗ ЗАВЕРШЕН!")
            print("Найдены рабочие API для Paddy Power + Pragmatic Play!")
        else:
            print("\n😞 Не удалось создать конфигурацию")


def main():
    """Главная функция"""
    try:
        analyzer = APIAnalyzer()
        analyzer.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Анализ прерван пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()