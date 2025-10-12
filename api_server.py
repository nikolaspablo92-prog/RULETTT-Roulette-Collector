"""
🎲 RULETTT - API Сервер для Облачного Хранения
===============================================

REST API для интеграции с веб-интерфейсом и мобильными приложениями
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import sqlite3
import os
from typing import Dict, List, Optional

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда

class RouletteAPI:
    """API для работы с данными рулетки"""
    
    def __init__(self):
        self.db_path = "data/rulettt_cloud.db"
        self.ensure_database()
    
    def ensure_database(self):
        """Проверка и создание базы данных"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем таблицы если их нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roulette_spins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                casino_name TEXT NOT NULL,
                number INTEGER NOT NULL,
                color TEXT NOT NULL,
                session_id TEXT,
                table_id TEXT,
                synced_to_cloud BOOLEAN DEFAULT FALSE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                strategy_name TEXT NOT NULL,
                bet_amount REAL NOT NULL,
                win_amount REAL DEFAULT 0,
                session_id TEXT,
                profit REAL GENERATED ALWAYS AS (win_amount - bet_amount) STORED
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                team_name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                total_spins INTEGER DEFAULT 0,
                total_profit REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()

api_manager = RouletteAPI()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'service': 'RULETTT Cloud API'
    })

@app.route('/api/spins', methods=['POST'])
def add_spin():
    """Добавление нового спина рулетки"""
    try:
        data = request.get_json()
        
        required_fields = ['casino_name', 'number', 'color']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Отсутствуют обязательные поля'}), 400
        
        conn = sqlite3.connect(api_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO roulette_spins 
            (casino_name, number, color, session_id, table_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['casino_name'],
            data['number'],
            data['color'],
            data.get('session_id'),
            data.get('table_id')
        ))
        
        spin_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'spin_id': spin_id,
            'message': f'Спин добавлен: {data["number"]} ({data["color"]})'
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Ошибка добавления спина: {str(e)}'}), 500

