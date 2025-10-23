"""
СБОРЩИК ДАННЫХ РУЛЕТКИ
=====================

Этот модуль отвечает за сбор и хранение данных о выпавших числах в рулетке.

Простыми словами:
- Собирает информацию о каждом спине рулетки
- Сохраняет данные в базу данных
- Позволяет получать статистику за любой период
- Может симулировать игру для тестирования
"""

import sqlite3
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from utils import RouletteUtils


class DataCollector:
    """Класс для сбора и хранения данных о рулетке"""
    
    def __init__(self, db_path: str = "../data/roulette_history.db"):
        """
        Инициализация сборщика данных
        
        Простыми словами: Готовим систему для работы с данными
        
        Args:
            db_path (str): Путь к файлу базы данных
        """
        self.db_path = db_path
        self.utils = RouletteUtils()
        
        # Создаем папку для данных если не существует
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Создаем базу данных и таблицы
        self._init_database()
    
    def _init_database(self):
        """
        Создает базу данных и таблицы
        
        Простыми словами: Готовим место для хранения данных
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица для истории спинов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS spins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number INTEGER NOT NULL,
                    color TEXT NOT NULL,
                    is_even BOOLEAN,
                    dozen INTEGER,
                    column_num INTEGER,
                    timestamp DATETIME NOT NULL,
                    session_id TEXT,
                    casino_name TEXT,
                    table_name TEXT
                )
            """)
            
            # Таблица для пользовательских ставок (для тестирования стратегий)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_bets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    spin_id INTEGER,
                    strategy_name TEXT NOT NULL,
                    bet_type TEXT NOT NULL,
                    bet_amount REAL NOT NULL,
                    bet_numbers TEXT,
                    payout REAL NOT NULL,
                    profit REAL NOT NULL,
                    timestamp DATETIME NOT NULL,
                    FOREIGN KEY (spin_id) REFERENCES spins (id)
                )
            """)
            
            conn.commit()
            print("База данных инициализирована успешно!")
    
    def add_spin(self, number: int, timestamp: datetime = None, session_id: str = None, 
                 casino_name: str = None, table_name: str = None) -> int:
        """
        Добавляет результат спина в базу данных
        
        Простыми словами: Записываем что выпало в рулетке
        
        Args:
            number (int): Выпавшее число (0-36)
            timestamp (datetime): Время спина (если не указано - текущее время)
            session_id (str): ID сессии игры
            casino_name (str): Название казино
            table_name (str): Название стола
            
        Returns:
            int: ID записи в базе данных
        """
        if not self.utils.validate_number(number):
            raise ValueError(f"Некорректное число рулетки: {number}")
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Получаем дополнительную информацию о числе
        color = self.utils.get_color(number)
        is_even = self.utils.is_even(number)
        dozen = self.utils.get_dozen(number)
        column = self.utils.get_column(number)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO spins (number, color, is_even, dozen, column_num, timestamp, 
                                 session_id, casino_name, table_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (number, color, is_even, dozen, column, timestamp, 
                  session_id, casino_name, table_name))
            
            spin_id = cursor.lastrowid
            conn.commit()
            
        print(f"Добавлен спин: число {number} ({color}), время {timestamp}")
        return spin_id
    
    def generate_random_spins(self, count: int, start_date: datetime = None, 
                            session_id: str = "simulation") -> List[int]:
        """
        Генерирует случайные спины для тестирования
        
        Простыми словами: Создаем поддельные результаты рулетки для проверки стратегий
        
        Args:
            count (int): Количество спинов для генерации
            start_date (datetime): Начальная дата (если не указана - неделю назад)
            session_id (str): ID сессии
            
        Returns:
            List[int]: Список сгенерированных чисел
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        
        numbers = []
        time_delta = timedelta(minutes=2)  # Каждые 2 минуты новый спин
        
        print(f"Генерируем {count} случайных спинов...")
        
        for i in range(count):
            number = random.randint(0, 36)  # Случайное число от 0 до 36
            spin_time = start_date + (time_delta * i)
            
            spin_id = self.add_spin(
                number=number,
                timestamp=spin_time,
                session_id=session_id,
                casino_name="Test Casino",
                table_name="Test Table"
            )
            
            numbers.append(number)
            
            # Показываем прогресс каждые 50 спинов
            if (i + 1) % 50 == 0:
                print(f"Сгенерировано {i + 1}/{count} спинов...")
        
        print(f"Генерация завершена! Создано {count} спинов.")
        return numbers
    
    def get_spins_by_period(self, start_date: datetime, end_date: datetime = None) -> List[Dict]:
        """
        Получает спины за определенный период
        
        Простыми словами: Достаем из базы все спины за указанное время
        
        Args:
            start_date (datetime): Начальная дата
            end_date (datetime): Конечная дата (если не указана - до текущего момента)
            
        Returns:
            List[Dict]: Список спинов с полной информацией
        """
        if end_date is None:
            end_date = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM spins 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp
            """, (start_date, end_date))
            
            rows = cursor.fetchall()
            
        # Преобразуем в список словарей
        spins = []
        for row in rows:
            spin = dict(row)
            spin['timestamp'] = datetime.fromisoformat(spin['timestamp'])
            spins.append(spin)
        
        print(f"Найдено {len(spins)} спинов за период с {start_date} по {end_date}")
        return spins
    
    def get_statistics(self, start_date: datetime, end_date: datetime = None) -> Dict:
        """
        Получает статистику за период
        
        Простыми словами: Считаем сколько раз выпадал какой цвет, число и т.д.
        
        Args:
            start_date (datetime): Начальная дата
            end_date (datetime): Конечная дата
            
        Returns:
            Dict: Статистика с различными показателями
        """
        spins = self.get_spins_by_period(start_date, end_date)
        
        if not spins:
            return {"error": "Нет данных за указанный период"}
        
        # Инициализируем счетчики
        stats = {
            "total_spins": len(spins),
            "period": {
                "start": start_date,
                "end": end_date or datetime.now()
            },
            "colors": {"red": 0, "black": 0, "green": 0},
            "even_odd": {"even": 0, "odd": 0, "zero": 0},
            "dozens": {1: 0, 2: 0, 3: 0, "zero": 0},
            "columns": {1: 0, 2: 0, 3: 0, "zero": 0},
            "numbers": {i: 0 for i in range(37)},
            "most_frequent": [],
            "least_frequent": [],
            "longest_streaks": {
                "red": 0, "black": 0, "even": 0, "odd": 0
            }
        }
        
        # Считаем статистику
        for spin in spins:
            number = spin['number']
            color = spin['color']
            
            # Цвета
            stats["colors"][color] += 1
            
            # Четность
            if number == 0:
                stats["even_odd"]["zero"] += 1
            elif number % 2 == 0:
                stats["even_odd"]["even"] += 1
            else:
                stats["even_odd"]["odd"] += 1
            
            # Дюжины
            if number == 0:
                stats["dozens"]["zero"] += 1
            elif 1 <= number <= 12:
                stats["dozens"][1] += 1
            elif 13 <= number <= 24:
                stats["dozens"][2] += 1
            else:
                stats["dozens"][3] += 1
            
            # Колонки
            if number == 0:
                stats["columns"]["zero"] += 1
            else:
                column = ((number - 1) % 3) + 1
                stats["columns"][column] += 1
            
            # Числа
            stats["numbers"][number] += 1
        
        # Находим самые/менее частые числа
        number_counts = [(num, count) for num, count in stats["numbers"].items()]
        number_counts.sort(key=lambda x: x[1], reverse=True)
        
        stats["most_frequent"] = number_counts[:5]  # Топ 5
        stats["least_frequent"] = number_counts[-5:]  # Последние 5
        
        # Вычисляем процентажи
        total = stats["total_spins"]
        stats["percentages"] = {
            "colors": {color: round(count/total*100, 2) for color, count in stats["colors"].items()},
            "even_odd": {key: round(count/total*100, 2) for key, count in stats["even_odd"].items()},
            "dozens": {key: round(count/total*100, 2) for key, count in stats["dozens"].items()},
            "columns": {key: round(count/total*100, 2) for key, count in stats["columns"].items()}
        }
        
        return stats
    
    def clear_data(self, confirm: bool = False):
        """
        Очищает все данные из базы
        
        Простыми словами: Удаляет все записи (ОСТОРОЖНО!)
        
        Args:
            confirm (bool): Подтверждение удаления
        """
        if not confirm:
            print("ВНИМАНИЕ! Это удалит ВСЕ данные. Используйте confirm=True для подтверждения")
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM spins")
            cursor.execute("DELETE FROM test_bets")
            conn.commit()
        
        print("Все данные удалены из базы!")
    
    def export_to_csv(self, filepath: str, start_date: datetime = None, end_date: datetime = None):
        """
        Экспортирует данные в CSV файл
        
        Простыми словами: Сохраняет данные в файл Excel/таблицу
        
        Args:
            filepath (str): Путь к файлу для сохранения
            start_date (datetime): Начальная дата (опционально)
            end_date (datetime): Конечная дата (опционально)
        """
        import csv
        
        if start_date and end_date:
            spins = self.get_spins_by_period(start_date, end_date)
        else:
            spins = self.get_spins_by_period(datetime.min)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if not spins:
                print("Нет данных для экспорта")
                return
            
            fieldnames = spins[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for spin in spins:
                writer.writerow(spin)
        
        print(f"Данные экспортированы в {filepath} ({len(spins)} записей)")


# Тестирование (запускается при запуске файла)
if __name__ == "__main__":
    print("Тестируем сборщик данных...")
    
    # Создаем экземпляр сборщика
    collector = DataCollector("../data/test_roulette.db")
    
    # Генерируем тестовые данные
    print("Генерируем 100 тестовых спинов...")
    start_date = datetime.now() - timedelta(days=3)
    numbers = collector.generate_random_spins(100, start_date)
    
    # Получаем статистику
    print("\nПолучаем статистику...")
    stats = collector.get_statistics(start_date)
    
    print(f"\n=== СТАТИСТИКА ===")
    print(f"Всего спинов: {stats['total_spins']}")
    print(f"Красных: {stats['colors']['red']} ({stats['percentages']['colors']['red']}%)")
    print(f"Черных: {stats['colors']['black']} ({stats['percentages']['colors']['black']}%)")
    print(f"Зеленых: {stats['colors']['green']} ({stats['percentages']['colors']['green']}%)")
    
    print(f"\nСамые частые числа:")
    for num, count in stats['most_frequent']:
        print(f"  {num}: {count} раз")
    
    print("\nТест завершен!")