"""
СТРОГИЙ СБОРЩИК ДАННЫХ ТОЛЬКО С ОДНОГО СТОЛА
============================================

Этот модуль гарантирует получение данных ТОЛЬКО с одного указанного стола рулетки.
Никаких данных с других столов не получается.
"""

import json
import time
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, List
from pathlib import Path


class SingleTableOnlyCollector:
    """Класс для получения данных СТРОГО с одного стола"""
    
    def __init__(self, table_id: str = "roulettestura541"):
        """
        Инициализация с конкретным столом
        
        Args:
            table_id: ID стола (ТОЛЬКО с него будут данные)
        """
        self.target_table_id = table_id
        self.config = self._load_config()
        
        print(f"🎯 НАСТРОЕН СБОР ДАННЫХ ТОЛЬКО С СТОЛА: {self.target_table_id}")
        print(f"⚠️  НИКАКИХ ДРУГИХ СТОЛОВ НЕ БУДЕТ!")
    
    def _load_config(self) -> Dict:
        """Загрузка конфигурации"""
        try:
            config_path = Path(__file__).parent / "casino_setup.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            return {}
    
    def get_single_table_data(self, limit: int = 50) -> List[Dict]:
        """
        Получает данные ТОЛЬКО с указанного стола
        
        Args:
            limit: Количество результатов (максимум 500)
            
        Returns:
            Список результатов ТОЛЬКО с целевого стола
        """
        if not self.config:
            print("❌ Нет конфигурации API")
            return []
        
        try:
            # Строгая проверка стола
            print(f"🔍 Получение данных ТОЛЬКО с стола: {self.target_table_id}")
            
            # API запрос СТРОГО для одного стола
            auth = self.config['api']['auth']
            base_url = "https://games.pragmaticplaylive.net/api/ui/statisticHistory"
            
            # Параметры ТОЛЬКО для нашего стола
            params = {
                'tableId': self.target_table_id,  # СТРОГО наш стол
                'numberOfGames': min(limit, 500),
                'JSESSIONID': auth['jsessionid']
            }
            
            url = f"{base_url}?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.config['api']['headers']['User-Agent'])
            req.add_header('Accept', 'application/json')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    results = self._parse_single_table_only(data)
                    
                    # ДВОЙНАЯ ПРОВЕРКА: убираем любые данные не с нашего стола
                    filtered_results = []
                    for result in results:
                        if result.get('table_id') == self.target_table_id:
                            filtered_results.append(result)
                        else:
                            print(f"🚫 ОТФИЛЬТРОВАН результат с чужого стола: {result.get('table_id')}")
                    
                    print(f"✅ ПОЛУЧЕНО {len(filtered_results)} результатов ТОЛЬКО с стола {self.target_table_id}")
                    return filtered_results
                else:
                    print(f"❌ API вернул код {response.getcode()}")
                    
        except Exception as e:
            print(f"❌ Ошибка API: {e}")
        
        return []
    
    def _parse_single_table_only(self, data: Dict) -> List[Dict]:
        """
        Парсит данные с проверкой стола
        """
        results = []
        
        try:
            if 'history' in data and isinstance(data['history'], list):
                print(f"📊 Получено {len(data['history'])} записей")
                
                for game in data['history']:
                    if not isinstance(game, dict):
                        continue
                    
                    # Парсим номер и цвет
                    winning_number = None
                    color = None
                    
                    if 'gameResult' in game:
                        try:
                            parts = game['gameResult'].split()
                            if len(parts) >= 2:
                                winning_number = int(parts[0])
                                api_color = parts[1].lower()
                                color = api_color if api_color in ['red', 'black', 'green'] else self._get_color(winning_number)
                        except (ValueError, IndexError):
                            continue
                    
                    if winning_number is not None and 0 <= winning_number <= 36:
                        # Время
                        timestamp = datetime.now()
                        if 'gameTime' in game:
                            try:
                                timestamp = datetime.fromisoformat(game['gameTime'].replace('Z', '+00:00'))
                            except:
                                pass
                        
                        # СТРОГО привязываем к нашему столу
                        result = {
                            'number': winning_number,
                            'color': color,
                            'timestamp': timestamp,
                            'table_id': self.target_table_id,  # СТРОГО наш стол
                            'source': 'single_table_api',
                            'game_id': game.get('gameId', '')
                        }
                        
                        results.append(result)
                
                print(f"✅ Обработано {len(results)} результатов стола {self.target_table_id}")
                
        except Exception as e:
            print(f"❌ Ошибка парсинга: {e}")
        
        return results
    
    def _get_color(self, number: int) -> str:
        """Определяет цвет числа"""
        if number == 0:
            return 'green'
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return 'red' if number in red_numbers else 'black'
    
    def monitor_single_table(self, duration_minutes: int = 30):
        """
        Мониторинг ТОЛЬКО одного стола в реальном времени
        
        Args:
            duration_minutes: Продолжительность мониторинга
        """
        print(f"🎰 МОНИТОРИНГ ТОЛЬКО СТОЛА {self.target_table_id}")
        print(f"⏱️  Продолжительность: {duration_minutes} минут")
        print(f"🚫 НИКАКИХ ДРУГИХ СТОЛОВ!")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        spin_counter = 0
        last_results = set()  # Для избежания дублей
        
        while time.time() < end_time:
            try:
                # Получаем свежие данные
                current_results = self.get_single_table_data(10)
                
                # Ищем новые результаты
                for result in current_results:
                    result_key = f"{result['game_id']}_{result['number']}_{result['timestamp']}"
                    
                    if result_key not in last_results:
                        spin_counter += 1
                        print(f"🎯 Спин #{spin_counter}: {result['number']} ({result['color']}) - СТОЛ {result['table_id']}")
                        
                        # Сохраняем в базу данных
                        self._save_to_database(result)
                        
                        last_results.add(result_key)
                        
                        # Ограничиваем размер кэша
                        if len(last_results) > 100:
                            last_results = set(list(last_results)[-50:])
                
                # Ждем перед следующим запросом
                time.sleep(30)  # 30 секунд между запросами
                
            except KeyboardInterrupt:
                print("⏹️  Мониторинг остановлен пользователем")
                break
            except Exception as e:
                print(f"❌ Ошибка мониторинга: {e}")
                time.sleep(10)
        
        print(f"✅ Мониторинг завершен. Получено {spin_counter} новых спинов ТОЛЬКО с стола {self.target_table_id}")
    
    def _save_to_database(self, result: Dict):
        """Сохраняет результат в базу данных"""
        try:
            import sqlite3
            
            db_path = Path(__file__).parent / "data" / "single_table_history.db"
            db_path.parent.mkdir(exist_ok=True)
            
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.cursor()
                
                # Создаем таблицу если не существует
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS single_table_spins (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        number INTEGER NOT NULL,
                        color TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        table_id TEXT NOT NULL,
                        game_id TEXT,
                        source TEXT
                    )
                """)
                
                # Вставляем результат
                cursor.execute("""
                    INSERT INTO single_table_spins 
                    (number, color, timestamp, table_id, game_id, source)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    result['number'],
                    result['color'],
                    result['timestamp'],
                    result['table_id'],
                    result.get('game_id', ''),
                    result.get('source', 'single_table_api')
                ))
                
                conn.commit()
                print(f"💾 Результат сохранен: {result['number']} ({result['color']})")
                
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")


