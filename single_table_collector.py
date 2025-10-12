"""
СБОРЩИК ДАННЫХ ОДНОГО СТОЛА РУЛЕТКИ
==================================

Этот модуль собирает данные только с одного конкретного стола,
игнорируя все остальные столы казино.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

class SingleTableCollector:
    """Сборщик данных одного стола рулетки"""
    
    def __init__(self, config_file="casino_setup.json"):
        self.config = self.load_config(config_file)
        self.target_table_id = None
        self.results = []
        
        if self.config and 'table_info' in self.config:
            self.target_table_id = self.config['table_info'].get('table_id')
        
        print(f"🎯 Настроен сбор данных с стола: {self.target_table_id}")
    
    def load_config(self, config_file):
        """Загружает конфигурацию"""
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
        return None
    
    def get_single_table_history(self, limit=100):
        """Получает историю только указанного стола"""
        if not self.config or not self.target_table_id:
            print("❌ Конфигурация стола не найдена")
            return []
        
        print(f"🔍 Получение истории стола {self.target_table_id}...")
        
        try:
            # Используем API статистики для конкретного стола
            auth = self.config['api']['auth']
            base_url = "https://games.pragmaticplaylive.net/api/ui/statisticHistory"
            
            # Параметры запроса для конкретного стола
            params = {
                'tableId': self.target_table_id,
                'numberOfGames': min(limit, 500),  # Максимум 500
                'JSESSIONID': auth['jsessionid'],
                'ck': str(int(datetime.now().timestamp() * 1000)),
                'game_mode': 'lobby_desktop'
            }
            
            url = f"{base_url}?" + urllib.parse.urlencode(params)
            
            # Создаем запрос
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.config['api']['headers']['User-Agent'])
            req.add_header('Accept', 'application/json, text/plain, */*')
            req.add_header('Accept-Language', 'ru,en-US;q=0.9,en;q=0.8,lt;q=0.7')
            
            # Выполняем запрос
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return self.parse_history_data(data)
                else:
                    print(f"❌ HTTP {response.getcode()}")
                    
        except Exception as e:
            print(f"❌ Ошибка получения данных: {e}")
        
        return []
    
    def parse_history_data(self, data):
        """Парсит данные истории"""
        results = []
        
        try:
            if 'history' in data and isinstance(data['history'], list):
                print(f"📊 Получено {len(data['history'])} записей")
                
                for game in data['history']:
                    if isinstance(game, dict):
                        # Парсим gameResult из API (формат: "25 Red", "0 Green")
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
                            color = api_color if api_color in ['red', 'black', 'green'] else self.get_number_color(winning_number)
                            
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
                                'table_id': self.target_table_id,
                                'game_id': game.get('gameId', ''),
                            }
                            
                            results.append(result)
                
                # Сортируем по времени (новые сначала)
                results.sort(key=lambda x: x['timestamp'], reverse=True)
                
                print(f"✅ Обработано {len(results)} результатов стола {self.target_table_id}")
                
            else:
                print("⚠️ Неожиданный формат данных")
                
        except Exception as e:
            print(f"❌ Ошибка парсинга данных: {e}")
        
        return results
    
    def get_number_color(self, number):
        """Определяет цвет числа рулетки"""
        if number == 0:
            return 'green'
        
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        
        return 'red' if number in red_numbers else 'black'
    
    def filter_by_table(self, all_results):
        """Фильтрует результаты по конкретному столу"""
        if not self.target_table_id:
            return all_results
        
        filtered = [r for r in all_results if r.get('table_id') == self.target_table_id]
        
        print(f"🎯 Отфильтровано {len(filtered)} результатов для стола {self.target_table_id}")
        print(f"   (из {len(all_results)} общих результатов)")
        
        return filtered
    
    def get_table_info(self):
        """Получает информацию о столе"""
        if not self.config or not self.target_table_id:
            return None
        
        try:
            auth = self.config['api']['auth']
            base_url = "https://games.pragmaticplaylive.net/cgibin/tableconfig.jsp"
            
            params = {
                'table_id': self.target_table_id,
                'JSESSIONID': auth['jsessionid'],
                'ck': str(int(datetime.now().timestamp() * 1000)),
                'game_mode': 'lobby_desktop'
            }
            
            url = f"{base_url}?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.config['api']['headers']['User-Agent'])
            req.add_header('Accept', 'application/json, text/plain, */*')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = response.read().decode('utf-8')
                    print(f"ℹ️  Конфигурация стола {self.target_table_id} получена")
                    return data
                    
        except Exception as e:
            print(f"⚠️ Не удалось получить информацию о столе: {e}")
        
        return None
    
    def start_monitoring(self, interval=30):
        """Запускает мониторинг одного стола"""
        print(f"🚀 МОНИТОРИНГ СТОЛА {self.target_table_id}")
        print("=" * 40)
        
        if not self.target_table_id:
            print("❌ ID стола не настроен")
            return
        
        # Получаем информацию о столе
        table_info = self.get_table_info()
        
        # Получаем последние результаты
        results = self.get_single_table_history(50)
        
        if results:
            print(f"\n📊 ПОСЛЕДНИЕ РЕЗУЛЬТАТЫ СТОЛА {self.target_table_id}:")
            print("-" * 50)
            
            for i, result in enumerate(results[:10], 1):
                time_str = result['timestamp'].strftime('%H:%M:%S')
                print(f"  {i:2}. {time_str}: {result['number']:2} ({result['color']})")
            
            # Статистика
            self.show_table_statistics(results)
        else:
            print("❌ Не удалось получить данные стола")
    
    def show_table_statistics(self, results):
        """Показывает статистику конкретного стола"""
        if not results:
            return
        
        print(f"\n📈 СТАТИСТИКА СТОЛА {self.target_table_id}:")
        print("-" * 40)
        
        # Подсчет цветов
        colors = {'red': 0, 'black': 0, 'green': 0}
        numbers = {}
        
        for result in results:
            colors[result['color']] += 1
            numbers[result['number']] = numbers.get(result['number'], 0) + 1
        
        total = len(results)
        
        print(f"Всего результатов: {total}")
        print(f"Красные: {colors['red']} ({colors['red']/total*100:.1f}%)")
        print(f"Черные: {colors['black']} ({colors['black']/total*100:.1f}%)")
        print(f"Зеленые: {colors['green']} ({colors['green']/total*100:.1f}%)")
        
        # Самые частые числа
        most_frequent = sorted(numbers.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\nЧастые числа:")
        for number, count in most_frequent:
            print(f"  {number}: {count} раз ({count/total*100:.1f}%)")
    
    def save_results_to_database(self, results):
        """Сохраняет результаты в базу данных"""
        # Здесь можно добавить сохранение в SQLite
        # Для примера просто сохраняем в JSON
        try:
            data = {
                'table_id': self.target_table_id,
                'casino': self.config.get('casino_name', 'Unknown'),
                'timestamp': datetime.now().isoformat(),
                'results': [
                    {
                        'number': r['number'],
                        'color': r['color'],
                        'timestamp': r['timestamp'].isoformat(),
                        'game_id': r.get('game_id', '')
                    }
                    for r in results
                ]
            }
            
            filename = f"table_{self.target_table_id}_results.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Результаты сохранены в {filename}")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")


def main():
    """Главная функция"""
    try:
        collector = SingleTableCollector()
        collector.start_monitoring()
        
    except KeyboardInterrupt:
        print("\n\n👋 Мониторинг остановлен")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()