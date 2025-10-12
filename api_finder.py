"""
ПОИСКОВИК И ТЕСТЕР API КАЗИНО
============================

Помогает найти и протестировать API различных казино.
"""

import requests
import json
import time
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional

class CasinoAPIFinder:
    """Поисковик API казино"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Известные казино с потенциальными API
        self.known_casinos = {
            'stake': {
                'name': 'Stake.com',
                'base_url': 'https://stake.com',
                'potential_endpoints': [
                    '/api/v1/casino/games/history',
                    '/api/v1/live/roulette',
                    '/_api/graphql'
                ],
                'description': 'Крупное криптовалютное казино'
            },
            'bc_game': {
                'name': 'BC.Game',
                'base_url': 'https://bc.game',
                'potential_endpoints': [
                    '/api/casino/roulette/history',
                    '/api/v1/live-games'
                ],
                'description': 'Криптовалютное казино с API'
            },
            'roobet': {
                'name': 'Roobet',
                'base_url': 'https://roobet.com',
                'potential_endpoints': [
                    '/api/casino/roulette',
                    '/api/games/live'
                ],
                'description': 'Популярное онлайн казино'
            }
        }
    
    def run_search(self):
        """Запуск поиска API"""
        print("🔍 ПОИСК API КАЗИНО")
        print("=" * 25)
        
        print("Выберите действие:")
        print("1. Тестировать известные казино")
        print("2. Проверить конкретный URL")
        print("3. Поиск endpoints на сайте")
        print("4. Анализ сетевого трафика")
        print("0. Выход")
        
        choice = input("\nВыбор (0-4): ").strip()
        
        if choice == "1":
            self.test_known_casinos()
        elif choice == "2":
            self.test_custom_url()
        elif choice == "3":
            self.search_endpoints()
        elif choice == "4":
            self.show_network_analysis_guide()
        elif choice == "0":
            return
        else:
            print("Неверный выбор")
    
    def test_known_casinos(self):
        """Тестирование известных казино"""
        print("\n🎰 ТЕСТИРОВАНИЕ ИЗВЕСТНЫХ КАЗИНО")
        print("-" * 35)
        
        for casino_id, casino_info in self.known_casinos.items():
            print(f"\n📍 {casino_info['name']}")
            print(f"   {casino_info['description']}")
            
            for endpoint in casino_info['potential_endpoints']:
                url = casino_info['base_url'] + endpoint
                result = self.test_endpoint(url)
                
                status_icon = "✅" if result.get('accessible') else "❌"
                print(f"   {status_icon} {endpoint} - {result.get('status', 'Ошибка')}")
                
                if result.get('data'):
                    print(f"      📊 Найдены данные: {len(str(result['data']))} символов")
                
                time.sleep(1)  # Пауза между запросами
    
    def test_custom_url(self):
        """Тестирование пользовательского URL"""
        print("\n🔗 ТЕСТИРОВАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО URL")
        print("-" * 40)
        
        base_url = input("Введите базовый URL казино (например, https://casino.com): ").strip()
        
        if not base_url:
            print("❌ URL не введен")
            return
        
        # Добавляем протокол если не указан
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
        
        # Стандартные endpoints для поиска
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
            '/api/v1/casino/games',
            '/api/v1/live/games',
            '/_api',
            '/rest/api',
            '/graphql'
        ]
        
        print(f"\n🔍 Поиск API endpoints на {base_url}")
        
        found_endpoints = []
        
        for endpoint in common_endpoints:
            url = base_url + endpoint
            result = self.test_endpoint(url)
            
            if result.get('accessible'):
                found_endpoints.append((endpoint, result))
                print(f"✅ {endpoint} - {result.get('status')}")
                
                # Показываем краткую информацию о данных
                if result.get('data'):
                    data_preview = str(result['data'])[:100]
                    print(f"   📊 Данные: {data_preview}...")
            else:
                print(f"❌ {endpoint} - {result.get('status', 'Недоступен')}")
            
            time.sleep(0.5)  # Короткая пауза
        
        if found_endpoints:
            print(f"\n🎯 НАЙДЕНО {len(found_endpoints)} ДОСТУПНЫХ ENDPOINTS:")
            for endpoint, result in found_endpoints:
                print(f"   • {base_url}{endpoint}")
        else:
            print("\n😞 API endpoints не найдены")
            print("💡 Попробуйте:")
            print("   1. Проверить документацию сайта")
            print("   2. Использовать анализ сетевого трафика")
            print("   3. Связаться с технической поддержкой")
    
    def search_endpoints(self):
        """Поиск endpoints на сайте"""
        print("\n🕷️ ПОИСК ENDPOINTS НА САЙТЕ")
        print("-" * 30)
        
        url = input("Введите URL страницы для анализа: ").strip()
        
        if not url:
            print("❌ URL не введен")
            return
        
        try:
            response = self.session.get(url, timeout=10)
            content = response.text
            
            # Поиск потенциальных API endpoints в коде
            import re
            
            # Паттерны для поиска API endpoints
            patterns = [
                r'["\']https?://[^"\']*api[^"\']*["\']',
                r'["\'][^"\']*api[^"\']*["\']',
                r'["\']https?://[^"\']*roulette[^"\']*["\']',
                r'endpoint["\']?\s*:\s*["\'][^"\']*["\']',
                r'url["\']?\s*:\s*["\'][^"\']*api[^"\']*["\']'
            ]
            
            found_urls = set()
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Очищаем от кавычек
                    clean_url = match.strip('"\'')
                    if 'api' in clean_url.lower() or 'roulette' in clean_url.lower():
                        found_urls.add(clean_url)
            
            if found_urls:
                print(f"\n🎯 НАЙДЕНО {len(found_urls)} ПОТЕНЦИАЛЬНЫХ ENDPOINTS:")
                for found_url in sorted(found_urls):
                    print(f"   • {found_url}")
                    
                # Предлагаем протестировать найденные URL
                if input("\nПротестировать найденные endpoints? (y/n): ").lower() == 'y':
                    for found_url in list(found_urls)[:5]:  # Тестируем первые 5
                        result = self.test_endpoint(found_url)
                        status = "✅" if result.get('accessible') else "❌"
                        print(f"{status} {found_url} - {result.get('status', 'Ошибка')}")
                        time.sleep(1)
            else:
                print("😞 API endpoints в коде страницы не найдены")
        
        except Exception as e:
            print(f"❌ Ошибка при анализе страницы: {e}")
    
    def test_endpoint(self, url: str) -> Dict:
        """Тестирование конкретного endpoint"""
        try:
            response = self.session.get(url, timeout=10)
            
            result = {
                'url': url,
                'status': response.status_code,
                'accessible': response.status_code < 400
            }
            
            # Пытаемся парсить JSON
            try:
                data = response.json()
                result['data'] = data
                result['content_type'] = 'json'
            except:
                result['data'] = response.text[:200] if response.text else None
                result['content_type'] = response.headers.get('content-type', 'unknown')
            
            return result
            
        except requests.exceptions.Timeout:
            return {'url': url, 'status': 'Timeout', 'accessible': False}
        except requests.exceptions.ConnectionError:
            return {'url': url, 'status': 'Connection Error', 'accessible': False}
        except Exception as e:
            return {'url': url, 'status': f'Error: {str(e)}', 'accessible': False}
    
    def show_network_analysis_guide(self):
        """Показать руководство по анализу сетевого трафика"""
        print("\n🌐 АНАЛИЗ СЕТЕВОГО ТРАФИКА")
        print("-" * 30)
        print("""
