"""
УНИВЕРСАЛЬНЫЙ СБОРЩИК API ИЗ БРАУЗЕРА
====================================

Этот инструмент поможет настроить любой найденный API
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path

class UniversalAPISetup:
    """Универсальная настройка API"""
    
    def __init__(self):
        self.config = {}
    
    def setup_multiple_casinos(self):
        """Настройка нескольких казино"""
        print("🎰 УПРАВЛЕНИЕ НЕСКОЛЬКИМИ КАЗИНО")
        print("=" * 32)
        
        print("""
У вас уже настроено:
✅ Paddy Power + Pragmatic Play Live (paddypower_config.json)
   • Рабочие API с авторизацией
   • История рулетки (500 игр)
   • Реальные данные
   
🆕 Новое казино: Spin and Go Roulette
   • Нужно найти API в браузере
   • Скопировать запросы из Network tab
        """)
        
        choice = input("\nЧто вы хотите сделать?\n1. Использовать Paddy Power (уже работает)\n2. Настроить Spin and Go\n3. Добавить новое казино\nВыбор (1-3): ").strip()
        
        if choice == '1':
            self.use_paddypower()
        elif choice == '2':
            self.setup_spinandgo()  
        elif choice == '3':
            self.setup_new_casino()
        else:
            print("❌ Неверный выбор")
    
    def use_paddypower(self):
        """Используем Paddy Power"""
        print("\n✅ ИСПОЛЬЗУЕМ PADDY POWER")
        print("-" * 23)
        
        try:
            # Копируем конфигурацию Paddy Power
            import shutil
            shutil.copy("paddypower_config.json", "casino_setup.json")
            
            print("✅ Конфигурация Paddy Power активирована")
            print("🎯 Система настроена на работу с одним столом: roulettestura541")
            
            print("\n📋 ГОТОВО К ИСПОЛЬЗОВАНИЮ:")
            print("1. python test_connection.py - проверить подключение")
            print("2. python src/main.py - запустить систему")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def setup_spinandgo(self):
        """Настройка Spin and Go"""
        print("\n🎯 НАСТРОЙКА SPIN AND GO ROULETTE")
        print("-" * 33)
        
        print("""
ИНСТРУКЦИИ ДЛЯ SPIN AND GO:

1. 🌐 Откройте в браузере:
   https://casinopp-com-ngm.bfcdl.com/livedistributed/25.9.3.0/?game=sgrol&launch_alias=sgrol_spinandgorol&language=EN

2. 🔧 Откройте Developer Tools (F12)
   • Перейдите на вкладку Network
   • Поставьте фильтр XHR/Fetch

3. 🎰 Поиграйте несколько минут
   • Подождите несколько спинов
   • Наблюдайте за запросами

