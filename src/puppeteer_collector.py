"""
🤖 Автоматизированный коллектор рулетки с Puppeteer
Интеграция бота-симулятора с браузерным коллектором
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from pyppeteer import launch
from pyppeteer.errors import TimeoutError as PuppeteerTimeoutError

# Импортируем наш симулятор
from bot_simulator import HumanBehaviorSimulator


class PuppeteerRouletteCollector:
    """Автоматизированный сборщик данных рулетки с симуляцией человека"""
    
    def __init__(self, config_path: str = None):
        """
        Инициализация коллектора
        
        Args:
            config_path: Путь к конфигурационному файлу .env
        """
        self.simulator = HumanBehaviorSimulator()
        self.browser = None
        self.page = None
        self.is_running = False
        self.collected_data = []
        
        # Загрузка конфигурации
        self.load_config(config_path)
        
        print("✅ Puppeteer коллектор инициализирован")
    
    def load_config(self, config_path: str = None):
        """Загрузка конфигурации из .env"""
        from dotenv import load_dotenv
        
        if config_path:
            load_dotenv(config_path)
        else:
            load_dotenv()
        
        self.config = {
            'headless': os.getenv('BOT_HEADLESS', 'True').lower() == 'true',
            'viewport_width': int(os.getenv('BOT_VIEWPORT_WIDTH', '1920')),
            'viewport_height': int(os.getenv('BOT_VIEWPORT_HEIGHT', '1080')),
            'user_agent': os.getenv('BOT_USER_AGENT', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
            'xpath': os.getenv('ROULETTE_XPATH', 
                '/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[7]/div/div[3]/div'),
            'collection_interval': int(os.getenv('COLLECTOR_INTERVAL', '30')),
            'max_results': int(os.getenv('COLLECTOR_MAX_RESULTS', '200'))
        }
    
    async def init_browser(self):
        """Инициализация браузера с anti-detection настройками"""
        print("🌐 Запуск браузера...")
        
        # Аргументы запуска Chrome
        args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            f'--window-size={self.config["viewport_width"]},{self.config["viewport_height"]}',
        ]
        
        # Запуск браузера
        self.browser = await launch({
            'headless': self.config['headless'],
            'args': args,
            'ignoreHTTPSErrors': True,
            'slowMo': 10,  # Небольшая задержка для естественности
        })
        
        # Создание страницы
        self.page = await self.browser.newPage()
        
        # Настройка viewport
        await self.page.setViewport({
            'width': self.config['viewport_width'],
            'height': self.config['viewport_height']
        })
        
        # Установка User-Agent
        await self.page.setUserAgent(self.config['user_agent'])
        
        # Маскировка webdriver
        await self.page.evaluateOnNewDocument('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Дополнительные маскировки
            window.navigator.chrome = {
                runtime: {},
            };
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en', 'ru'],
            });
        ''')
        
        print("✅ Браузер готов к работе")
    
    async def navigate_to_casino(self, url: str):
        """
        Переход на сайт казино с симуляцией человека
        
        Args:
            url: URL сайта казино
        """
        print(f"🎰 Переход на {url}...")
        
        try:
            # Переход на страницу
            await self.page.goto(url, {
                'waitUntil': 'networkidle2',
                'timeout': 30000
            })
            
            # Имитация задержки на чтение
            await self.simulator.wait_human(3.0)
            
            # Случайная прокрутка для естественности
            await self.simulator.scroll_human(self.page, 300, direction='down')
            await self.simulator.wait_human()
            
            print("✅ Страница загружена")
            
        except PuppeteerTimeoutError:
            print("❌ Таймаут при загрузке страницы")
            raise
    
    async def inject_collector_script(self):
        """Внедрение JavaScript коллектора в страницу"""
        print("💉 Внедрение скрипта коллектора...")
        
        # Читаем файл коллектора
        collector_path = Path(__file__).parent.parent / 'paddypower_collector_v2.js'
        
        if not collector_path.exists():
            print(f"❌ Файл коллектора не найден: {collector_path}")
            return False
        
        with open(collector_path, 'r', encoding='utf-8') as f:
            collector_script = f.read()
        
        # Внедряем скрипт
        try:
            await self.page.evaluate(collector_script)
            print("✅ Коллектор внедрён успешно")
            
            # Ждём инициализации
            await asyncio.sleep(5)
            
            return True
        except Exception as e:
            print(f"❌ Ошибка внедрения скрипта: {e}")
            return False
    
    async def check_collector_status(self) -> Dict:
        """Проверка статуса коллектора"""
        try:
            stats = await self.page.evaluate('showPaddypowerStats()')
            return stats
        except Exception as e:
            print(f"⚠️ Не удалось получить статистику: {e}")
            return {'total': 0}
    
    async def export_collected_data(self) -> List[Dict]:
        """Экспорт собранных данных из браузера"""
        print("📥 Экспорт данных из браузера...")
        
        try:
            # Вызываем функцию экспорта
            data = await self.page.evaluate('exportPaddypowerData()')
            
            if data and 'data' in data:
                self.collected_data = data['data']
                print(f"✅ Экспортировано {len(self.collected_data)} спинов")
                return self.collected_data
            else:
                print("⚠️ Нет данных для экспорта")
                return []
                
        except Exception as e:
            print(f"❌ Ошибка экспорта данных: {e}")
            return []
    
    async def save_to_file(self, filename: str = 'roulette_console_data.json'):
        """
        Сохранение собранных данных в файл
        
        Args:
            filename: Имя файла для сохранения
        """
        if not self.collected_data:
            print("⚠️ Нет данных для сохранения")
            return
        
        # Формируем полный объект для сохранения
        export_data = {
            'casino': 'Paddypower.com',
            'game': 'Spin and Go Roulette',
            'collected': datetime.now().isoformat(),
            'total_spins': len(self.collected_data),
            'collector_type': 'puppeteer_automated',
            'data': self.collected_data
        }
        
        # Сохраняем
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Данные сохранены в {filepath.absolute()}")
    
    async def run_collection_session(self, url: str, duration_minutes: int = 30):
        """
        Запуск сессии сбора данных
        
        Args:
            url: URL казино
            duration_minutes: Длительность сессии в минутах
        """
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🚀 ЗАПУСК СЕССИИ СБОРА ДАННЫХ")
        print(f"🎰 URL: {url}")
        print(f"⏱️ Длительность: {duration_minutes} минут")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            # Инициализация браузера
            await self.init_browser()
            
            # Переход на сайт
            await self.navigate_to_casino(url)
            
            # Внедрение коллектора
            if not await self.inject_collector_script():
                print("❌ Не удалось внедрить коллектор")
                return
            
            # Запуск цикла сбора
            self.is_running = True
            start_time = asyncio.get_event_loop().time()
            duration_seconds = duration_minutes * 60
            check_interval = self.config['collection_interval']
            
            iteration = 0
            
            while self.is_running:
                elapsed = asyncio.get_event_loop().time() - start_time
                
                # Проверка времени
                if elapsed >= duration_seconds:
                    print(f"⏰ Время сессии истекло ({duration_minutes} мин)")
                    break
                
                iteration += 1
                remaining = duration_seconds - elapsed
                
                print(f"\n🔄 Итерация {iteration} | Осталось: {remaining/60:.1f} мин")
                
                # Проверка статуса коллектора
                stats = await self.check_collector_status()
                if stats:
                    print(f"📊 Собрано спинов: {stats.get('total', 0)}")
                
                # Случайные действия для естественности
                if iteration % 3 == 0:
                    # Небольшая прокрутка
                    scroll_distance = await self.page.evaluate('Math.random() * 200 + 100')
                    await self.simulator.scroll_human(self.page, scroll_distance, 
                                                     direction='down' if iteration % 2 == 0 else 'up')
                
                # Ждём до следующей проверки
                await asyncio.sleep(check_interval)
            
            print("\n✅ Сессия сбора завершена")
            
            # Экспорт данных
            await self.export_collected_data()
            
            # Сохранение в файл
            await self.save_to_file()
            
            # Экспорт статистики активности бота
            self.simulator.export_activity_log('bot_session_log.json')
            
        except Exception as e:
            print(f"❌ Ошибка во время сессии: {e}")
            raise
        
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Очистка ресурсов"""
        print("\n🧹 Очистка ресурсов...")
        
        if self.browser:
            await self.browser.close()
            print("✅ Браузер закрыт")
        
        self.is_running = False
    
    def stop(self):
        """Остановка сбора данных"""
        print("\n⏹️ Остановка коллектора...")
        self.is_running = False