1. Откройте браузер (Chrome/Firefox)
2. Нажмите F12 (Developer Tools)
3. Перейдите на вкладку "Network" (Сеть)
4. Откройте страницу live рулетки
5. Играйте или наблюдайте за игрой
6. Ищите запросы типа:
   • XHR/Fetch
   • WebSocket connections
   • С названиями содержащими: api, roulette, live, games

7. Кликните на интересный запрос
8. Посмотрите:
   • Request URL
   • Headers
   • Response

ВАЖНО:
⚠️ Не злоупотребляйте найденными endpoints
⚠️ Соблюдайте Terms of Service сайта
⚠️ Добавляйте задержки между запросами
        """)
    
    def save_findings(self, findings: List[Dict]):
        """Сохранить найденные API"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"found_apis_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(findings, f, indent=2, ensure_ascii=False)
            print(f"💾 Результаты сохранены в {filename}")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")


def main():
    """Главная функция"""
    print("🎰 ПОИСКОВИК API КАЗИНО")
    print("=" * 30)
    print("Поможет найти и протестировать API различных казино")
    print("для получения данных рулетки.\n")
    
    finder = CasinoAPIFinder()
    
    while True:
        try:
            finder.run_search()
            
            if input("\nПродолжить поиск? (y/n): ").lower() != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Поиск прерван пользователем")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
    
    print("\n🎯 Поиск завершен!")
    print("💡 Не забудьте проверить найденные API на соответствие ToS")


if __name__ == "__main__":
    main()