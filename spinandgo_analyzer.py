"""
АНАЛИЗАТОР НОВЫХ API ENDPOINTS
=============================

Анализирует новые найденные API endpoints для рулетки
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path
import re

class NewAPIAnalyzer:
    """Анализатор новых API endpoints"""
    
    def __init__(self):
        self.found_endpoints = []
        
    def analyze_spin_and_go_url(self, url):
        """Анализируем URL Spin and Go Roulette"""
        print("🎯 АНАЛИЗ SPIN AND GO ROULETTE URL")
        print("=" * 35)
        
        print(f"🔗 URL: {url}")
        
        # Парсим URL
        parsed = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        print(f"\n📋 ИНФОРМАЦИЯ О URL:")
        print(f"   Домен: {parsed.netloc}")
        print(f"   Путь: {parsed.path}")
        print(f"   Игра: {query_params.get('game', ['неизвестно'])[0]}")
        print(f"   Алиас: {query_params.get('launch_alias', ['неизвестно'])[0]}")
        print(f"   Язык: {query_params.get('language', ['неизвестно'])[0]}")
        
        # Извлекаем базовые данные
        base_info = {
            'domain': parsed.netloc,
            'game_type': query_params.get('game', [''])[0],
            'launch_alias': query_params.get('launch_alias', [''])[0],
            'language': query_params.get('language', ['EN'])[0],
            'base_url': f"{parsed.scheme}://{parsed.netloc}"
        }
        
        return base_info
    
    def find_potential_api_endpoints(self, base_info):
        """Ищем потенциальные API endpoints"""
        print("\n🔍 ПОИСК ПОТЕНЦИАЛЬНЫХ API ENDPOINTS")
        print("=" * 38)
        
        base_url = base_info['base_url']
        game_type = base_info['game_type']
        
        # Типичные паттерны API для live-казино
        potential_endpoints = [
            f"{base_url}/api/game/{game_type}/history",
            f"{base_url}/api/game/{game_type}/results",
            f"{base_url}/api/game/{game_type}/current",
            f"{base_url}/api/live/{game_type}/status",
            f"{base_url}/api/live/results",
            f"{base_url}/api/roulette/history",
            f"{base_url}/api/roulette/results",
            f"{base_url}/live/api/game_data",
            f"{base_url}/live/api/history",
            f"{base_url}/gameapi/history",
            f"{base_url}/gameapi/results",
            f"{base_url}/ws/game/{game_type}",  # WebSocket endpoint
        ]
        
        print("🎯 ПОТЕНЦИАЛЬНЫЕ ENDPOINTS:")
        for i, endpoint in enumerate(potential_endpoints, 1):
            print(f"   {i:2d}. {endpoint}")
        
        return potential_endpoints
    
    def test_endpoints(self, endpoints):
        """Тестируем найденные endpoints"""
        print("\n🧪 ТЕСТИРОВАНИЕ ENDPOINTS")
        print("=" * 25)
        
        working_endpoints = []
        
        for endpoint in endpoints:
            print(f"\n🔍 Тестирую: {endpoint}")
            
            try:
                req = urllib.request.Request(endpoint)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                req.add_header('Accept', 'application/json, text/plain, */*')
                req.add_header('Accept-Language', 'en-US,en;q=0.9')
                
                with urllib.request.urlopen(req, timeout=5) as response:
                    status_code = response.getcode()
                    content_type = response.headers.get('Content-Type', '')
                    
                    if status_code == 200:
                        data = response.read(500).decode('utf-8', errors='ignore')
                        print(f"   ✅ HTTP {status_code} - {content_type}")
                        print(f"   📄 Данные: {data[:100]}...")
                        
                        working_endpoints.append({
                            'url': endpoint,
                            'status': status_code,
                            'content_type': content_type,
                            'data_preview': data[:200]
                        })
                    else:
                        print(f"   ⚠️ HTTP {status_code}")
                        
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"   ❌ 404 - Не найден")
                elif e.code == 403:
                    print(f"   🔐 403 - Доступ запрещен")
                elif e.code == 401:
                    print(f"   🔑 401 - Требуется авторизация")
                else:
                    print(f"   ❌ HTTP {e.code}")
                    
            except urllib.error.URLError as e:
                print(f"   ❌ Ошибка соединения: {e.reason}")
                
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        return working_endpoints
    
    def analyze_main_page(self, url):
        """Анализируем главную страницу игры"""
        print("\n📄 АНАЛИЗ ГЛАВНОЙ СТРАНИЦЫ")
        print("=" * 26)
        
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    content = response.read().decode('utf-8', errors='ignore')
                    
                    print(f"✅ Страница загружена ({len(content)} символов)")
                    
                    # Ищем API endpoints в коде страницы
                    api_patterns = [
                        r'["\']([^"\']*api[^"\']*)["\']',
                        r'["\']([^"\']*\/ws\/[^"\']*)["\']',
                        r'["\']([^"\']*websocket[^"\']*)["\']',
                        r'["\']([^"\']*results?[^"\']*)["\']',
                        r'["\']([^"\']*history[^"\']*)["\']',
                    ]
                    
                    found_apis = set()
                    for pattern in api_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if ('api' in match.lower() or 'ws' in match.lower() or 
                                'result' in match.lower() or 'history' in match.lower()):
                                found_apis.add(match)
                    
                    if found_apis:
                        print(f"\n🎯 НАЙДЕННЫЕ API В КОДЕ СТРАНИЦЫ:")
                        for api in sorted(found_apis)[:10]:  # Показываем первые 10
                            print(f"   • {api}")
                        
                        return list(found_apis)
                    else:
                        print("❌ API endpoints в коде не найдены")
                        return []
                        
                else:
                    print(f"❌ Ошибка загрузки: HTTP {response.getcode()}")
                    return []
                    
        except Exception as e:
            print(f"❌ Ошибка анализа страницы: {e}")
            return []
    
    def create_config_for_new_casino(self, base_info, working_endpoints):
        """Создаем конфигурацию для нового казино"""
        print("\n⚙️ СОЗДАНИЕ КОНФИГУРАЦИИ")
        print("=" * 24)
        
        if not working_endpoints:
            print("❌ Нет рабочих endpoints для конфигурации")
            return None
        
        config = {
            "casino_name": f"Spin and Go Roulette ({base_info['domain']})",
            "connection_method": "api",
            "api": {
                "base_url": base_info['base_url'],
                "endpoints": {},
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.9"
                }
            },
            "game_info": {
                "game_type": base_info['game_type'],
                "launch_alias": base_info['launch_alias'],
                "language": base_info['language']
            },
            "betting": {
                "base_bet": 100,
                "max_bet": 10000,
                "bankroll": 100000
            },
            "safety": {
                "enabled": True,
                "max_daily_loss": 50000
            }
        }
        
        # Добавляем рабочие endpoints
        for i, endpoint in enumerate(working_endpoints):
            endpoint_name = f"endpoint_{i+1}"
            config['api']['endpoints'][endpoint_name] = {
                'url': endpoint['url'],
                'method': 'GET',
                'content_type': endpoint['content_type'],
                'description': f'Working endpoint {i+1}'
            }
        
        # Сохраняем конфигурацию
        try:
            config_path = Path(__file__).parent / "spinandgo_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Конфигурация сохранена в {config_path}")
            return config
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return None
    
    def run(self, url):
        """Запуск анализа"""
        print("🎯 АНАЛИЗАТОР НОВЫХ API ENDPOINTS")
        print("=" * 33)
        
        # Анализируем URL
        base_info = self.analyze_spin_and_go_url(url)
        
        # Ищем потенциальные endpoints
        potential_endpoints = self.find_potential_api_endpoints(base_info)
        
        # Тестируем endpoints
        working_endpoints = self.test_endpoints(potential_endpoints)
        
        # Анализируем главную страницу
        page_apis = self.analyze_main_page(url)
        
        # Если нашли API в коде страницы, тестируем их тоже
        if page_apis:
            print(f"\n🧪 ТЕСТИРОВАНИЕ API ИЗ КОДА СТРАНИЦЫ")
            print("=" * 35)
            
            # Дополняем относительные URL
            full_page_apis = []
            for api in page_apis[:5]:  # Тестируем первые 5
                if api.startswith('/'):
                    full_page_apis.append(base_info['base_url'] + api)
                elif api.startswith('http'):
                    full_page_apis.append(api)
            
            if full_page_apis:
                page_working = self.test_endpoints(full_page_apis)
                working_endpoints.extend(page_working)
        
        # Создаем конфигурацию
        if working_endpoints:
            config = self.create_config_for_new_casino(base_info, working_endpoints)
            
            if config:
                print(f"\n🎉 АНАЛИЗ ЗАВЕРШЕН!")
                print(f"✅ Найдено {len(working_endpoints)} рабочих endpoints")
                print(f"📁 Конфигурация: spinandgo_config.json")
                
                print(f"\n📋 СЛЕДУЮЩИЕ ШАГИ:")
                print(f"1. cp spinandgo_config.json casino_setup.json")
                print(f"2. python test_connection.py")
                print(f"3. python src/main.py")
            else:
                print(f"\n😞 Не удалось создать конфигурацию")
        else:
            print(f"\n😞 Рабочие endpoints не найдены")
            print(f"💡 Попробуйте:")
            print(f"   • Проверить Network tab в браузере")
            print(f"   • Поискать WebSocket соединения")
            print(f"   • Использовать другой стол/провайдер")


def main():
    """Главная функция"""
    # URL который предоставил пользователь
    spin_and_go_url = "https://casinopp-com-ngm.bfcdl.com/livedistributed/25.9.3.0/?game=sgrol&launch_alias=sgrol_spinandgorol&language=EN&redirect_time=1760063327593&backUrl=https%3A%2F%2Fcasinopp-com-ngm.bfcdl.com%2Flive%2F%3Fgame%3Dsgrol%26launch_alias%3Dsgrol_spinandgorol%26language%3DEN&_entry=live"
    
    try:
        analyzer = NewAPIAnalyzer()
        analyzer.run(spin_and_go_url)
        
    except KeyboardInterrupt:
        print("\n\n👋 Анализ прерван пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()