# ============================================
# ФУНКЦИЯ ДЛЯ ЗАПУСКА ИЗ КОМАНДНОЙ СТРОКИ
# ============================================

async def main():
    """Главная функция для запуска коллектора"""
    import argparse
    
    parser = argparse.ArgumentParser(description='🤖 Puppeteer Roulette Collector')
    parser.add_argument('--url', type=str, 
                       default='https://casinopp-com-ngm.bfcdl.com/livedistributed/25.9.3.0/?game=sgrol',
                       help='URL казино')
    parser.add_argument('--duration', type=int, default=30,
                       help='Длительность сессии в минутах')
    parser.add_argument('--headless', action='store_true',
                       help='Запуск в headless режиме')
    parser.add_argument('--output', type=str, default='roulette_console_data.json',
                       help='Имя выходного файла')
    
    args = parser.parse_args()
    
    # Создание коллектора
    collector = PuppeteerRouletteCollector()
    
    # Переопределение headless из аргументов
    if args.headless:
        collector.config['headless'] = True
    
    try:
        # Запуск сессии
        await collector.run_collection_session(
            url=args.url,
            duration_minutes=args.duration
        )
        
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🎉 СБОР ДАННЫХ ЗАВЕРШЁН УСПЕШНО!")
        print(f"📁 Данные сохранены в: {args.output}")
        print(f"📊 Всего собрано спинов: {len(collector.collected_data)}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")
        collector.stop()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 PUPPETEER ROULETTE COLLECTOR")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Запуск
    asyncio.run(main())
