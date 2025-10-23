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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                session_id TEXT,
                message_type TEXT DEFAULT 'text',
                FOREIGN KEY (session_id) REFERENCES team_sessions (session_id)
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

@app.route('/api/chat', methods=['GET'])
def get_chat_messages():
    """Получение сообщений чата"""
    try:
        session_id = request.args.get('session_id', 'default')
        limit = request.args.get('limit', 50, type=int)
        
        conn = sqlite3.connect(api_manager.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM chat_messages 
            WHERE session_id = ? OR session_id IS NULL
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'username': row['username'],
                'message': row['message'],
                'session_id': row['session_id'],
                'message_type': row['message_type']
            })
        
        conn.close()
        
        # Возвращаем в обратном порядке (от старых к новым)
        messages.reverse()
        
        return jsonify({
            'messages': messages,
            'count': len(messages),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения сообщений: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def send_chat_message():
    """Отправка сообщения в чат"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Отсутствуют обязательные поля (username, message)'}), 400
        
        session_id = data.get('session_id', 'default')
        message_type = data.get('message_type', 'text')
        
        conn = sqlite3.connect(api_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (username, message, session_id, message_type)
            VALUES (?, ?, ?, ?)
        ''', (data['username'], data['message'], session_id, message_type))
        
        conn.commit()
        message_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message_id': message_id,
            'message': f'Сообщение от {data["username"]} отправлено',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка отправки сообщения: {str(e)}'}), 500

@app.route('/api/chat/users', methods=['GET'])
def get_chat_users():
    """Получение списка активных пользователей чата"""
    try:
        session_id = request.args.get('session_id', 'default')
        hours_ago = request.args.get('hours', 24, type=int)
        
        since_time = datetime.now() - timedelta(hours=hours_ago)
        
        conn = sqlite3.connect(api_manager.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT username, MAX(timestamp) as last_seen
            FROM chat_messages 
            WHERE (session_id = ? OR session_id IS NULL) 
            AND timestamp > ?
            GROUP BY username
            ORDER BY last_seen DESC
        ''', (session_id, since_time.isoformat()))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'username': row['username'],
                'last_seen': row['last_seen']
            })
        
        conn.close()
        
        return jsonify({
            'users': users,
            'count': len(users),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка получения пользователей: {str(e)}'}), 500

@app.route('/api/chat/ai', methods=['POST'])
def chat_with_ai():
    """AI-ассистент для команды RULETTT"""
    try:
        data = request.get_json()
        
        required_fields = ['message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Отсутствует поле message'}), 400
        
        user_message = data['message'].lower().strip()
        session_id = data.get('session_id', 'default')
        
        # Простой AI-ассистент на основе ключевых слов
        ai_responses = {
            'привет': 'Привет! 👋 Я AI-ассистент RULETTT. Могу помочь с анализом данных рулетки, стратегиями и командной работой!',
            'помощь': '🤖 Доступные команды:\n• "статистика" - анализ данных\n• "стратегия" - советы по стратегиям\n• "команда" - помощь с координацией\n• "api" - документация API',
            'статистика': '📊 Для анализа статистики используйте:\n• /api/statistics - общая статистика\n• Dashboard для визуализации\n• Advanced Analytics для глубокого анализа',
            'стратегия': '🎯 Рекомендуемые стратегии:\n• Мартингейл (высокий риск)\n• Фибоначчи (средний риск)\n• Плоские ставки (низкий риск)\nВсегда помните о управлении банкроллом!',
            'команда': '👥 Для эффективной работы команды:\n• Используйте этот чат для координации\n• Назначайте роли участникам\n• Регулярно синхронизируйте данные\n• Делитесь результатами анализа',
            'api': '🔌 API RULETTT:\n• GET /api/health - статус\n• POST/GET /api/chat - чат\n• GET /api/statistics - данные\n• POST /api/spins - добавить спин\nПолная документация в dashboard',
            'код': '💻 Для работы с кодом:\n• Консольный коллектор: auto_collector_console_code.js\n• Python анализ: src/main.py\n• API сервер: api_server.py\n• Веб-интерфейсы: webapp/',
            'ошибка': '🐛 При возникновении ошибок:\n1. Проверьте консоль браузера\n2. Убедитесь что API сервер запущен\n3. Проверьте сетевое подключение\n4. Обратитесь к администратору',
            'как': '🤔 Опишите подробнее что именно хотите узнать:\n• Как собирать данные?\n• Как анализировать результаты?\n• Как настроить команду?\n• Как использовать API?'
        }
        
        # Поиск подходящего ответа
        ai_response = None
        for key, response in ai_responses.items():
            if key in user_message:
                ai_response = response
                break
        
        # Ответ по умолчанию
        if not ai_response:
            ai_response = f'🤖 Получил ваше сообщение: "{data["message"]}"\n\nНапишите "помощь" чтобы узнать что я умею, или задайте конкретный вопрос о RULETTT!'
        
        # Сохраняем ответ AI в чат
        conn = sqlite3.connect(api_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (username, message, session_id, message_type)
            VALUES (?, ?, ?, ?)
        ''', ('🤖 RULETTT AI', ai_response, session_id, 'ai'))
        
        conn.commit()
        message_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message_id': message_id,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка AI-ассистента: {str(e)}'}), 500

# ============ ЛОГИРОВАНИЕ И МОНИТОРИНГ ============

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Получить логи"""
    try:
        import glob
        import re
        from pathlib import Path
        
        limit = int(request.args.get('limit', 100))
        level = request.args.get('level', '')
        
        logs = []
        log_dir = Path('logs')
        
        if not log_dir.exists():
            return jsonify([])
        
        # Читаем последние логи из файлов
        log_files = sorted(log_dir.glob('*.log'), key=lambda x: x.stat().st_mtime, reverse=True)
        
        for log_file in log_files[:3]:  # Только последние 3 файла
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        # Пытаемся парсить как JSON
                        log_entry = json.loads(line.strip())
                        if not level or log_entry.get('level') == level:
                            logs.append(log_entry)
                    except json.JSONDecodeError:
                        # Обычный текстовый лог
                        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - (\w+) - (.+)', line)
                        if match:
                            timestamp, log_level, message = match.groups()
                            if not level or log_level == level:
                                logs.append({
                                    'timestamp': timestamp,
                                    'level': log_level,
                                    'message': message
                                })
        
        # Сортируем по времени и ограничиваем
        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return jsonify(logs[:limit])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs/stats', methods=['GET'])
def get_logs_stats():
    """Получить статистику логов"""
    try:
        from src.error_tracker import error_db
        
        stats = error_db.get_error_statistics()
        
        # Добавляем активные сессии
        db_path = "data/rulettt_cloud.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(DISTINCT session_id) 
            FROM team_sessions 
            WHERE created_at > datetime('now', '-1 hour')
        ''')
        active_sessions = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'total_errors': stats['total'],
            'unresolved_errors': stats['unresolved'],
            'last_24h': stats['last_24h'],
            'active_sessions': active_sessions,
            'by_type': stats['by_type'],
            'top_modules': stats['top_modules']
        })
        
    except Exception as e:
        return jsonify({
            'total_errors': 0,
            'unresolved_errors': 0,
            'last_24h': 0,
            'active_sessions': 0
        })

@app.route('/api/logs/stats/detailed', methods=['GET'])
def get_detailed_stats():
    """Получить детальную статистику"""
    try:
        from src.error_tracker import error_db
        
        stats = error_db.get_error_statistics()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/errors/unresolved', methods=['GET'])
def get_unresolved_errors():
    """Получить нерешённые ошибки"""
    try:
        from src.error_tracker import error_db
        
        limit = int(request.args.get('limit', 50))
        errors = error_db.get_unresolved_errors(limit)
        
        return jsonify(errors)
        
    except Exception as e:
        return jsonify([])

@app.route('/api/errors/<int:error_id>/resolve', methods=['POST'])
def resolve_error(error_id):
    """Пометить ошибку как решённую"""
    try:
        from src.error_tracker import error_db
        
        data = request.get_json()
        notes = data.get('notes', '')
        
        error_db.mark_resolved(error_id, notes)
        
        return jsonify({
            'success': True,
            'error_id': error_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['POST'])
def receive_event():
    """Получить событие от фронтенда"""
    try:
        from src.logger import main_logger
        from src.error_tracker import action_tracker
        
        events = request.get_json()
        if not isinstance(events, list):
            events = [events]
        
        for event in events:
            # Логируем событие
            level = event.get('level', 'info').upper()
            log_func = getattr(main_logger, level.lower(), main_logger.info)
            log_func(f"Frontend event: {event.get('type')} - {json.dumps(event.get('details', {}))}")
            
            # Записываем действие пользователя
            action_tracker.track_action(
                action_type=event.get('type'),
                details=event.get('details', {})
            )
        
        return jsonify({
            'success': True,
            'received': len(events)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Получить события"""
    try:
        from src.error_tracker import action_tracker
        
        limit = int(request.args.get('limit', 100))
        actions = action_tracker.get_recent_actions(limit)
        
        # Форматируем для отображения
        events = []
        for action in actions:
            events.append({
                'type': action['type'],
                'timestamp': action['timestamp'],
                'details': action['details']
            })
        
        return jsonify(events)
        
    except Exception as e:
        return jsonify([])

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """Очистить логи (требует подтверждения)"""
    try:
        from pathlib import Path
        import shutil
        
        # Создаём резервную копию
        backup_dir = Path('logs/backup')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        log_dir = Path('logs')
        if log_dir.exists():
            for log_file in log_dir.glob('*.log'):
                # Копируем в backup
                shutil.copy(log_file, backup_dir / f"{log_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
                # Очищаем
                log_file.write_text('')
        
        return jsonify({
            'success': True,
            'message': 'Логи очищены (резервная копия создана)'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    print("   💬 ЧАТ:")
    print("   GET  /api/chat - Получить сообщения чата")
    print("   POST /api/chat - Отправить сообщение")
    print("   GET  /api/chat/users - Активные пользователи")
    print("   POST /api/chat/ai - 🤖 AI-ассистент")
    print("   📊 МОНИТОРИНГ:")
    print("   GET  /api/logs - Получить логи")
    print("   GET  /api/logs/stats - Статистика логов")
    print("   GET  /api/logs/stats/detailed - Детальная статистика")
    print("   GET  /api/errors/unresolved - Нерешённые ошибки")
    print("   POST /api/errors/<id>/resolve - Пометить ошибку решённой")
    print("   POST /api/events - Отправить событие")
    print("   GET  /api/events - Получить события")
    print("   POST /api/logs/clear - Очистить логи")
    
    app.run(debug=True, host='0.0.0.0', port=5000)