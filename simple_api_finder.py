"""
ПРОСТОЙ ПОИСКОВИК API КАЗИНО (БЕЗ ВНЕШНИХ ЗАВИСИМОСТЕЙ)
========================================================

Использует только стандартные библиотеки Python.
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class SimpleCasinoAPIFinder:
    """Простой поисковик API казино"""
    
    def __init__(self):
        # Известные казино с потенциальными API
        self.known_casinos = {
            'stake': {
                'name': 'Stake.com',
                'base_url': 'https://stake.com',
                'endpoints': [
                    '/_api/graphql',
                    '/api/v1/casino/games/history'
                ],
                'description': 'Крупное криптовалютное казино с публичными API'
            },
            'bc_game': {
                'name': 'BC.Game', 
                'base_url': 'https://bc.game',
                'endpoints': [
                    '/api/casino/roulette/history',
                    '/api/v1/live-games'
                ],
                'description': 'Криптовалютное казино'
            },
            'bustabit': {
                'name': 'Bustabit (пример хорошего API)',
                'base_url': 'https://www.bustabit.com',
                'endpoints': [
                    '/api/games/history'
                ],
                'description': 'Полностью открытый API (не рулетка, но хороший пример)'
            }
        }
    
    def run(self):
        """Запуск поисковика"""
        print("🔍 ПРОСТОЙ ПОИСКОВИК API КАЗИНО")
        print("=" * 35)
        print("(Использует только стандартные библиотеки Python)\n")
        
        while True:
            print("Выберите действие:")
            print("1. Тестировать известные казино")
            print("2. Проверить конкретный URL")
            print("3. Показать гайд по поиску API")
            print("4. Примеры рабочих запросов")
            print("0. Выход")
            
            choice = input("\nВыбор (0-4): ").strip()
            
            if choice == "1":
                self.test_known_casinos()
            elif choice == "2":
                self.test_custom_url()
            elif choice == "3":
                self.show_search_guide()
            elif choice == "4":
                self.show_working_examples()
            elif choice == "0":
                break
            else:
                print("❌ Неверный выбор")
            
            input("\nНажмите Enter для продолжения...")
    
    def test_known_casinos(self):
        """Тестирование известных казино"""
        print("\n🎰 ТЕСТИРОВАНИЕ ИЗВЕСТНЫХ КАЗИНО")
        print("-" * 35)
        
        for casino_id, info in self.known_casinos.items():
            print(f"\n📍 {info['name']}")
            print(f"   {info['description']}")
            
            for endpoint in info['endpoints']:
                url = info['base_url'] + endpoint
                result = self.test_url(url)
                
                if result['success']:
                    print(f"   ✅ {endpoint} - HTTP {result['status']}")
                    if result.get('is_api'):
                        print(f"      🎯 Похоже на API! Тип: {result.get('content_type')}")
                else:
                    print(f"   ❌ {endpoint} - {result['error']}")
                
                time.sleep(1.5)  # Пауза между запросами
    
    def test_custom_url(self):
        """Тестирование пользовательского URL"""
        print("\n🔗 ТЕСТИРОВАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО URL")
        print("-" * 40)
        
        base_url = input("Введите базовый URL казино: ").strip()
        
        if not base_url:
            print("❌ URL не введен")
            return
        
        # Добавляем протокол если не указан
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
        
        # Стандартные API endpoints
        common_endpoints = [
            '/api',
            '/api/v1',
            '/api/v2',
            '/api/casino',
            '/api/live',
            '/api/roulette',
            '/api/games',
            '/api/casino/roulette',
            '/api/live/roulette',
            '/_api',
            '/graphql'
        ]
        
        print(f"\n🔍 Проверяем {len(common_endpoints)} стандартных endpoints...")
        
        found_apis = []
        
        for endpoint in common_endpoints:
            url = base_url + endpoint
            result = self.test_url(url)
            
            if result['success']:
                status_icon = "🎯" if result.get('is_api') else "✅"
                print(f"{status_icon} {endpoint} - HTTP {result['status']}")
                
                if result.get('is_api'):
                    found_apis.append((endpoint, result))
                    print(f"     📊 API обнаружен! Тип: {result.get('content_type')}")
            else:
                print(f"❌ {endpoint} - {result['error']}")
            
            time.sleep(0.8)  # Пауза
        
        if found_apis:
            print(f"\n🎉 НАЙДЕНО {len(found_apis)} ПОТЕНЦИАЛЬНЫХ API:")
            for endpoint, result in found_apis:
                print(f"   • {base_url}{endpoint}")
                print(f"     Тип: {result.get('content_type', 'unknown')}")
        else:
            print("\n😞 API endpoints не найдены")
            print("\n💡 РЕКОМЕНДАЦИИ:")
            print("   1. Проверьте документацию сайта")
            print("   2. Используйте браузерную консоль (F12)")
            print("   3. Поищите 'API' или 'Developer' на сайте")
            print("   4. Свяжитесь с технической поддержкой")
    
    def test_url(self, url: str) -> Dict:
        """Тестирование URL"""
        try:
            # Создаем запрос с заголовками
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            # Выполняем запрос
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.getcode()
                content_type = response.headers.get('Content-Type', '').lower()
                
                # Читаем первые байты для анализа
                data = response.read(1024)  # Первый килобайт
                
                # Определяем является ли это API
                is_api = self._detect_api(data, content_type)
                
                return {
                    'success': True,
                    'status': status,
                    'content_type': content_type,
                    'is_api': is_api,
                    'data_preview': data.decode('utf-8', errors='ignore')[:200]
                }
        
        except urllib.error.HTTPError as e:
            return {
                'success': False,
                'error': f'HTTP {e.code}',
                'status': e.code
            }
        except urllib.error.URLError as e:
            return {
                'success': False,
                'error': f'URL Error: {e.reason}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    def _detect_api(self, data: bytes, content_type: str) -> bool:
        """Определение является ли ответ API"""
        try:
            text = data.decode('utf-8', errors='ignore').lower()
            
            # Проверяем Content-Type
            if 'application/json' in content_type:
                return True
            
            # Проверяем содержимое
            api_indicators = [
                '{"', '[{', '"data":', '"api":', '"result":',
                '"status":', '"error":', '"message":', 
                'graphql', 'mutation', 'query'
            ]
            
            return any(indicator in text for indicator in api_indicators)
            
        except:
            return False
    
    def show_search_guide(self):
        """Показать гайд по поиску API"""
        print("\n📖 ГАЙД ПО ПОИСКУ API КАЗИНО")
        print("-" * 30)
        print("""