4. 📋 Найдите запросы с данными рулетки
   • Ищите URL содержащие: result, history, spin, game
   • Копируйте полный URL и заголовки
        """)
        
        manual_setup = input("\nНашли API в браузере? (y/n): ").lower()
        if manual_setup == 'y':
            self.collect_manual_api_info("Spin and Go Roulette")
        else:
            print("💡 Вернитесь к настройке когда найдете API в браузере")
    
    def setup_new_casino(self):
        """Настройка нового казино"""
        print("\n🆕 НАСТРОЙКА НОВОГО КАЗИНО")
        print("-" * 24)
        
        casino_name = input("Название казино: ").strip()
        casino_url = input("URL казино: ").strip()
        
        if casino_name and casino_url:
            self.collect_manual_api_info(casino_name, casino_url)
        else:
            print("❌ Нужно указать название и URL")
    
    def collect_manual_api_info(self, casino_name, casino_url=""):
        """Сбор информации об API вручную"""
        print(f"\n📝 НАСТРОЙКА API ДЛЯ {casino_name.upper()}")
        print("=" * (15 + len(casino_name)))
        
        endpoints = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        print("🔗 ДОБАВЛЕНИЕ API ENDPOINTS")
        print("Введите найденные API URLs (по одному, Enter для завершения):")
        
        counter = 1
        while True:
            url = input(f"API URL #{counter} (или Enter для завершения): ").strip()
            if not url:
                break
            
            # Определяем тип API
            print("Что возвращает этот API?")
            print("1. История результатов рулетки")
            print("2. Текущие/live результаты")
            print("3. Конфигурация стола")
            print("4. Другое")
            
            api_type = input("Тип API (1-4): ").strip()
            
            type_names = {
                '1': 'history',
                '2': 'live_results', 
                '3': 'table_config',
                '4': f'api_{counter}'
            }
            
            endpoint_name = type_names.get(api_type, f'api_{counter}')
            
            # Проверяем, нужны ли дополнительные заголовки
            needs_auth = input("API требует специальные заголовки? (y/n): ").lower() == 'y'
            
            endpoint_info = {
                'url': url,
                'method': 'GET',
                'description': f'API endpoint {counter}'
            }
            
            if needs_auth:
                auth_header = input("Authorization header (если есть): ").strip()
                session_header = input("Session/Cookie header (если есть): ").strip()
                
                if auth_header:
                    headers['Authorization'] = auth_header
                if session_header:
                    headers['Cookie'] = session_header
            
            endpoints[endpoint_name] = endpoint_info
            print(f"✅ Добавлен: {endpoint_name} -> {url}")
            counter += 1
        
        if endpoints:
            # Создаем конфигурацию
            config = {
                "casino_name": casino_name,
                "casino_url": casino_url,
                "connection_method": "api",
                "api": {
                    "base_url": self.extract_base_url(casino_url) if casino_url else "",
                    "endpoints": endpoints,
                    "headers": headers
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
            
            # Сохраняем конфигурацию
            filename = f"{casino_name.lower().replace(' ', '_')}_config.json"
            self.save_config(config, filename)
            
            # Тестируем API
            test_choice = input(f"\nПротестировать API сейчас? (y/n): ").lower()
            if test_choice == 'y':
                self.test_manual_config(config)
            
            print(f"\n🎉 КОНФИГУРАЦИЯ СОЗДАНА!")
            print(f"📁 Файл: {filename}")
            
            # Предлагаем активировать
            activate = input("Активировать эту конфигурацию? (y/n): ").lower()
            if activate == 'y':
                import shutil
                shutil.copy(filename, "casino_setup.json")
                print("✅ Конфигурация активирована")
        else:
            print("❌ Не добавлено ни одного API")
    
    def test_manual_config(self, config):
        """Тестируем ручную конфигурацию"""
        print("\n🧪 ТЕСТИРОВАНИЕ API")
        print("-" * 16)
        
        for name, endpoint in config['api']['endpoints'].items():
            print(f"\n🔍 Тестирую {name}...")
            
            try:
                req = urllib.request.Request(endpoint['url'])
                
                # Добавляем заголовки
                for header, value in config['api']['headers'].items():
                    req.add_header(header, value)
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    status_code = response.getcode()
                    content_type = response.headers.get('Content-Type', '')
                    data = response.read(300).decode('utf-8', errors='ignore')
                    
                    if status_code == 200:
                        print(f"   ✅ HTTP {status_code} - {content_type}")
                        print(f"   📄 Данные: {data[:100]}...")
                        
                        # Проверяем на рулеточные данные
                        if self.contains_roulette_data(data):
                            print(f"   🎰 СОДЕРЖИТ ДАННЫЕ РУЛЕТКИ!")
                    else:
                        print(f"   ⚠️ HTTP {status_code}")
                        
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
    
    def contains_roulette_data(self, data):
        """Проверяет наличие данных рулетки"""
        indicators = ['roulette', 'wheel', 'spin', 'number', 'red', 'black', 'winning', 'result']
        data_lower = data.lower()
        return sum(1 for indicator in indicators if indicator in data_lower) >= 2
    
    def extract_base_url(self, url):
        """Извлекает базовый URL"""
        if '://' in url:
            parts = url.split('/')
            return '/'.join(parts[:3])
        return url
    
    def save_config(self, config, filename):
        """Сохраняет конфигурацию"""
        try:
            config_path = Path(__file__).parent / filename
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"💾 Конфигурация сохранена в {filename}")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def show_current_status(self):
        """Показывает текущий статус"""
        print("📊 ТЕКУЩИЙ СТАТУС СИСТЕМЫ")
        print("=" * 25)
        
        # Проверяем существующие конфигурации
        config_files = [
            ("casino_setup.json", "Активная конфигурация"),
            ("paddypower_config.json", "Paddy Power + Pragmatic Play"),
            ("spinandgo_config.json", "Spin and Go Roulette")
        ]
        
        for file, description in config_files:
            if Path(file).exists():
                print(f"✅ {file} - {description}")
            else:
                print(f"❌ {file} - {description} (не найден)")
        
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        if Path("paddypower_config.json").exists():
            print(f"• Используйте Paddy Power API - он уже работает!")
            print(f"• Команда: python test_connection.py")
        else:
            print(f"• Настройте API через браузер (F12 → Network)")
            print(f"• Скопируйте найденные запросы в эту систему")
    
    def run(self):
        """Запуск системы"""
        print("🎰 УНИВЕРСАЛЬНЫЙ СБОРЩИК API")
        print("=" * 28)
        
        # Показываем статус
        self.show_current_status()
        
        # Предлагаем варианты
        self.setup_multiple_casinos()


def main():
    """Главная функция"""
    try:
        setup = UniversalAPISetup()
        setup.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Настройка прервана")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()