@app.route('/api/spins', methods=['GET'])
def get_spins():
    """Получение списка спинов с фильтрацией"""
    try:
        # Параметры фильтрации
        casino = request.args.get('casino')
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        conn = sqlite3.connect(api_manager.db_path)
        conn.row_factory = sqlite3.Row  # Возвращать словари
        cursor = conn.cursor()
        
        # Строим SQL запрос с фильтрами
        query = "SELECT * FROM roulette_spins WHERE 1=1"
        params = []
        
        if casino:
            query += " AND casino_name = ?"
            params.append(casino)
            
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        spins = [dict(row) for row in cursor.fetchall()]
        
        # Получаем общее количество
        count_query = "SELECT COUNT(*) FROM roulette_spins WHERE 1=1"
        count_params = []
        
        if casino:
            count_query += " AND casino_name = ?"
            count_params.append(casino)
            
        if session_id:
            count_query += " AND session_id = ?"
            count_params.append(session_id)
        
        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'spins': spins,
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': (offset + limit) < total_count
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения спинов: {str(e)}'}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Получение статистики по спинам и стратегиям"""
    try:
        session_id = request.args.get('session_id')
        days = int(request.args.get('days', 7))  # За последние N дней
        
        conn = sqlite3.connect(api_manager.db_path)
        cursor = conn.cursor()
        
        # Фильтр по времени
        date_filter = datetime.now() - timedelta(days=days)
        
        # Статистика спинов
        spin_query = '''
            SELECT 
                casino_name,
                COUNT(*) as total_spins,
                COUNT(CASE WHEN color = 'red' THEN 1 END) as red_count,
                COUNT(CASE WHEN color = 'black' THEN 1 END) as black_count,
                COUNT(CASE WHEN color = 'green' THEN 1 END) as green_count,
                AVG(number) as avg_number
            FROM roulette_spins 
            WHERE timestamp >= ?
        '''
        
        params = [date_filter.isoformat()]
        
        if session_id:
            spin_query += " AND session_id = ?"
            params.append(session_id)
        
        spin_query += " GROUP BY casino_name"
        
        cursor.execute(spin_query, params)
        spin_stats = []
        for row in cursor.fetchall():
            spin_stats.append({
                'casino': row[0],
                'total_spins': row[1],
                'red_count': row[2],
                'black_count': row[3],
                'green_count': row[4],
                'avg_number': round(row[5], 2) if row[5] else 0,
                'red_percentage': round((row[2] / row[1]) * 100, 1) if row[1] > 0 else 0,
                'black_percentage': round((row[3] / row[1]) * 100, 1) if row[1] > 0 else 0,
                'green_percentage': round((row[4] / row[1]) * 100, 1) if row[1] > 0 else 0
            })
        
        # Статистика стратегий
        strategy_query = '''
            SELECT 
                strategy_name,
                COUNT(*) as sessions,
                SUM(profit) as total_profit,
                AVG(profit) as avg_profit,
                MAX(profit) as max_profit,
                MIN(profit) as min_profit,
                COUNT(CASE WHEN profit > 0 THEN 1 END) as winning_sessions
            FROM strategy_results 
            WHERE timestamp >= ?
        '''
        
        strategy_params = [date_filter.isoformat()]
        
        if session_id:
            strategy_query += " AND session_id = ?"
            strategy_params.append(session_id)
        
        strategy_query += " GROUP BY strategy_name"
        
        cursor.execute(strategy_query, strategy_params)
        strategy_stats = []
        for row in cursor.fetchall():
            win_rate = (row[7] / row[1]) * 100 if row[1] > 0 else 0
            strategy_stats.append({
                'strategy': row[0],
                'sessions': row[1],
                'total_profit': round(row[2], 2) if row[2] else 0,
                'avg_profit': round(row[3], 2) if row[3] else 0,
                'max_profit': round(row[4], 2) if row[4] else 0,
                'min_profit': round(row[5], 2) if row[5] else 0,
                'winning_sessions': row[7],
                'win_rate': round(win_rate, 1)
            })
        
        # Общая статистика
        cursor.execute('''
            SELECT 
                COUNT(*) as total_spins,
                COUNT(DISTINCT casino_name) as casinos_count,
                COUNT(DISTINCT session_id) as sessions_count
            FROM roulette_spins 
            WHERE timestamp >= ?
        ''', [date_filter.isoformat()])
        
        general_stats = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'period': f'Last {days} days',
            'general': {
                'total_spins': general_stats[0],
                'casinos_count': general_stats[1],
                'sessions_count': general_stats[2]
            },
            'casinos': spin_stats,
            'strategies': strategy_stats,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения статистики: {str(e)}'}), 500

@app.route('/api/strategies', methods=['POST'])
def add_strategy_result():
    """Добавление результата стратегии"""
    try:
        data = request.get_json()
        
        required_fields = ['strategy_name', 'bet_amount', 'win_amount']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Отсутствуют обязательные поля'}), 400
        
        conn = sqlite3.connect(api_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO strategy_results 
            (strategy_name, bet_amount, win_amount, session_id)
            VALUES (?, ?, ?, ?)
        ''', (
            data['strategy_name'],
            data['bet_amount'],
            data['win_amount'],
            data.get('session_id')
        ))
        
        result_id = cursor.lastrowid
        profit = data['win_amount'] - data['bet_amount']
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'result_id': result_id,
            'profit': round(profit, 2),
            'message': f'Результат стратегии добавлен: {profit:+.2f}'
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Ошибка добавления результата: {str(e)}'}), 500

@app.route('/api/sessions', methods=['POST'])
def create_team_session():
    """Создание новой командной сессии"""
    try:
        data = request.get_json()
        
        if 'team_name' not in data:
            return jsonify({'error': 'Требуется имя команды'}), 400
        
        session_id = f"team_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conn = sqlite3.connect(api_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO team_sessions (session_id, team_name)
            VALUES (?, ?)
        ''', (session_id, data['team_name']))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'team_name': data['team_name'],
            'created_at': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Ошибка создания сессии: {str(e)}'}), 500

