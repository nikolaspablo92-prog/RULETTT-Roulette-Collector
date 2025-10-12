"""
БЫСТРАЯ НАСТРОЙКА API ИЗ КОНСОЛИ БРАУЗЕРА
=========================================

Этот скрипт помогает быстро настроить API казино
используя данные из консоли браузера.
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path

class QuickAPISetup:
    """Быстрая настройка API из браузера"""
    
    def __init__(self):
        self.config = {}
    
    def run(self):
        """Запуск быстрой настройки"""
        print("⚡ БЫСТРАЯ НАСТРОЙКА API ИЗ БРАУЗЕРА")
        print("=" * 38)
        
        print("""
ШАГИ ДЛЯ ПОИСКА API В БРАУЗЕРЕ:

1. 🌐 Откройте live-рулетку в браузере
2. 🔧 Нажмите F12 → вкладка Network
3. 🎯 Поставьте фильтр XHR/Fetch  
4. 🎰 Понаблюдайте за игрой 2-3 минуты
5. 📋 Найдите запросы с данными рулетки

ТИПИЧНЫЕ НАЗВАНИЯ API:
• live_results, game_history, roulette_data
• api/games/, live/, results/
• websocket соединения
        """)
        
        choice = input("Готовы к настройке? (y/n): ").lower()
        if choice != 'y':
            print("👋 До свидания!")
            return
        
        # Собираем информацию
        self.collect_api_info()
        self.create_config()
        self.test_config()
        self.show_next_steps()
    
    def collect_api_info(self):
        """Собираем информацию об API"""
        print("\n📝 ВВОД ИНФОРМАЦИИ ОБ API")
        print("-" * 26)
        
        # Основная информация
        casino_name = input("Название казино: ").strip()
        casino_url = input("URL сайта казино: ").strip()
        
        # Собираем API endpoints
        print("\n🔗 API ENDPOINTS")
        print("Введите найденные API URLs (по одному, Enter для завершения):")
        
        endpoints = {}
        counter = 1
        
        while True:
            url = input(f"API URL #{counter} (или Enter для завершения): ").strip()
            if not url:
                break
            
            # Определяем назначение API
            print("Что возвращает этот API?")
            print("1. Текущие результаты рулетки")
            print("2. История игр") 
            print("3. Информация о столах")
            print("4. Другое")
            
            api_type = input("Выберите тип (1-4): ").strip()
            
            type_names = {
                '1': 'live_results',
                '2': 'history', 
                '3': 'tables',
                '4': 'other'
            }
            
            endpoint_name = type_names.get(api_type, 'api_' + str(counter))
            endpoints[endpoint_name] = url
            
            print(f"✅ Добавлен: {endpoint_name} -> {url}")
            counter += 1
        
        # Дополнительные параметры
        print("\n🔐 ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ")
        needs_auth = input("API требует авторизацию? (y/n): ").lower() == 'y'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        if needs_auth:
            auth_header = input("Authorization header (если есть): ").strip()
            if auth_header:
                headers['Authorization'] = auth_header
        
        # Сохраняем в конфигурацию
        self.config = {
            'casino_name': casino_name,
            'casino_url': casino_url,
            'connection_method': 'api',
            'api': {
                'base_url': self.extract_base_url(casino_url),
                'endpoints': endpoints,
                'headers': headers,
                'timeout': 10
            },
            'betting': {
                'base_bet': 100,
                'max_bet': 10000,
                'bankroll': 100000
            },
            'safety': {
                'enabled': True,
                'max_daily_loss': 50000
            }
        }
        
        print(f"\n✅ Конфигурация создана для {casino_name}")
        print(f"   🔗 {len(endpoints)} API endpoints")
        print(f"   🔐 Авторизация: {'Да' if needs_auth else 'Нет'}")
    
    def create_config(self):
        """Создаем и сохраняем конфигурацию"""
        print("\n💾 СОХРАНЕНИЕ КОНФИГУРАЦИИ")
        print("-" * 23)
        
        try:
            config_path = Path("casino_setup.json")
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Конфигурация сохранена в {config_path}")
            
            # Показываем что сохранили
            print("\n📋 СОХРАНЕННАЯ КОНФИГУРАЦИЯ:")
            print(f"   Казино: {self.config['casino_name']}")
            print(f"   URL: {self.config['casino_url']}")
            print(f"   Endpoints:")
            for name, url in self.config['api']['endpoints'].items():
                print(f"     • {name}: {url}")
                
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def test_config(self):
        """Тестируем созданную конфигурацию"""
        print("\n🧪 ТЕСТИРОВАНИЕ API")
        print("-" * 16)
        
        test_choice = input("Протестировать API сейчас? (y/n): ").lower()
        if test_choice != 'y':
            print("⏭️ Тестирование пропущено")
            return
        
        # Тестируем каждый endpoint
        for name, url in self.config['api']['endpoints'].items():
            print(f"\n🔍 Тестирую {name}...")
            
            try:
                # Создаем запрос с заголовками
                req = urllib.request.Request(url)
                for header, value in self.config['api']['headers'].items():
                    req.add_header(header, value)
                
                # Выполняем запрос
                with urllib.request.urlopen(req, timeout=5) as response:
                    status_code = response.getcode()
                    content_type = response.headers.get('Content-Type', '')
                    
                    if status_code == 200:
                        print(f"   ✅ {name}: HTTP {status_code}, {content_type}")
                        
                        # Читаем небольшую часть ответа
                        data = response.read(500).decode('utf-8', errors='ignore')
                        if data:
                            print(f"   📄 Данные: {data[:100]}...")
                            
                            # Проверяем на JSON
                            if 'json' in content_type.lower():
                                try:
                                    json.loads(data)
                                    print("   📊 Формат: Валидный JSON")
                                except:
                                    print("   ⚠️ Формат: Не JSON или поврежден")
                    else:
                        print(f"   ⚠️ {name}: HTTP {status_code}")
                        
            except urllib.error.HTTPError as e:
                print(f"   ❌ {name}: HTTP {e.code} - {e.reason}")
            except urllib.error.URLError as e:
                print(f"   ❌ {name}: Ошибка соединения - {e.reason}")
            except Exception as e:
                print(f"   ❌ {name}: {e}")
        
        print("\n✅ Тестирование завершено")
    
    def show_next_steps(self):
        """Показываем следующие шаги"""
        print("\n🎯 СЛЕДУЮЩИЕ ШАГИ")
        print("-" * 14)
        
        print("""