🔍 ГДЕ ИСКАТЬ API:

1. 📄 ДОКУМЕНТАЦИЯ САЙТА:
   • Ищите разделы: API, Developer, Integration
   • Обычно в футере сайта
   • Примеры: casino.com/api-docs, casino.com/developers

2. 🌐 АНАЛИЗ БРАУЗЕРА:
   • Откройте F12 (Developer Tools)
   • Вкладка Network (Сеть)
   • Играйте в рулетку и смотрите запросы
   • Ищите XHR/Fetch с JSON данными

3. 🔗 СТАНДАРТНЫЕ ПУТИ:
   • /api, /api/v1, /api/v2
   • /rest/api, /_api, /graphql
   • /casino/api, /live/api, /games/api

4. 📱 МОБИЛЬНЫЕ ПРИЛОЖЕНИЯ:
   • Часто используют более простые API
   • Анализируйте трафик мобильного приложения

5. 🤝 ОФИЦИАЛЬНЫЕ КАНАЛЫ:
   • Техподдержка казино
   • Партнерские программы
   • GitHub организации казино

⚖️ ВАЖНО:
• Всегда читайте Terms of Service
• Соблюдайте лимиты запросов
• Не перегружайте сервера
• Используйте данные этично

🎯 ЛУЧШИЕ КАНДИДАТЫ:
• Криптовалютные казино (часто более открытые)
• Казино с партнерскими программами
• Провайдеры live игр (Evolution, Pragmatic Play)
        """)
    
    def show_working_examples(self):
        """Показать примеры рабочих запросов"""
        print("\n🎯 ПРИМЕРЫ РАБОЧИХ API ЗАПРОСОВ")
        print("-" * 35)
        print("""
1. 🎰 STAKE.COM (GraphQL):
   URL: https://stake.com/_api/graphql
   Метод: POST
   Данные: GraphQL query для истории игр

2. 🎲 BUSTABIT:
   URL: https://www.bustabit.com/api/games/history
   Метод: GET
   Ответ: JSON с историей игр

3. 💎 BC.GAME:
   URL: https://bc.game/api/casino/roulette/history
   Метод: GET
   Ответ: История рулетки

ПРИМЕР КОДА:
```python
import urllib.request
import json

url = "https://www.bustabit.com/api/games/history"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        print(f"Получено {len(data)} записей")
        for game in data[:3]:
            print(f"Game {game['id']}: {game['bust_point']}")
except Exception as e:
    print(f"Ошибка: {e}")
```

⚠️ ПРИМЕЧАНИЯ:
• Эти примеры могут устареть
• Всегда проверяйте актуальность
• Соблюдайте правила использования
• Добавляйте задержки между запросами
        """)


def main():
    """Главная функция"""
    try:
        finder = SimpleCasinoAPIFinder()
        finder.run()
        print("\n👋 До свидания! Удачи в поиске API!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Поиск прерван пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()