@app.route('/api/sessions', methods=['GET'])
def get_team_sessions():
    """Получение списка командных сессий"""
    try:
        conn = sqlite3.connect(api_manager.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, 
                   COUNT(rs.id) as spin_count,
                   COUNT(sr.id) as strategy_count
            FROM team_sessions s
            LEFT JOIN roulette_spins rs ON s.session_id = rs.session_id
            LEFT JOIN strategy_results sr ON s.session_id = sr.session_id
            GROUP BY s.id
            ORDER BY s.created_at DESC
        ''')
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'session_id': row['session_id'],
                'team_name': row['team_name'],
                'created_at': row['created_at'],
                'active': bool(row['active']),
                'spin_count': row['spin_count'],
                'strategy_count': row['strategy_count']
            })
        
        conn.close()
        
        return jsonify({'sessions': sessions})
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения сессий: {str(e)}'}), 500

@app.route('/api/export/<format>', methods=['GET'])
def export_data(format):
    """Экспорт данных в различных форматах"""
    try:
        session_id = request.args.get('session_id')
        days = int(request.args.get('days', 30))
        
        date_filter = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(api_manager.db_path)
        
        # Строим запросы с фильтрами
        spin_query = "SELECT * FROM roulette_spins WHERE timestamp >= ?"
        strategy_query = "SELECT * FROM strategy_results WHERE timestamp >= ?"
        params = [date_filter.isoformat()]
        
        if session_id:
            spin_query += " AND session_id = ?"
            strategy_query += " AND session_id = ?"
            params.append(session_id)
        
        # Получаем данные
        cursor = conn.cursor()
        cursor.execute(spin_query, params)
        spins = [dict(zip([col[0] for col in cursor.description], row)) 
                for row in cursor.fetchall()]
        
        cursor.execute(strategy_query, params)
        strategies = [dict(zip([col[0] for col in cursor.description], row)) 
                     for row in cursor.fetchall()]
        
        conn.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'json':
            filename = f"rulettt_export_{timestamp}.json"
            filepath = f"exports/{filename}"
            
            export_data = {
                'export_info': {
                    'timestamp': datetime.now().isoformat(),
                    'period_days': days,
                    'session_id': session_id,
                    'total_spins': len(spins),
                    'total_strategies': len(strategies)
                },
                'roulette_spins': spins,
                'strategy_results': strategies
            }
            
            os.makedirs("exports", exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            return send_file(filepath, as_attachment=True, 
                           download_name=filename, mimetype='application/json')
        
        else:
            return jsonify({'error': 'Поддерживается только формат JSON'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Ошибка экспорта: {str(e)}'}), 500

@app.route('/api/realtime/feed', methods=['GET'])
def get_realtime_feed():
    """Получение ленты активности в реальном времени"""
    try:
        limit = int(request.args.get('limit', 50))
        
        conn = sqlite3.connect(api_manager.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Объединяем последние спины и результаты стратегий
        cursor.execute('''
            SELECT 'spin' as type, timestamp, casino_name as source, 
                   number || ' (' || color || ')' as description,
                   session_id
            FROM roulette_spins
            UNION ALL
            SELECT 'strategy' as type, timestamp, strategy_name as source,
                   'Прибыль: ' || printf('%.2f', win_amount - bet_amount) as description,
                   session_id
            FROM strategy_results
            ORDER BY timestamp DESC
            LIMIT ?
        ''', [limit])
        
        feed = []
        for row in cursor.fetchall():
            feed.append({
                'type': row['type'],
                'timestamp': row['timestamp'],
                'source': row['source'],
                'description': row['description'],
                'session_id': row['session_id']
            })
        
        conn.close()
        
        return jsonify({
            'feed': feed,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения ленты: {str(e)}'}), 500

if __name__ == '__main__':
    print("🎲 Запуск RULETTT Cloud API сервера...")
    print("📡 API доступен на: http://localhost:5000")
    print("📊 Endpoint'ы:")
    print("   GET  /api/health - Проверка работоспособности")
    print("   POST /api/spins - Добавить спин")
    print("   GET  /api/spins - Получить спины")
    print("   GET  /api/statistics - Статистика")
    print("   POST /api/strategies - Добавить результат стратегии")
    print("   POST /api/sessions - Создать команд. сессию")
    print("   GET  /api/sessions - Список сессий")
    print("   GET  /api/export/<format> - Экспорт данных")
    print("   GET  /api/realtime/feed - Лента активности")
    
    app.run(debug=True, host='0.0.0.0', port=5000)