ФАЙЛЫ СОЗДАНЫ:
✅ casino_setup.json - конфигурация казино

ЧТО ДЕЛАТЬ ДАЛЬШЕ:

1. 🧪 ДЕТАЛЬНОЕ ТЕСТИРОВАНИЕ:
   python test_connection.py
   
2. 🚀 ЗАПУСК СИСТЕМЫ:
   python src/main.py
   
3. 📊 В МЕНЮ ВЫБЕРИТЕ:
   "Получить реальные данные"
   
4. 📈 АНАЛИЗ И СТРАТЕГИИ:
   Система автоматически использует ваши API
   для получения реальных данных рулетки

ПОЛЕЗНЫЕ КОМАНДЫ:
• python simple_api_finder.py - поиск новых API
• python setup_casino.py - изменить настройки
• python src/main.py - основная система
        """)
        
        print("🎉 Быстрая настройка завершена!")
        print("💡 Если API не работают, проверьте Network tab в браузере еще раз")
    
    def extract_base_url(self, url):
        """Извлекаем базовый URL"""
        if not url:
            return ""
        
        if '://' in url:
            parts = url.split('/')
            return '/'.join(parts[:3])
        
        return url


def main():
    """Главная функция"""
    try:
        setup = QuickAPISetup()
        setup.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Настройка прервана")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()