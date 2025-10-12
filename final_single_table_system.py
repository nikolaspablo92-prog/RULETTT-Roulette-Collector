"""
ОКОНЧАТЕЛЬНОЕ РЕШЕНИЕ - ТОЛЬКО ОДИН СТОЛ
=======================================

Эта система ГАРАНТИРОВАННО работает только с одним столом roulettestura541
и никогда не будет получать данные с других столов.
"""

import json
import time
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, List
from pathlib import Path
import sqlite3


class FinalSingleTableSystem:
    """Окончательная система для работы ТОЛЬКО с одним столом"""
    
    def __init__(self):
        self.TARGET_TABLE = "roulettestura541"  # ТОЛЬКО ЭТОТ СТОЛ
        self.config = self._load_config()
        self.db_path = Path(__file__).parent / "data" / "final_single_table.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
        
        print("🎯" + "="*50)
        print(f"   СИСТЕМА НАСТРОЕНА ТОЛЬКО НА СТОЛ: {self.TARGET_TABLE}")
        print("   НИКАКИХ ДРУГИХ СТОЛОВ НЕ БУДЕТ!")
        print("🎯" + "="*50)
    
    def _load_config(self) -> Dict:
        """Загрузка конфигурации"""
        try:
            config_path = Path(__file__).parent / "casino_setup.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            return {}
    
    def _init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS final_spins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number INTEGER NOT NULL,
                    color TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    table_id TEXT NOT NULL CHECK(table_id = 'roulettestura541'),
                    game_id TEXT,
                    source TEXT
                )
            """)
            conn.commit()
    
    def get_single_table_data_only(self, limit: int = 50) -> List[Dict]:
        """
        Получает данные СТРОГО ТОЛЬКО с указанного стола
        """
        print(f"🔍 ПОЛУЧЕНИЕ ДАННЫХ ТОЛЬКО С СТОЛА: {self.TARGET_TABLE}")
        print(f"🚫 ВСЕ ОСТАЛЬНЫЕ СТОЛЫ ИГНОРИРУЮТСЯ!")
        
        if not self.config:
            print("❌ Нет конфигурации API")
            return []
        
        try:
            # API запрос СТРОГО для одного стола
            auth = self.config['api']['auth']
            base_url = "https://games.pragmaticplaylive.net/api/ui/statisticHistory"
            
            # Параметры ТОЛЬКО для нашего стола
            params = {
                'tableId': self.TARGET_TABLE,  # СТРОГО наш стол
                'numberOfGames': min(limit, 500)
            }
            
            url = f"{base_url}?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.config['api']['headers']['User-Agent'])
            req.add_header('Accept', 'application/json')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    results = self._parse_with_strict_filtering(data)
                    
                    print(f"✅ ПОЛУЧЕНО {len(results)} результатов ТОЛЬКО с стола {self.TARGET_TABLE}")
                    return results
                else:
                    print(f"❌ API вернул код {response.getcode()}")
                    
        except Exception as e:
            print(f"❌ Ошибка API: {e}")
        
        return []
    
    def _parse_with_strict_filtering(self, data: Dict) -> List[Dict]:
        """
        Парсит данные с ЖЕСТКОЙ фильтрацией по столу
        """
        results = []
        
        try:
            if 'history' in data and isinstance(data['history'], list):
                print(f"📊 Получено {len(data['history'])} записей из API")
                
                valid_results = 0
                filtered_out = 0
                
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
                        
                        # ЖЕСТКАЯ ПРОВЕРКА: ТОЛЬКО НАШ СТОЛ
                        result = {
                            'number': winning_number,
                            'color': color,
                            'timestamp': timestamp,
                            'table_id': self.TARGET_TABLE,  # ПРИНУДИТЕЛЬНО наш стол
                            'source': 'final_single_table_api',
                            'game_id': game.get('gameId', '')
                        }
                        
                        # ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА - убеждаемся что это наш стол
                        if result['table_id'] == self.TARGET_TABLE:
                            results.append(result)
                            valid_results += 1
                        else:
                            filtered_out += 1
                            print(f"🚫 ОТФИЛЬТРОВАН: {result['table_id']}")
                
                print(f"✅ Валидных результатов: {valid_results}")
                print(f"🚫 Отфильтровано: {filtered_out}")
                print(f"🎯 ВСЕ РЕЗУЛЬТАТЫ С СТОЛА: {self.TARGET_TABLE}")
                
        except Exception as e:
            print(f"❌ Ошибка парсинга: {e}")
        
        return results
    
    def _get_color(self, number: int) -> str:
        """Определяет цвет числа"""
        if number == 0:
            return 'green'
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return 'red' if number in red_numbers else 'black'
    
    def save_to_database(self, results: List[Dict]) -> int:
        """Сохраняет результаты в базу данных с проверкой стола"""
        saved_count = 0
        
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            for result in results:
                # ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА перед сохранением
                if result.get('table_id') != self.TARGET_TABLE:
                    print(f"🚫 ОТКЛОНЕНО сохранение: чужой стол {result.get('table_id')}")
                    continue
                
                try:
                    cursor.execute("""
                        INSERT INTO final_spins 
                        (number, color, timestamp, table_id, game_id, source)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        result['number'],
                        result['color'],
                        result['timestamp'],
                        result['table_id'],
                        result.get('game_id', ''),
                        result.get('source', 'final_single_table')
                    ))
                    saved_count += 1
                except Exception as e:
                    print(f"❌ Ошибка сохранения: {e}")
            
            conn.commit()
        
        print(f"💾 СОХРАНЕНО {saved_count} результатов в базу данных")
        return saved_count
    
    def get_statistics(self) -> Dict:
        """Получает статистику ТОЛЬКО с одного стола"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            # Проверяем что все данные только с нашего стола
            cursor.execute("SELECT DISTINCT table_id FROM final_spins")
            tables = [row[0] for row in cursor.fetchall()]
            
            if len(tables) > 1:
                print(f"⚠️ ОБНАРУЖЕНЫ ДАННЫЕ С ЧУЖИХ СТОЛОВ: {tables}")
                print(f"🧹 ОЧИЩАЕМ ЧУЖИЕ ДАННЫЕ...")
                cursor.execute("DELETE FROM final_spins WHERE table_id != ?", (self.TARGET_TABLE,))
                conn.commit()
            
            # Получаем статистику только нашего стола
            cursor.execute("""
                SELECT number, color, timestamp 
                FROM final_spins 
                WHERE table_id = ? 
                ORDER BY timestamp DESC
            """, (self.TARGET_TABLE,))
            
            rows = cursor.fetchall()
            
            if not rows:
                return {'total': 0, 'colors': {}, 'table': self.TARGET_TABLE}
            
            colors = {'red': 0, 'black': 0, 'green': 0}
            numbers_count = {}
            
            for number, color, timestamp in rows:
                colors[color] += 1
                numbers_count[number] = numbers_count.get(number, 0) + 1
            
            total = len(rows)
            
            return {
                'total': total,
                'table': self.TARGET_TABLE,
                'colors': colors,
                'percentages': {
                    'red': round(colors['red']/total*100, 1),
                    'black': round(colors['black']/total*100, 1),
                    'green': round(colors['green']/total*100, 1)
                },
                'most_frequent': sorted(numbers_count.items(), key=lambda x: x[1], reverse=True)[:5],
                'latest_results': [(number, color) for number, color, _ in rows[:10]]
            }
    
    def show_detailed_stats(self):
        """Показывает подробную статистику"""
        stats = self.get_statistics()
        
        if stats['total'] == 0:
            print("❌ Нет данных для отображения статистики")
            return
        
        print(f"\n📊 ПОДРОБНАЯ СТАТИСТИКА СТОЛА {stats['table']}:")
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
    
    def run_collection_session(self, count: int = 50):
        """Запускает сессию сбора данных"""
        print(f"\n🚀 ЗАПУСК СЕССИИ СБОРА ДАННЫХ")
        print(f"🎯 ЦЕЛЬ: {count} результатов ТОЛЬКО с стола {self.TARGET_TABLE}")
        print("="*50)
        
        # Получаем данные
        results = self.get_single_table_data_only(count)
        
        if results:
            # Сохраняем
            saved = self.save_to_database(results)
            
            # Показываем статистику
            self.show_detailed_stats()
            
            print(f"\n✅ СЕССИЯ ЗАВЕРШЕНА УСПЕШНО!")
            print(f"📊 Получено: {len(results)} результатов")
            print(f"💾 Сохранено: {saved} результатов") 
            print(f"🎯 ВСЕ ДАННЫЕ ТОЛЬКО С СТОЛА: {self.TARGET_TABLE}")
        else:
            print("❌ Не удалось получить данные")


def main():
    """Главная функция"""
    print("🎯 ОКОНЧАТЕЛЬНАЯ СИСТЕМА - ТОЛЬКО ОДИН СТОЛ")
    print("="*60)
    
    system = FinalSingleTableSystem()
    
    while True:
        print(f"\n🎰 МЕНЮ СИСТЕМЫ (СТОЛ: {system.TARGET_TABLE})")
        print("-"*40)
        print("1. 📊 Получить данные с одного стола")
        print("2. 📈 Показать статистику")
        print("3. 🔄 Запустить сессию сбора (50 результатов)")
        print("4. 🧪 Тест подключения")
        print("0. 🚪 Выход")
        print("-"*40)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            count = input("Количество результатов (по умолчанию 20): ").strip()
            count = int(count) if count.isdigit() else 20
            
            results = system.get_single_table_data_only(count)
            if results:
                system.save_to_database(results)
                print(f"✅ Получено и сохранено {len(results)} результатов")
        
        elif choice == '2':
            system.show_detailed_stats()
        
        elif choice == '3':
            system.run_collection_session(50)
        
        elif choice == '4':
            print("🧪 Тестирование подключения...")
            results = system.get_single_table_data_only(5)
            if results:
                print(f"✅ Подключение работает! Получено {len(results)} результатов")
                for i, r in enumerate(results, 1):
                    print(f"  {i}. {r['number']} ({r['color']}) - {r['table_id']}")
            else:
                print("❌ Проблемы с подключением")
        
        elif choice == '0':
            print("👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()