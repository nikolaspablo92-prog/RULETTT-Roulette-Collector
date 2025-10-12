"""
МАСТЕР НАСТРОЙКИ ДЛЯ ПОДКЛЮЧЕНИЯ К РЕАЛЬНОМУ КАЗИНО
=================================================

Эта утилита поможет настроить систему для работы с вашим казино.
"""

import json
import os
from pathlib import Path

class CasinoSetupWizard:
    """Мастер настройки казино"""
    
    def __init__(self):
        self.config = {}
        self.setup_path = Path(__file__).parent / "casino_setup.json"
    
    def run(self):
        """Запуск мастера настройки"""
        print("🎰 МАСТЕР НАСТРОЙКИ ПОДКЛЮЧЕНИЯ К КАЗИНО")
        print("=" * 50)
        
        self.setup_basic_info()
        self.setup_connection_method()
        self.setup_betting_config()
        self.setup_safety_limits()
        self.save_config()
        self.show_next_steps()
    
    def setup_basic_info(self):
        """Настройка базовой информации"""
        print("\n📋 БАЗОВЫЕ НАСТРОЙКИ")
        print("-" * 25)
        
        self.config['casino_name'] = input("Название казино: ").strip() or "Мое Казино"
        self.config['currency'] = input("Валюта (RUB/USD/EUR): ").strip().upper() or "RUB"
        
        timezone = input("Часовой пояс (Europe/Moscow): ").strip() or "Europe/Moscow"
        self.config['timezone'] = timezone
        
        print(f"✅ Настроено: {self.config['casino_name']} ({self.config['currency']})")
    
    def setup_connection_method(self):
        """Настройка метода подключения"""
        print("\n🔗 МЕТОД ПОЛУЧЕНИЯ ДАННЫХ")
        print("-" * 30)
        print("1. Ручной ввод результатов (простой)")
        print("2. API казино (автоматический)")
        print("3. Веб-скрапинг (продвинутый)")
        print("4. Импорт из CSV файла (разовый)")
        print("5. Тестовые данные (для обучения)")
        
        choice = input("Выберите метод (1-5): ").strip()
        
        methods = {
            "1": "manual",
            "2": "api", 
            "3": "scraping",
            "4": "csv_import",
            "5": "mock"
        }
        
        method = methods.get(choice, "manual")
        self.config['connection_method'] = method
        
        if method == "api":
            self.setup_api_config()
        elif method == "scraping":
            self.setup_scraping_config()
        elif method == "csv_import":
            self.setup_csv_config()
        
        print(f"✅ Выбран метод: {method}")
    
    def setup_api_config(self):
        """Настройка API"""
        print("\n📡 НАСТРОЙКА API")
        print("-" * 20)
        
        api_url = input("URL API (https://api.casino.com): ").strip()
        api_key = input("API ключ: ").strip()
        
        self.config['api'] = {
            'base_url': api_url,
            'api_key': api_key,
            'endpoints': {
                'live_results': input("Endpoint для живых результатов (/roulette/live): ").strip() or "/roulette/live",
                'history': input("Endpoint для истории (/roulette/history): ").strip() or "/roulette/history"
            }
        }
    
    def setup_scraping_config(self):
        """Настройка веб-скрапинга"""
        print("\n🕷️ НАСТРОЙКА ВЕБ-СКРАПИНГА")
        print("-" * 30)
        print("⚠️ ВНИМАНИЕ: Убедитесь что скрапинг разрешен правилами сайта!")
        
        site_url = input("URL сайта казино: ").strip()
        live_page = input("Страница с живой рулеткой: ").strip()
        
        print("\nCSS селекторы для элементов:")
        number_selector = input("Селектор для числа (.roulette-number): ").strip() or ".roulette-number"
        time_selector = input("Селектор для времени (.result-time): ").strip() or ".result-time"
        
        self.config['scraping'] = {
            'base_url': site_url,
            'live_page': live_page,
            'selectors': {
                'number': number_selector,
                'timestamp': time_selector
            }
        }
    
    def setup_csv_config(self):
        """Настройка импорта CSV"""
        print("\n📄 НАСТРОЙКА ИМПОРТА CSV")
        print("-" * 25)
        
        csv_path = input("Путь к CSV файлу: ").strip()
        
        print("Формат CSV (столбцы):")
        print("1. timestamp,number")
        print("2. date,time,number")
        print("3. timestamp,number,color")
        
        format_choice = input("Выберите формат (1-3): ").strip()
        
        self.config['csv_import'] = {
            'file_path': csv_path,
            'format': format_choice,
            'delimiter': input("Разделитель (,): ").strip() or ",",
            'skip_header': input("Пропустить заголовок? (y/n): ").strip().lower() == 'y'
        }
    
    def setup_betting_config(self):
        """Настройка ставок"""
        print("\n💰 НАСТРОЙКИ СТАВОК")
        print("-" * 20)
        
        try:
            base_bet = int(input("Базовая ставка: ").strip() or "100")
            max_bet = int(input("Максимальная ставка: ").strip() or str(base_bet * 100))
            bankroll = int(input("Общий банкролл: ").strip() or str(base_bet * 1000))
            
            self.config['betting'] = {
                'base_bet': base_bet,
                'max_bet': max_bet,
                'bankroll': bankroll
            }
            
            print(f"✅ Настроено: базовая ставка {base_bet}, банкролл {bankroll}")
            
        except ValueError:
            print("❌ Ошибка: используются значения по умолчанию")
            self.config['betting'] = {
                'base_bet': 100,
                'max_bet': 10000,
                'bankroll': 100000
            }
    
    def setup_safety_limits(self):
        """Настройка лимитов безопасности"""
        print("\n🛡️ ЛИМИТЫ БЕЗОПАСНОСТИ")
        print("-" * 25)
        
        enable_limits = input("Включить лимиты безопасности? (y/n): ").strip().lower() == 'y'
        
        if enable_limits:
            try:
                daily_loss = int(input("Максимальная дневная потеря: ").strip() or "50000")
                session_time = int(input("Максимальное время сессии (минуты): ").strip() or "240")
                
                self.config['safety'] = {
                    'enabled': True,
                    'max_daily_loss': daily_loss,
                    'max_session_time': session_time * 60,
                    'force_break': True
                }
                
                print("✅ Лимиты безопасности включены")
                
            except ValueError:
                print("❌ Ошибка: лимиты отключены")
                self.config['safety'] = {'enabled': False}
        else:
            self.config['safety'] = {'enabled': False}
    
    def save_config(self):
        """Сохранение конфигурации"""
        try:
            with open(self.setup_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Конфигурация сохранена в {self.setup_path}")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def show_next_steps(self):
        """Показать следующие шаги"""
        print("\n🎯 СЛЕДУЮЩИЕ ШАГИ")
        print("-" * 20)
        print("1. Проверьте настройки в файле casino_setup.json")
        print("2. Запустите систему: python src/main.py")
        print("3. Выберите 'Управление данными' -> 'Получить реальные данные'")
        print("4. Протестируйте подключение")
        print("5. Начните с небольших ставок!")
        
        print("\n⚠️ ВАЖНЫЕ НАПОМИНАНИЯ:")
        print("- Никогда не ставьте больше, чем можете потерять")
        print("- Рулетка - игра с преимуществом казино")
        print("- Используйте систему только для анализа и обучения")
        print("- Соблюдайте правила и законы вашей юрисдикции")
        
        print(f"\n🎰 Настройка завершена для казино '{self.config.get('casino_name', 'Unknown')}'!")


def main():
    """Главная функция"""
    wizard = CasinoSetupWizard()
    wizard.run()


if __name__ == "__main__":
    main()