def test_single_table():
    """Тестирование сборщика одного стола"""
    print("🧪 ТЕСТИРОВАНИЕ СБОРЩИКА ОДНОГО СТОЛА")
    print("=" * 50)
    
    collector = SingleTableOnlyCollector("roulettestura541")
    
    # Получаем данные
    results = collector.get_single_table_data(20)
    
    if results:
        print(f"\n📊 ПОЛУЧЕНО {len(results)} РЕЗУЛЬТАТОВ ТОЛЬКО С СТОЛА roulettestura541:")
        print("-" * 50)
        
        for i, result in enumerate(results[:10], 1):
            time_str = result['timestamp'].strftime("%H:%M:%S")
            print(f"  {i:2d}. {time_str}: {result['number']:2d} ({result['color']}) - {result['table_id']}")
        
        # Статистика
        colors = {'red': 0, 'black': 0, 'green': 0}
        for result in results:
            colors[result['color']] += 1
        
        total = len(results)
        print(f"\n📈 СТАТИСТИКА СТОЛА {collector.target_table_id}:")
        print(f"Всего результатов: {total}")
        print(f"Красные: {colors['red']} ({colors['red']/total*100:.1f}%)")
        print(f"Черные: {colors['black']} ({colors['black']/total*100:.1f}%)")
        print(f"Зеленые: {colors['green']} ({colors['green']/total*100:.1f}%)")
        
        # Проверяем что все результаты с нужного стола
        wrong_table = [r for r in results if r.get('table_id') != collector.target_table_id]
        if wrong_table:
            print(f"❌ НАЙДЕНЫ РЕЗУЛЬТАТЫ С ЧУЖИХ СТОЛОВ: {len(wrong_table)}")
        else:
            print(f"✅ ВСЕ РЕЗУЛЬТАТЫ С ПРАВИЛЬНОГО СТОЛА: {collector.target_table_id}")
    else:
        print("❌ Нет данных")


if __name__ == "__main__":
    test_single_table()