"""
🎲 RULETTT - Система Облачного Хранения Данных
===========================================

Интеграция с различными облачными сервисами для хранения данных рулетки
"""

import json
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any

class CloudDataManager:
    """Менеджер облачного хранения данных RULETTT"""
    
    def __init__(self):
        self.local_db = "data/rulettt_cloud.db"
        self.api_endpoints = {
            "firebase": "https://rulettt-default-rtdb.firebaseio.com/",
            "supabase": "https://your-project.supabase.co/rest/v1/",
            "airtable": "https://api.airtable.com/v0/your-base/",
            "github_gist": "https://api.github.com/gists"
        }
        self.setup_database()
        
    def setup_database(self):
        """Инициализация локальной базы данных"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        # Таблица результатов рулетки
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roulette_spins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                casino_name TEXT NOT NULL,
                number INTEGER NOT NULL,
                color TEXT NOT NULL,
                session_id TEXT,
                table_id TEXT,
                synced_to_cloud BOOLEAN DEFAULT FALSE,
                cloud_id TEXT
            )
        ''')
        
        # Таблица стратегий и результатов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                strategy_name TEXT NOT NULL,
                bet_amount REAL NOT NULL,
                win_amount REAL DEFAULT 0,
                session_id TEXT,
                data_range TEXT,
                synced_to_cloud BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Таблица команды и активности
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT,
                session_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Локальная база данных инициализирована")

    async def save_spin_data(self, casino: str, number: int, color: str, 
                           session_id: str = None, table_id: str = None):
        """Сохранение данных спина рулетки"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO roulette_spins 
            (casino_name, number, color, session_id, table_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (casino, number, color, session_id, table_id))
        
        conn.commit()
        spin_id = cursor.lastrowid
        conn.close()
        
        # Асинхронная синхронизация с облаком
        await self.sync_to_cloud('roulette_spins', spin_id)
        
        print(f"💾 Спин сохранен: {casino} | {number} ({color})")
        return spin_id

    async def save_strategy_result(self, strategy: str, bet_amount: float, 
                                 win_amount: float, session_id: str = None,
                                 data_range: str = None):
        """Сохранение результатов стратегии"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO strategy_results 
            (strategy_name, bet_amount, win_amount, session_id, data_range)
            VALUES (?, ?, ?, ?, ?)
        ''', (strategy, bet_amount, win_amount, session_id, data_range))
        
        conn.commit()
        result_id = cursor.lastrowid
        conn.close()
        
        await self.sync_to_cloud('strategy_results', result_id)
        
        profit = win_amount - bet_amount
        print(f"📊 Результат стратегии: {strategy} | Прибыль: {profit:+.2f}")
        return result_id

    async def sync_to_cloud(self, table_name: str, record_id: int):
        """Синхронизация данных с облачными сервисами"""
        try:
            conn = sqlite3.connect(self.local_db)
            cursor = conn.cursor()
            
            # Получаем несинхронизированные данные
            cursor.execute(f'''
                SELECT * FROM {table_name} 
                WHERE id = ? AND synced_to_cloud = FALSE
            ''', (record_id,))
            
            record = cursor.fetchone()
            if not record:
                return
            
            # Преобразуем в словарь
            columns = [description[0] for description in cursor.description]
            data = dict(zip(columns, record))
            
            # Синхронизация с Firebase
            firebase_id = await self.sync_to_firebase(table_name, data)
            
            # Синхронизация с GitHub Gist (как бэкап)
            gist_id = await self.sync_to_github_gist(table_name, data)
            
            # Обновляем статус синхронизации
            cursor.execute(f'''
                UPDATE {table_name} 
                SET synced_to_cloud = TRUE, cloud_id = ?
                WHERE id = ?
            ''', (firebase_id, record_id))
            
            conn.commit()
            conn.close()
            
            print(f"☁️ Данные синхронизированы: {table_name}#{record_id}")
            
        except Exception as e:
            print(f"❌ Ошибка синхронизации: {e}")

    async def sync_to_firebase(self, table_name: str, data: Dict) -> str:
        """Синхронизация с Firebase Realtime Database"""
        try:
            url = f"{self.api_endpoints['firebase']}{table_name}.json"
            
            # Подготавливаем данные для Firebase
            firebase_data = {
                **data,
                'timestamp': data.get('timestamp', datetime.now().isoformat()),
                'source': 'rulettt_collector'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=firebase_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('name', '')  # Firebase возвращает уникальный ключ
                    else:
                        print(f"❌ Firebase ошибка: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"❌ Firebase синхронизация не удалась: {e}")
            return None

    async def sync_to_github_gist(self, table_name: str, data: Dict) -> str:
        """Бэкап данных в GitHub Gist"""
        try:
            # Создаем JSON файл с данными
            filename = f"rulettt_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            content = json.dumps(data, indent=2, ensure_ascii=False, default=str)
            
            gist_data = {
                "description": f"RULETTT {table_name} backup",
                "public": False,
                "files": {
                    filename: {
                        "content": content
                    }
                }
            }
            
            headers = {
                "Authorization": "token YOUR_GITHUB_TOKEN",
                "Accept": "application/vnd.github.v3+json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_endpoints['github_gist'], 
                    json=gist_data, 
                    headers=headers
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return result.get('id', '')
                    else:
                        print(f"❌ GitHub Gist ошибка: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"❌ GitHub Gist бэкап не удался: {e}")
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики данных"""
        conn = sqlite3.connect(self.local_db)
        
        # Статистика спинов
        spins_df = pd.read_sql_query('''
            SELECT casino_name, COUNT(*) as total_spins, 
                   COUNT(CASE WHEN color = 'red' THEN 1 END) as red_count,
                   COUNT(CASE WHEN color = 'black' THEN 1 END) as black_count,
                   COUNT(CASE WHEN color = 'green' THEN 1 END) as green_count,
                   MIN(timestamp) as first_spin,
                   MAX(timestamp) as last_spin
            FROM roulette_spins 
            GROUP BY casino_name
        ''', conn)
        
        # Статистика стратегий
        strategy_df = pd.read_sql_query('''
            SELECT strategy_name, 
                   COUNT(*) as sessions,
                   SUM(win_amount - bet_amount) as total_profit,
                   AVG(win_amount - bet_amount) as avg_profit,
                   MAX(win_amount - bet_amount) as max_profit,
                   MIN(win_amount - bet_amount) as min_profit
            FROM strategy_results 
            GROUP BY strategy_name
        ''', conn)
        
        conn.close()
        
        return {
            'spins_by_casino': spins_df.to_dict('records'),
            'strategy_performance': strategy_df.to_dict('records'),
            'total_spins': spins_df['total_spins'].sum() if not spins_df.empty else 0,
            'total_sessions': len(strategy_df) if not strategy_df.empty else 0
        }

    async def export_data(self, format: str = 'json', 
                         start_date: str = None, end_date: str = None) -> str:
        """Экспорт данных в различных форматах"""
        conn = sqlite3.connect(self.local_db)
        
        # Фильтр по датам
        date_filter = ""
        if start_date and end_date:
            date_filter = f"WHERE timestamp BETWEEN '{start_date}' AND '{end_date}'"
        
        # Получаем все данные
        spins_df = pd.read_sql_query(f'''
            SELECT * FROM roulette_spins {date_filter}
            ORDER BY timestamp DESC
        ''', conn)
        
        strategies_df = pd.read_sql_query(f'''
            SELECT * FROM strategy_results {date_filter}
            ORDER BY timestamp DESC
        ''', conn)
        
        conn.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'json':
            filename = f"rulettt_export_{timestamp}.json"
            export_data = {
                'export_info': {
                    'timestamp': datetime.now().isoformat(),
                    'total_spins': len(spins_df),
                    'total_strategies': len(strategies_df),
                    'date_range': f"{start_date} to {end_date}" if start_date else "All time"
                },
                'roulette_spins': spins_df.to_dict('records'),
                'strategy_results': strategies_df.to_dict('records')
            }
            
            with open(f"exports/{filename}", 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
                
        elif format.lower() == 'csv':
            filename_spins = f"rulettt_spins_{timestamp}.csv"
            filename_strategies = f"rulettt_strategies_{timestamp}.csv"
            
            spins_df.to_csv(f"exports/{filename_spins}", index=False, encoding='utf-8')
            strategies_df.to_csv(f"exports/{filename_strategies}", index=False, encoding='utf-8')
            
            filename = f"Exported: {filename_spins}, {filename_strategies}"
            
        elif format.lower() == 'excel':
            filename = f"rulettt_export_{timestamp}.xlsx"
            
            with pd.ExcelWriter(f"exports/{filename}", engine='openpyxl') as writer:
                spins_df.to_excel(writer, sheet_name='Roulette Spins', index=False)
                strategies_df.to_excel(writer, sheet_name='Strategy Results', index=False)
                
                # Добавляем статистику
                stats = self.get_statistics()
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        print(f"📤 Данные экспортированы: {filename}")
        return filename

    async def team_activity_log(self, user_name: str, action_type: str, 
                              description: str, session_id: str = None):
        """Логирование активности команды"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO team_activity 
            (user_name, action_type, description, session_id)
            VALUES (?, ?, ?, ?)
        ''', (user_name, action_type, description, session_id))
        
        conn.commit()
        activity_id = cursor.lastrowid
        conn.close()
        
        # Уведомление в реальном времени
        await self.broadcast_activity(user_name, action_type, description)
        
        print(f"👥 Активность: {user_name} - {action_type}")
        return activity_id

    async def broadcast_activity(self, user: str, action: str, description: str):
        """Трансляция активности команде в реальном времени"""
        # Здесь будет интеграция с WebSocket или Server-Sent Events
        activity_data = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'action': action,
            'description': description,
            'type': 'team_activity'
        }
        
        # Отправка через WebSocket всем подключенным клиентам
        print(f"📡 Трансляция активности: {user} - {action}")

# Пример использования
async def main():
    """Демонстрация системы облачного хранения"""
    print("🎲 Запуск системы облачного хранения RULETTT")
    
    # Инициализация менеджера
    cloud_manager = CloudDataManager()
    
    # Симуляция сбора данных рулетки
    await cloud_manager.save_spin_data("Stake.com", 17, "black", "session_001", "table_vip_1")
    await cloud_manager.save_spin_data("BC.Game", 32, "red", "session_001", "table_standard_2")
    await cloud_manager.save_spin_data("Roobet", 0, "green", "session_002", "table_vip_1")
    
    # Симуляция результатов стратегий
    await cloud_manager.save_strategy_result("Мартингейл красное", 10.0, 20.0, "session_001", "last_100_spins")
    await cloud_manager.save_strategy_result("Фибоначчи четное", 15.0, 12.0, "session_001", "last_50_spins")
    
    # Логирование активности команды
    await cloud_manager.team_activity_log("Коллектор", "data_collection", "Собрано 150 спинов с Stake.com", "session_001")
    await cloud_manager.team_activity_log("Аналитик", "strategy_analysis", "Анализ стратегии Мартингейл завершен", "session_001")
    
    # Получение статистики
    stats = cloud_manager.get_statistics()
    print("\n📊 Текущая статистика:")
    print(f"  Всего спинов: {stats['total_spins']}")
    print(f"  Сессий стратегий: {stats['total_sessions']}")
    
    # Экспорт данных
    json_file = await cloud_manager.export_data('json')
    excel_file = await cloud_manager.export_data('excel')
    
    print(f"\n✅ Система облачного хранения готова к работе!")
    print(f"📁 Экспортированы файлы: {json_file}, {excel_file}")

if __name__ == "__main__":
    # Создаем папку для экспорта
    import os
    os.makedirs("exports", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Запускаем демонстрацию
    asyncio.run(main())