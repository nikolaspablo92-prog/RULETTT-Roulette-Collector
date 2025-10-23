"""
🚨 RULETTT Advanced Error Tracker
Детальное отслеживание ошибок с контекстом, stack traces и автоматическими отчётами
"""

import traceback
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from collections import deque
import threading
import hashlib

from src.logger import setup_logger, log_error

# Настройка
ERRORS_DB = Path(__file__).parent.parent / "data" / "errors.db"
ERRORS_DB.parent.mkdir(exist_ok=True)

# Logger для error tracker
tracker_logger = setup_logger('rulettt.error_tracker', json_format=True)

class UserActionTracker:
    """Отслеживает действия пользователя перед ошибкой"""
    
    def __init__(self, max_actions: int = 50):
        self.max_actions = max_actions
        self._actions = deque(maxlen=max_actions)
        self._lock = threading.Lock()
    
    def track_action(self, action_type: str, details: Dict[str, Any]):
        """Записывает действие пользователя"""
        with self._lock:
            action = {
                'timestamp': datetime.utcnow().isoformat(),
                'type': action_type,
                'details': details
            }
            self._actions.append(action)
            tracker_logger.debug(f"Tracked action: {action_type}", extra=details)
    
    def get_recent_actions(self, count: Optional[int] = None) -> List[Dict]:
        """Возвращает последние N действий"""
        with self._lock:
            if count is None:
                return list(self._actions)
            return list(self._actions)[-count:]
    
    def clear(self):
        """Очищает историю действий"""
        with self._lock:
            self._actions.clear()

# Глобальный трекер действий
action_tracker = UserActionTracker()

class ErrorDatabase:
    """База данных для хранения ошибок"""
    
    def __init__(self, db_path: Path = ERRORS_DB):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализирует таблицы БД"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_hash TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    error_type TEXT NOT NULL,
                    error_message TEXT NOT NULL,
                    module TEXT,
                    function TEXT,
                    line_number INTEGER,
                    stack_trace TEXT,
                    context TEXT,
                    user_actions TEXT,
                    user_id TEXT,
                    session_id TEXT,
                    request_id TEXT,
                    resolved BOOLEAN DEFAULT 0,
                    resolution_notes TEXT,
                    occurrences INTEGER DEFAULT 1,
                    first_seen TEXT,
                    last_seen TEXT
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_error_hash ON errors(error_hash)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON errors(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_resolved ON errors(resolved)
            """)
            
            conn.commit()
    
    def save_error(self, error_data: Dict[str, Any]) -> int:
        """
        Сохраняет ошибку в БД
        Returns: ID записи
        """
        error_hash = self._generate_error_hash(error_data)
        
        with sqlite3.connect(self.db_path) as conn:
            # Проверяем, существует ли уже такая ошибка
            existing = conn.execute(
                "SELECT id, occurrences FROM errors WHERE error_hash = ? AND resolved = 0",
                (error_hash,)
            ).fetchone()
            
            if existing:
                # Увеличиваем счётчик повторений
                error_id, occurrences = existing
                conn.execute(
                    "UPDATE errors SET occurrences = ?, last_seen = ? WHERE id = ?",
                    (occurrences + 1, error_data['timestamp'], error_id)
                )
                tracker_logger.info(
                    f"Updated existing error #{error_id}, occurrences: {occurrences + 1}"
                )
                return error_id
            else:
                # Создаём новую запись
                cursor = conn.execute("""
                    INSERT INTO errors (
                        error_hash, timestamp, level, error_type, error_message,
                        module, function, line_number, stack_trace, context,
                        user_actions, user_id, session_id, request_id,
                        first_seen, last_seen
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    error_hash,
                    error_data['timestamp'],
                    error_data.get('level', 'ERROR'),
                    error_data['error_type'],
                    error_data['error_message'],
                    error_data.get('module'),
                    error_data.get('function'),
                    error_data.get('line_number'),
                    error_data.get('stack_trace'),
                    json.dumps(error_data.get('context', {}), ensure_ascii=False),
                    json.dumps(error_data.get('user_actions', []), ensure_ascii=False),
                    error_data.get('user_id'),
                    error_data.get('session_id'),
                    error_data.get('request_id'),
                    error_data['timestamp'],
                    error_data['timestamp']
                ))
                error_id = cursor.lastrowid
                tracker_logger.info(f"Saved new error #{error_id}")
                return error_id
    
    def get_unresolved_errors(self, limit: int = 100) -> List[Dict]:
        """Возвращает список нерешённых ошибок"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM errors 
                WHERE resolved = 0 
                ORDER BY occurrences DESC, last_seen DESC
                LIMIT ?
            """, (limit,)).fetchall()
            
            return [dict(row) for row in rows]
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику по ошибкам"""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            
            # Общее количество
            stats['total_errors'] = conn.execute(
                "SELECT COUNT(*) FROM errors"
            ).fetchone()[0]
            
            # Нерешённые
            stats['unresolved_errors'] = conn.execute(
                "SELECT COUNT(*) FROM errors WHERE resolved = 0"
            ).fetchone()[0]
            
            # По типам
            stats['by_type'] = dict(conn.execute("""
                SELECT error_type, COUNT(*) as count 
                FROM errors WHERE resolved = 0
                GROUP BY error_type
                ORDER BY count DESC
                LIMIT 10
            """).fetchall())
            
            # За последние 24 часа
            stats['last_24h'] = conn.execute("""
                SELECT COUNT(*) FROM errors 
                WHERE datetime(timestamp) > datetime('now', '-1 day')
            """).fetchone()[0]
            
            # Топ модулей с ошибками
            stats['top_modules'] = dict(conn.execute("""
                SELECT module, COUNT(*) as count 
                FROM errors WHERE resolved = 0 AND module IS NOT NULL
                GROUP BY module
                ORDER BY count DESC
                LIMIT 5
            """).fetchall())
            
            return stats
    
    def mark_resolved(self, error_id: int, notes: str = ""):
        """Помечает ошибку как решённую"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE errors SET resolved = 1, resolution_notes = ? WHERE id = ?",
                (notes, error_id)
            )
            tracker_logger.info(f"Marked error #{error_id} as resolved")
    
    def _generate_error_hash(self, error_data: Dict) -> str:
        """Генерирует уникальный хэш для ошибки (для группировки)"""
        # Используем тип ошибки, модуль, функцию и первые 2 строки стектрейса
        hash_parts = [
            error_data['error_type'],
            error_data.get('module', ''),
            error_data.get('function', ''),
        ]
        
        if error_data.get('stack_trace'):
            # Берём только первые 200 символов стектрейса
            hash_parts.append(error_data['stack_trace'][:200])
        
        hash_string = '|'.join(str(p) for p in hash_parts)
        return hashlib.md5(hash_string.encode()).hexdigest()

