"""
ВЕБ-СКРАПЕР ДЛЯ ОДНОЙ КОНКРЕТНОЙ РУЛЕТКИ
========================================

Этот скрапер извлекает данные ТОЛЬКО с одной конкретной рулетки используя XPath
"""

import time
from datetime import datetime
from typing import List, Dict
import re
import sqlite3
from pathlib import Path


class SingleRouletteWebScraper:
    """Веб-скрапер для одной конкретной рулетки"""
    
    def __init__(self, target_xpath: str = "/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[4]"):
        """
        Инициализация скрапера
        
        Args:
            target_xpath: XPath элемента с результатами конкретной рулетки
        """
        self.target_xpath = target_xpath
        self.driver = None
        self.db_path = Path(__file__).parent / "data" / "scraped_single_roulette.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
        
        print("🎯" + "="*60)
        print("   ВЕБ-СКРАПЕР ДЛЯ ОДНОЙ КОНКРЕТНОЙ РУЛЕТКИ")
        print(f"   XPath цели: {target_xpath[:50]}...")
        print("🎯" + "="*60)
    
    def _init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number INTEGER NOT NULL,
                    color TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    source TEXT,
                    xpath TEXT
                )
            """)
            conn.commit()
    
    def setup_selenium(self, url: str = None):
        """
        Настройка Selenium WebDriver
        
        Args:
            url: URL страницы для скрапинга
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            print("🔧 Настройка Selenium WebDriver...")
            
            # Настройки Chrome
            chrome_options = Options()
            # chrome_options.add_argument('--headless')  # Раскомментируйте для фонового режима
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Создаем драйвер
            self.driver = webdriver.Chrome(options=chrome_options)
            
            if url:
                print(f"🌐 Открываем страницу: {url}")
                self.driver.get(url)
                time.sleep(5)  # Ждем загрузку
            
            print("✅ Selenium настроен успешно")
            return True
            
        except ImportError:
            print("❌ Selenium не установлен!")
            print("   Установите: pip install selenium")
            print("   Также нужен ChromeDriver: https://chromedriver.chromium.org/")
            return False
        except Exception as e:
            print(f"❌ Ошибка настройки Selenium: {e}")
            return False
    
    def extract_numbers_from_xpath(self) -> List[Dict]:
        """
        Извлекает числа из элемента по XPath
        
        Returns:
            Список результатов рулетки
        """
        if not self.driver:
            print("❌ WebDriver не инициализирован")
            return []
        
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            print(f"🔍 Ищем элемент по XPath: {self.target_xpath}")
            
            # Ждем появления элемента
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, self.target_xpath))
            )
            
            print("✅ Элемент найден!")
            
            # Получаем текст элемента
            element_text = element.text
            element_html = element.get_attribute('innerHTML')
            
            print(f"📊 Текст элемента: {element_text[:200]}")
            
            # Ищем все дочерние элементы
            children = element.find_elements(By.XPATH, ".//*")
            print(f"📊 Найдено дочерних элементов: {len(children)}")
            
            results = []
            
            # Вариант 1: Парсим текст
            numbers = self._extract_numbers_from_text(element_text)
            if numbers:
                results.extend(numbers)
            
            # Вариант 2: Парсим HTML
            numbers_from_html = self._extract_numbers_from_html(element_html)
            if numbers_from_html:
                results.extend(numbers_from_html)
            
            # Вариант 3: Парсим дочерние элементы
            for child in children:
                child_text = child.text
                child_class = child.get_attribute('class')
                
                if child_text and child_text.strip():
                    child_numbers = self._extract_numbers_from_text(child_text)
                    if child_numbers:
                        results.extend(child_numbers)
            
            # Удаляем дубликаты
            unique_results = []
            seen = set()
            for r in results:
                key = (r['number'], r['timestamp'].strftime('%Y-%m-%d %H:%M:%S'))
                if key not in seen:
                    seen.add(key)
                    unique_results.append(r)
            
            print(f"✅ Извлечено {len(unique_results)} уникальных результатов")
            return unique_results
            
        except Exception as e:
            print(f"❌ Ошибка извлечения данных: {e}")
            return []
    
    def _extract_numbers_from_text(self, text: str) -> List[Dict]:
        """Извлекает числа рулетки из текста"""
        results = []
        
        # Паттерны для поиска чисел рулетки (0-36)
        patterns = [
            r'\b([0-9]|[1-2][0-9]|3[0-6])\b',  # Числа 0-36
            r'#([0-9]|[1-2][0-9]|3[0-6])\b',    # С решеткой
            r'№([0-9]|[1-2][0-9]|3[0-6])\b',    # С номером
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    number = int(match)
                    if 0 <= number <= 36:
                        color = self._get_color(number)
                        results.append({
                            'number': number,
                            'color': color,
                            'timestamp': datetime.now(),
                            'source': 'web_scraper',
                            'xpath': self.target_xpath
                        })
                except ValueError:
                    continue
        
        return results
    
    def _extract_numbers_from_html(self, html: str) -> List[Dict]:
        """Извлекает числа рулетки из HTML"""
        results = []
        
        # Ищем числа в классах, атрибутах и тексте
        patterns = [
            r'number["\s:]*([0-9]|[1-2][0-9]|3[0-6])',
            r'result["\s:]*([0-9]|[1-2][0-9]|3[0-6])',
            r'winning["\s:]*([0-9]|[1-2][0-9]|3[0-6])',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    number = int(match)
                    if 0 <= number <= 36:
                        color = self._get_color(number)
                        results.append({
                            'number': number,
                            'color': color,
                            'timestamp': datetime.now(),
                            'source': 'web_scraper_html',
                            'xpath': self.target_xpath
                        })
                except ValueError:
                    continue
        
        return results
    
    def _get_color(self, number: int) -> str:
        """Определяет цвет числа"""
        if number == 0:
            return 'green'
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return 'red' if number in red_numbers else 'black'
    
    def save_results(self, results: List[Dict]) -> int:
        """Сохраняет результаты в базу данных"""
        if not results:
            return 0
        
        saved_count = 0
        
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            for result in results:
                try:
                    cursor.execute("""
                        INSERT INTO scraped_results 
                        (number, color, timestamp, source, xpath)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        result['number'],
                        result['color'],
                        result['timestamp'],
                        result['source'],
                        result['xpath']
                    ))
                    saved_count += 1
                except Exception as e:
                    print(f"⚠️ Ошибка сохранения: {e}")
            
            conn.commit()
        
        print(f"💾 Сохранено {saved_count} результатов")
        return saved_count
    
    def monitor_roulette(self, url: str, duration_minutes: int = 30, check_interval: int = 30):
        """
        Мониторинг рулетки в реальном времени
        
        Args:
            url: URL страницы с рулеткой
            duration_minutes: Продолжительность мониторинга
            check_interval: Интервал проверки в секундах
        """
        print(f"🎰 ЗАПУСК МОНИТОРИНГА РУЛЕТКИ")
        print(f"⏱️  Продолжительность: {duration_minutes} минут")
        print(f"🔄 Интервал проверки: {check_interval} секунд")
        print("="*60)
        
        if not self.setup_selenium(url):
            print("❌ Не удалось настроить Selenium")
            return
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        last_results = set()
        total_new_results = 0
        
        try:
            while time.time() < end_time:
                print(f"\n🔍 Проверка результатов... ({datetime.now().strftime('%H:%M:%S')})")
                
                # Извлекаем результаты
                results = self.extract_numbers_from_xpath()
                
                # Фильтруем новые результаты
                new_results = []
                for result in results:
                    result_key = (result['number'], result['timestamp'].strftime('%Y-%m-%d %H:%M'))
                    if result_key not in last_results:
                        new_results.append(result)
                        last_results.add(result_key)
                
                if new_results:
                    print(f"🎯 Найдено {len(new_results)} новых результатов:")
                    for r in new_results:
                        print(f"   {r['number']} ({r['color']})")
                    
                    # Сохраняем
                    saved = self.save_results(new_results)
                    total_new_results += saved
                else:
                    print("   Новых результатов нет")
                
                # Показываем статистику
                print(f"📊 Всего собрано результатов: {total_new_results}")
                
                # Ждем перед следующей проверкой
                print(f"⏳ Ожидание {check_interval} секунд...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  Мониторинг остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка мониторинга: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                print("✅ WebDriver закрыт")
        
        print(f"\n🎉 МОНИТОРИНГ ЗАВЕРШЕН!")
        print(f"📊 Всего собрано {total_new_results} новых результатов")
    
    def get_statistics(self) -> Dict:
        """Получает статистику собранных данных"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT number, color, timestamp FROM scraped_results ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            if not rows:
                return {'total': 0}
            
            colors = {'red': 0, 'black': 0, 'green': 0}
            numbers_count = {}
            
            for number, color, timestamp in rows:
                colors[color] += 1
                numbers_count[number] = numbers_count.get(number, 0) + 1
            
            total = len(rows)
            
            return {
                'total': total,
                'colors': colors,
                'percentages': {
                    'red': round(colors['red']/total*100, 1),
                    'black': round(colors['black']/total*100, 1),
                    'green': round(colors['green']/total*100, 1)
                },
                'most_frequent': sorted(numbers_count.items(), key=lambda x: x[1], reverse=True)[:5],
                'latest_results': [(number, color) for number, color, _ in rows[:10]]
            }
    
    def show_statistics(self):
        """Показывает статистику"""
        stats = self.get_statistics()
        
        if stats['total'] == 0:
            print("❌ Нет данных для статистики")
            return
        
        print(f"\n📊 СТАТИСТИКА СОБРАННЫХ ДАННЫХ:")
        print("="*50)
        print(f"Всего результатов: {stats['total']}")
        print(f"Красные: {stats['colors']['red']} ({stats['percentages']['red']}%)")
        print(f"Черные: {stats['colors']['black']} ({stats['percentages']['black']}%)")
        print(f"Зеленые: {stats['colors']['green']} ({stats['percentages']['green']}%)")
        
        print(f"\nЧастые числа:")
        for number, count in stats['most_frequent']:
            print(f"  {number}: {count} раз ({count/stats['total']*100:.1f}%)")
        
        print(f"\nПоследние результаты:")
        for i, (number, color) in enumerate(stats['latest_results'], 1):
            print(f"  {i:2d}. {number:2d} ({color})")


def main():
    """Главная функция"""
    print("🎰 ВЕБ-СКРАПЕР ДЛЯ ОДНОЙ КОНКРЕТНОЙ РУЛЕТКИ")
    print("="*60)
    
    # Создаем скрапер с вашим XPath
    scraper = SingleRouletteWebScraper(
        target_xpath="/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[4]"
    )
    
    print("\n📋 МЕНЮ:")
    print("1. 🧪 Тест извлечения данных (нужен URL)")
    print("2. 🎰 Запустить мониторинг (нужен URL)")
    print("3. 📊 Показать статистику")
    print("4. ℹ️  Инструкция по использованию")
    print("0. 🚪 Выход")
    
    while True:
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            url = input("Введите URL страницы с рулеткой: ").strip()
            if url:
                if scraper.setup_selenium(url):
                    results = scraper.extract_numbers_from_xpath()
                    if results:
                        print(f"✅ Найдено {len(results)} результатов:")
                        for i, r in enumerate(results[:10], 1):
                            print(f"  {i}. {r['number']} ({r['color']})")
                        
                        save = input("Сохранить результаты? (y/n): ").strip().lower()
                        if save == 'y':
                            scraper.save_results(results)
                    else:
                        print("❌ Результаты не найдены")
                    
                    scraper.driver.quit()
        
        elif choice == '2':
            url = input("Введите URL страницы с рулеткой: ").strip()
            if url:
                duration = input("Продолжительность мониторинга в минутах (по умолчанию 30): ").strip()
                duration = int(duration) if duration.isdigit() else 30
                
                interval = input("Интервал проверки в секундах (по умолчанию 30): ").strip()
                interval = int(interval) if interval.isdigit() else 30
                
                scraper.monitor_roulette(url, duration, interval)
        
        elif choice == '3':
            scraper.show_statistics()
        
        elif choice == '4':
            print("\n📖 ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:")
            print("="*60)
            print("1. Откройте страницу с рулеткой в браузере")
            print("2. Нажмите F12 (открыть Developer Tools)")
            print("3. Найдите элемент с результатами рулетки")
            print("4. Правый клик → Copy → Copy XPath")
            print("5. Измените target_xpath в коде на ваш XPath")
            print("6. Запустите скрапер с URL страницы")
            print("\n⚠️ ТРЕБОВАНИЯ:")
            print("- pip install selenium")
            print("- ChromeDriver: https://chromedriver.chromium.org/")
            print("="*60)
        
        elif choice == '0':
            print("👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()