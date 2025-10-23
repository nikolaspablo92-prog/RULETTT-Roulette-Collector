"""
Модуль для получения реальных данных рулетки из различных источников
"""

import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random
import urllib.request
import urllib.error
from pathlib import Path

class LiveDataCollector:
    """Класс для получения реальных данных рулетки"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.sources = {
            'roulette_tracker': 'https://roulettetracker.net',
            'casino_stats': 'https://casino-stats.com',
            'live_roulette': 'https://live-roulette-results.com'
        }
        self.config = self._load_casino_config()
    
    def _load_casino_config(self) -> Dict:
        """Загрузка конфигурации казино"""
        try:
            config_path = Path(__file__).parent.parent / "casino_setup.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Не удалось загрузить конфигурацию казино: {e}")
        
        # Конфигурация по умолчанию
        return {
            'connection_method': 'mock',
            'casino_name': 'Demo Casino',
            'api': {},
            'scraping': {},
            'betting': {'base_bet': 100}
        }
    
    def get_live_results(self, source: str = 'mock', limit: int = 100) -> List[Dict]:
        """
        Получить живые результаты рулетки только с указанного стола
        
        Args:
            source: Источник данных ('mock', 'api', 'scrape')
            limit: Максимальное количество результатов
            
        Returns:
            Список результатов спинов
        """
        if source == 'mock':
            return self._get_mock_live_data(limit)
        elif source == 'api':
            return self._get_api_data(limit)
        elif source == 'scrape':
            return self._scrape_live_data(limit)
        else:
            raise ValueError(f"Неподдерживаемый источник: {source}")
    
    def _get_mock_live_data(self, limit: int) -> List[Dict]:
        """
        Генерирует реалистичные данные, имитирующие живую рулетку
        с более реальными паттернами и временными интервалами
        """
        results = []
        base_time = datetime.now() - timedelta(minutes=limit * 2)
        
        # Реалистичные параметры рулетки
        numbers_weights = self._get_realistic_weights()
        
        for i in range(limit):
            # Реалистичные интервалы между спинами (1-5 минут)
            interval = random.choice([1, 1, 2, 2, 2, 3, 3, 4, 5])
            spin_time = base_time + timedelta(minutes=i * interval)
            
            # Выбираем число с учетом весов (некоторые числа выпадают чаще)
            number = random.choices(
                list(range(37)), 
                weights=numbers_weights,
                k=1
            )[0]
            
            color = self._get_color(number)
            
            # Используем конкретный стол из конфигурации
            target_table = self.config.get('table_info', {}).get('table_id', 'roulettestura541')
            
            result = {
                'number': number,
                'color': color,
                'timestamp': spin_time,
                'source': 'live_simulation',
                'table_id': target_table,  # Только указанный стол
                'dealer': f'dealer_{random.randint(1, 3)}'  # Меньше дилеров для одного стола
            }
            results.append(result)
        
        return results
    
    def _get_realistic_weights(self) -> List[float]:
        """
        Возвращает реалистичные веса для чисел рулетки
        Некоторые числа могут выпадать чаще из-за физических особенностей колеса
        """
        base_weight = 1.0
        weights = [base_weight] * 37
        
        # Некоторые числа делаем чуть более/менее вероятными
        hot_numbers = [7, 17, 23, 29]  # "горячие" числа
        cold_numbers = [1, 13, 31, 35]  # "холодные" числа
        
        for num in hot_numbers:
            weights[num] = base_weight * 1.1
        
        for num in cold_numbers:
            weights[num] = base_weight * 0.9
        
        return weights
    
    def _get_api_data(self, limit: int) -> List[Dict]:
        """
        Получает данные через API только с указанного стола
        """
        # Проверяем наличие API конфигурации
        if self.config.get('connection_method') != 'api':
            print("⚠️  API не настроен, используем симуляцию...")
            return self._get_mock_live_data(limit)
        
        # Получаем данные с одного стола
        return self._get_single_table_api_data(limit)
    
    def _get_single_table_api_data(self, limit: int) -> List[Dict]:
        """
        Получает данные СТРОГО с одного конкретного стола через API
        """
        # Используем строгий сборщик одного стола
        try:
            # Импортируем строгий сборщик
            import sys
            from pathlib import Path
            
            # Добавляем путь к строгому сборщику
            strict_path = Path(__file__).parent.parent / "strict_single_table.py"
            if strict_path.exists():
                sys.path.insert(0, str(strict_path.parent))
                from strict_single_table import SingleTableOnlyCollector
                
                # Создаем строгий сборщик для нашего стола
                target_table = "roulettestura541"  # ТОЛЬКО этот стол
                strict_collector = SingleTableOnlyCollector(target_table)
                
                print(f"🎯 СТРОГИЙ СБОР ДАННЫХ ТОЛЬКО С СТОЛА: {target_table}")
                results = strict_collector.get_single_table_data(limit)
                
                if results:
                    print(f"✅ ПОЛУЧЕНО {len(results)} результатов ТОЛЬКО с стола {target_table}")
                    # Дополнительная проверка на всякий случай
                    filtered = [r for r in results if r.get('table_id') == target_table]
                    if len(filtered) != len(results):
                        print(f"🚫 ОТФИЛЬТРОВАНО {len(results) - len(filtered)} чужих результатов")
                    return filtered
                else:
                    print(f"❌ Нет данных с стола {target_table}")
                    
        except Exception as e:
            print(f"❌ Ошибка строгого сборщика: {e}")
        
        # Фоллбэк - используем старый метод с дополнительной фильтрацией
        return self._fallback_single_table_data(limit)
    
    def _fallback_single_table_data(self, limit: int) -> List[Dict]:
        """Фоллбэк метод с дополнительной фильтрацией"""
        try:
            target_table = "roulettestura541"  # ТОЛЬКО этот стол
            print(f"🎯 Фоллбэк: получение данных стола {target_table}...")
            
            # Используем API статистики для конкретного стола
            auth = self.config['api']['auth']
            base_url = "https://games.pragmaticplaylive.net/api/ui/statisticHistory"
            
            import urllib.parse
            params = {
                'tableId': target_table,  # СТРОГО наш стол
                'numberOfGames': min(limit, 500)
            }
            
            url = f"{base_url}?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.config['api']['headers']['User-Agent'])
            req.add_header('Accept', 'application/json, text/plain, */*')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    results = self._parse_api_history(data, target_table)
                    
                    # СТРОГАЯ ФИЛЬТРАЦИЯ: убираем все что не с нашего стола
                    filtered_results = []
                    for result in results:
                        if result.get('table_id') == target_table:
                            filtered_results.append(result)
                        else:
                            print(f"🚫 ОТФИЛЬТРОВАН: {result.get('table_id')} (нужен {target_table})")
                    
                    print(f"✅ После фильтрации: {len(filtered_results)} результатов с стола {target_table}")
                    return filtered_results
                else:
                    print(f"❌ API вернул код {response.getcode()}")
                    
        except Exception as e:
            print(f"❌ Ошибка фоллбэк API: {e}")
        
        return self._get_mock_live_data(limit)
    
    def _parse_api_history(self, data: Dict, table_id: str) -> List[Dict]:
        """
        Парсит историю игр из API ответа
        """
        results = []
        
        try:
            if 'history' in data and isinstance(data['history'], list):
                print(f"📊 Получено {len(data['history'])} записей с стола {table_id}")
                
                for game in data['history']:
                    if isinstance(game, dict):
                        # Парсим gameResult (формат: "25 Red", "0 Green", "12 Black")
                        winning_number = None
                        api_color = None
                        
                        if 'gameResult' in game:
                            try:
                                parts = game['gameResult'].split()
                                if len(parts) >= 2:
                                    winning_number = int(parts[0])
                                    api_color = parts[1].lower()
                            except (ValueError, IndexError):
                                continue
                        
                        if winning_number is not None and 0 <= winning_number <= 36:
                            # Используем цвет из API или рассчитываем
                            color = api_color if api_color in ['red', 'black', 'green'] else self._get_color(winning_number)
                            
                            # Время игры
                            timestamp = datetime.now()
                            if 'gameTime' in game:
                                try:
                                    timestamp = datetime.fromisoformat(game['gameTime'].replace('Z', '+00:00'))
                                except:
                                    pass
                            
                            result = {
                                'number': winning_number,
                                'color': color,
                                'timestamp': timestamp,
                                'source': 'pragmatic_api',
                                'table_id': table_id,
                                'game_id': game.get('gameId', ''),
                                'dealer': f'dealer_{table_id}'
                            }
                            
                            results.append(result)
                
                # Сортируем по времени (новые сначала)
                results.sort(key=lambda x: x['timestamp'], reverse=True)
                print(f"✅ Обработано {len(results)} результатов стола {table_id}")
                
        except Exception as e:
            print(f"❌ Ошибка парсинга: {e}")
        
        return results
    
    def _scrape_live_data(self, limit: int) -> List[Dict]:
        """
        Парсит данные с публичных сайтов статистики рулетки
        """
        try:
            print("🔍 Попытка получить данные с публичных источников...")
            
            # Пример парсинга (нужно адаптировать под конкретные сайты)
            results = []
            
            # Здесь был бы реальный код для парсинга
            # Но многие сайты защищены от парсинга
            print("⚠️  Многие сайты казино защищены от автоматического сбора данных")
            print("   Используем симуляцию реальных данных...")
            
            return self._get_mock_live_data(limit)
            
        except Exception as e:
            print(f"❌ Ошибка при получении данных: {e}")
            print("   Переключаемся на симуляцию...")
            return self._get_mock_live_data(limit)
    
    def _get_color(self, number: int) -> str:
        """Определяет цвет числа на рулетке"""
        if number == 0:
            return 'green'
        
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return 'red' if number in red_numbers else 'black'
    
    def get_live_stream(self, duration_minutes: int = 60) -> List[Dict]:
        """
        Симулирует получение данных в реальном времени
        
        Args:
            duration_minutes: Продолжительность получения данных в минутах
            
        Returns:
            Список результатов спинов в хронологическом порядке
        """
        print(f"🎰 Начинаем получение живых данных на {duration_minutes} минут...")
        
        results = []
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        spin_counter = 0
        
        while time.time() < end_time:
            # Реалистичный интервал между спинами (1-3 минуты)
            sleep_time = random.uniform(60, 180)
            
            print(f"⏳ Ждем следующий спин... ({sleep_time:.0f} сек)")
            time.sleep(min(sleep_time, 10))  # Для демо ускоряем
            
            # Получаем новый результат
            new_results = self._get_mock_live_data(1)
            if new_results:
                spin_counter += 1
                result = new_results[0]
                result['spin_id'] = spin_counter
                results.append(result)
                
                print(f"🎯 Спин #{spin_counter}: {result['number']} ({result['color']})")
                
                # Можно добавлять результат сразу в базу данных
                self._save_live_result(result)
        
        print(f"✅ Получено {len(results)} результатов за {duration_minutes} минут")
        return results
    
    def _save_live_result(self, result: Dict):
        """Сохраняет результат в базу данных"""
        try:
            from data_collector import DataCollector
            
            db = DataCollector()
            db.add_spin(
                number=result['number'],
                timestamp=result['timestamp']
            )
            print(f"💾 Результат сохранен: {result['number']} ({result['color']})")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def get_historical_data(self, days: int = 30) -> List[Dict]:
        """
        Получает исторические данные за указанный период
        
        Args:
            days: Количество дней для получения данных
            
        Returns:
            Список исторических результатов
        """
        print(f"📊 Получаем исторические данные за {days} дней...")
        
        # Генерируем исторические данные с реалистичными интервалами
        total_spins = days * 12 * 24  # примерно 12 спинов в час, 24 часа
        historical_data = []
        
        base_time = datetime.now() - timedelta(days=days)
        
        for i in range(total_spins):
            # Реалистичные интервалы (5-10 минут)
            minutes_offset = i * random.uniform(5, 10)
            spin_time = base_time + timedelta(minutes=minutes_offset)
            
            number = random.choices(
                list(range(37)), 
                weights=self._get_realistic_weights(),
                k=1
            )[0]
            
            color = self._get_color(number)
            
            result = {
                'number': number,
                'color': color,
                'timestamp': spin_time,
                'source': 'historical_simulation',
                'spin_id': i + 1
            }
            historical_data.append(result)
        
        print(f"✅ Получено {len(historical_data)} исторических записей")
        return historical_data
    
    def test_connection(self) -> Dict[str, bool]:
        """Тестирует доступность различных источников данных"""
        print("🔌 Тестируем подключение к источникам данных...")
        
        results = {
            'mock': True,  # Всегда доступно
            'api': False,  # Требует настройки
            'scrape': False  # Зависит от доступности сайтов
        }
        
        # Тест API
        try:
            # Здесь был бы тест реального API
            print("🔑 API: Требуется настройка ключей доступа")
        except:
            pass
        
        # Тест веб-скрапинга
        try:
            req = urllib.request.Request('https://httpbin.org/get', headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    results['scrape'] = True
                    print("🌐 Веб-скрапинг: Соединение доступно")
        except:
            print("🌐 Веб-скрапинг: Соединение недоступно")
        
        print("✅ Симуляция реальных данных: Всегда доступна")
        
        return results

def main():
    """Демонстрация возможностей модуля"""
    collector = LiveDataCollector()
    
    print("=== ТЕСТ МОДУЛЯ ПОЛУЧЕНИЯ ЖИВЫХ ДАННЫХ ===\n")
    
    # Тест подключения
    print("1. Тестирование подключений:")
    connections = collector.test_connection()
    print(f"Доступные источники: {list(connections.keys())}\n")
    
    # Получение последних результатов
    print("2. Получение последних результатов:")
    recent_results = collector.get_live_results('mock', limit=10)
    for result in recent_results[-5:]:
        print(f"   {result['timestamp'].strftime('%H:%M:%S')}: "
              f"{result['number']} ({result['color']})")
    print()
    
    # Исторические данные
    print("3. Получение исторических данных:")
    historical = collector.get_historical_data(days=1)
    print(f"   Получено {len(historical)} записей за 1 день")
    
    # Статистика
    colors = {}
    for result in historical:
        color = result['color']
        colors[color] = colors.get(color, 0) + 1
    
    total = len(historical)
    print(f"   Красных: {colors.get('red', 0)} ({colors.get('red', 0)/total*100:.1f}%)")
    print(f"   Черных: {colors.get('black', 0)} ({colors.get('black', 0)/total*100:.1f}%)")
    print(f"   Зеленых: {colors.get('green', 0)} ({colors.get('green', 0)/total*100:.1f}%)")

if __name__ == "__main__":
    main()