# Глобальная БД ошибок
error_db = ErrorDatabase()

class ErrorTracker:
    """Основной класс для отслеживания ошибок"""
    
    def __init__(self):
        self.error_handlers: List[Callable] = []
        self.context_data: Dict[str, Any] = {}
    
    def add_error_handler(self, handler: Callable):
        """Добавляет обработчик ошибок (для уведомлений и т.д.)"""
        self.error_handlers.append(handler)
    
    def set_context(self, **kwargs):
        """Устанавливает контекстные данные для последующих ошибок"""
        self.context_data.update(kwargs)
    
    def clear_context(self):
        """Очищает контекстные данные"""
        self.context_data.clear()
    
    def track_error(
        self,
        exception: Exception,
        level: str = "ERROR",
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        additional_context: Optional[Dict] = None
    ) -> int:
        """
        Отслеживает и сохраняет ошибку с полным контекстом
        
        Returns: ID ошибки в БД
        """
        # Собираем информацию об ошибке
        exc_type, exc_value, exc_traceback = sys.exc_info()
        
        error_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'error_type': type(exception).__name__,
            'error_message': str(exception),
            'stack_trace': ''.join(traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )) if exc_traceback else traceback.format_exc(),
            'user_id': user_id,
            'session_id': session_id,
            'request_id': request_id,
            'user_actions': action_tracker.get_recent_actions(20),
            'context': {
                **self.context_data,
                **(additional_context or {})
            }
        }
        
        # Пытаемся извлечь информацию о месте ошибки
        if exc_traceback:
            tb = traceback.extract_tb(exc_traceback)
            if tb:
                last_frame = tb[-1]
                error_data['module'] = Path(last_frame.filename).stem
                error_data['function'] = last_frame.name
                error_data['line_number'] = last_frame.lineno
        
        # Логируем ошибку
        log_error(
            f"{error_data['error_type']}: {error_data['error_message']}",
            exc_info=True,
            **{
                'user_id': user_id,
                'session_id': session_id,
                'request_id': request_id
            }
        )
        
        # Сохраняем в БД
        error_id = error_db.save_error(error_data)
        
        # Вызываем обработчики (для уведомлений)
        for handler in self.error_handlers:
            try:
                handler(error_data, error_id)
            except Exception as e:
                tracker_logger.error(
                    f"Error handler failed: {e}",
                    exc_info=True
                )
        
        return error_id
    
    def track_exception_decorator(self, **kwargs):
        """
        Декоратор для автоматического отслеживания ошибок в функциях
        
        Usage:
            @error_tracker.track_exception_decorator(user_id='123')
            def my_function():
                raise ValueError("Error")
        """
        def decorator(func):
            def wrapper(*args, **func_kwargs):
                try:
                    return func(*args, **func_kwargs)
                except Exception as e:
                    self.track_error(e, **kwargs)
                    raise
            return wrapper
        return decorator

# Глобальный error tracker
error_tracker = ErrorTracker()

def track_action(action_type: str, **details):
    """Удобная функция для отслеживания действий пользователя"""
    action_tracker.track_action(action_type, details)

def get_error_report() -> Dict[str, Any]:
    """Генерирует полный отчёт по ошибкам"""
    stats = error_db.get_error_statistics()
    unresolved = error_db.get_unresolved_errors(limit=10)
    
    return {
        'generated_at': datetime.utcnow().isoformat(),
        'statistics': stats,
        'top_unresolved_errors': unresolved
    }

if __name__ == "__main__":
    print("🚨 Testing RULETTT Error Tracker...")
    print(f"📁 Database: {ERRORS_DB}")
    print()
    
    # Тест отслеживания действий
    track_action('button_click', button='test_button', page='dashboard')
    track_action('navigation', from_page='dashboard', to_page='analytics')
    track_action('data_load', table='roulette_spins', rows=100)
    
    # Тест отслеживания ошибки
    try:
        # Симулируем ошибку
        result = 10 / 0
    except Exception as e:
        error_id = error_tracker.track_error(
            e,
            user_id='test_user',
            session_id='test_session',
            additional_context={'operation': 'division_test'}
        )
        print(f"✅ Error tracked with ID: {error_id}")
    
    # Тест повторной ошибки (должна увеличить счётчик)
    try:
        result = 10 / 0
    except Exception as e:
        error_id = error_tracker.track_error(e, user_id='test_user')
        print(f"✅ Same error tracked again with ID: {error_id}")
    
    # Получаем статистику
    print("\n📊 Error Statistics:")
    report = get_error_report()
    print(json.dumps(report['statistics'], indent=2, ensure_ascii=False))
    
    print("\n✅ Error tracker test completed!")
