"""
🔐 Менеджер аутентификации и авторизации
Двухуровневая система: админы (постоянные токены) + клиенты (временные ключи)
"""

import sqlite3
import secrets
import hashlib
import jwt
import bcrypt
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class AuthManager:
    """Управление аутентификацией и авторизацией"""
    
    # Роли и разрешения
    ROLES = {
        "super_admin": {
            "name": "Супер-администратор",
            "permissions": [
                "full_access",
                "user_management",
                "key_generation",
                "bot_control",
                "view_logs",
                "system_config"
            ]
        },
        "team_member": {
            "name": "Член команды",
            "permissions": [
                "bot_control",
                "view_stats",
                "limited_key_generation",
                "view_logs"
            ]
        },
        "observer": {
            "name": "Наблюдатель",
            "permissions": [
                "view_stats",
                "view_logs"
            ]
        }
    }
    
    def __init__(self, db_path: str, secret_key: str):
        """
        Инициализация менеджера аутентификации
        
        Args:
            db_path: Путь к базе данных SQLite
            secret_key: Секретный ключ для JWT
        """
        self.db_path = Path(db_path)
        self.secret_key = secret_key
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Создание таблиц для аутентификации"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица администраторов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                is_active BOOLEAN DEFAULT 1,
                permissions TEXT,
                created_by TEXT
            )
        ''')
        
        # Таблица временных ключей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT UNIQUE NOT NULL,
                client_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                valid_hours TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                usage_count INTEGER DEFAULT 0,
                max_usage INTEGER DEFAULT 1000,
                last_used_at TEXT,
                created_by_admin TEXT,
                ip_whitelist TEXT,
                notes TEXT
            )
        ''')
        
        # Таблица логов доступа
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_type TEXT NOT NULL,
                identifier TEXT NOT NULL,
                endpoint TEXT,
                method TEXT,
                status_code INTEGER,
                timestamp TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                hidden_mode BOOLEAN DEFAULT 0
            )
        ''')
        
        # Таблица активных сессий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_token TEXT UNIQUE NOT NULL,
                user_type TEXT NOT NULL,
                identifier TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                last_activity TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ База данных аутентификации инициализирована")
    
    # ============================================
    # АДМИНИСТРАТОРЫ
    # ============================================
    
    def create_admin(self, username: str, password: str, role: str, 
                     created_by: str = "system") -> Dict:
        """
        Создание нового администратора
        
        Args:
            username: Имя пользователя
            password: Пароль (будет захэширован)
            role: Роль (super_admin, team_member, observer)
            created_by: Кто создал пользователя
        
        Returns:
            Словарь с информацией о созданном пользователе
        """
        if role not in self.ROLES:
            raise ValueError(f"❌ Неверная роль: {role}. Доступные: {list(self.ROLES.keys())}")
        
        # Хэширование пароля
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        permissions = json.dumps(self.ROLES[role]["permissions"])
        created_at = datetime.now().isoformat()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO admin_users (username, password_hash, role, created_at, 
                                       is_active, permissions, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, role, created_at, 1, permissions, created_by))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            print(f"✅ Администратор создан: {username} (роль: {self.ROLES[role]['name']})")
            
            return {
                "id": user_id,
                "username": username,
                "role": role,
                "role_name": self.ROLES[role]["name"],
                "permissions": self.ROLES[role]["permissions"],
                "created_at": created_at
            }
        
        except sqlite3.IntegrityError:
            raise ValueError(f"❌ Пользователь '{username}' уже существует")
    
    def authenticate_admin(self, username: str, password: str, 
                          hidden_mode: bool = False) -> Optional[Dict]:
        """
        Аутентификация администратора
        
        Args:
            username: Имя пользователя
            password: Пароль
            hidden_mode: Скрытый режим (не логировать в публичных логах)
        
        Returns:
            JWT токен и информация о пользователе или None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM admin_users 
            WHERE username = ? AND is_active = 1
        ''', (username,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return None
        
        # Проверка пароля
        if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            conn.close()
            return None
        
        # Обновление времени последнего входа
        cursor.execute('''
            UPDATE admin_users 
            SET last_login = ? 
            WHERE id = ?
        ''', (datetime.now().isoformat(), user['id']))
        
        conn.commit()
        conn.close()
        
        # Генерация JWT токена
        payload = {
            'user_id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'permissions': json.loads(user['permissions']),
            'exp': datetime.utcnow() + timedelta(hours=8),  # Токен на 8 часов
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        
        # Логирование (если не скрытый режим)
        if not hidden_mode:
            self.log_access('admin', username, '/auth/login', 'POST', 200)
        
        print(f"✅ Вход выполнен: {username} (роль: {user['role']})")
        if hidden_mode:
            print("🔒 Скрытый режим активирован")
        
        return {
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'role_name': self.ROLES[user['role']]['name'],
                'permissions': json.loads(user['permissions'])
            }
        }
    
    def verify_admin_token(self, token: str) -> Optional[Dict]:
        """
        Проверка JWT токена администратора
        
        Args:
            token: JWT токен
        
        Returns:
            Декодированный payload или None
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("❌ Токен истёк")
            return None
        except jwt.InvalidTokenError:
            print("❌ Неверный токен")
            return None
    
    # ============================================
    # ВРЕМЕННЫЕ КЛЮЧИ ДЛЯ КЛИЕНТОВ
    # ============================================
    
    def generate_temp_key(self, client_name: str, valid_hours: List[int], 
                         ttl_minutes: int = 120, max_usage: int = 1000,
                         created_by_admin: str = "admin",
                         ip_whitelist: List[str] = None,
                         notes: str = "") -> Tuple[str, Dict]:
        """
        Генерация временного ключа для клиента
        
        Args:
            client_name: Имя клиента
            valid_hours: Часы работы ключа (список 0-23)
            ttl_minutes: Время жизни ключа в минутах
            max_usage: Максимальное количество использований
            created_by_admin: Имя администратора, создавшего ключ
            ip_whitelist: Список разрешённых IP (опционально)
            notes: Заметки
        
        Returns:
            Кортеж (raw_key, key_info)
        """
        # Генерация уникального ключа
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=ttl_minutes)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO temp_keys (key_hash, client_name, created_at, expires_at,
                                 valid_hours, status, usage_count, max_usage,
                                 created_by_admin, ip_whitelist, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            key_hash,
            client_name,
            created_at.isoformat(),
            expires_at.isoformat(),
            json.dumps(valid_hours),
            'active',
            0,
            max_usage,
            created_by_admin,
            json.dumps(ip_whitelist) if ip_whitelist else None,
            notes
        ))
        
        key_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Ключ создан для '{client_name}'")
        print(f"   Действителен: {ttl_minutes} минут")
        print(f"   Часы работы: {valid_hours}")
        print(f"   Максимум использований: {max_usage}")
        
        return raw_key, {
            'id': key_id,
            'client_name': client_name,
            'created_at': created_at.isoformat(),
            'expires_at': expires_at.isoformat(),
            'valid_hours': valid_hours,
            'max_usage': max_usage
        }
    
    def validate_temp_key(self, key: str, ip_address: str = None) -> Dict:
        """
        Проверка временного ключа
        
        Args:
            key: Временный ключ
            ip_address: IP адрес клиента (для проверки whitelist)
        
        Returns:
            Словарь с результатом валидации
        """
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM temp_keys 
            WHERE key_hash = ? AND status = 'active'
        ''', (key_hash,))
        
        key_data = cursor.fetchone()
        
        if not key_data:
            conn.close()
            return {'valid': False, 'reason': 'key_not_found', 'message': '❌ Ключ не найден или неактивен'}
        
        # Проверка срока действия
        expires_at = datetime.fromisoformat(key_data['expires_at'])
        if datetime.now() > expires_at:
            conn.close()
            return {'valid': False, 'reason': 'key_expired', 'message': '❌ Ключ истёк'}
        
        # Проверка расписания (часы работы)
        valid_hours = json.loads(key_data['valid_hours'])
        current_hour = datetime.now().hour
        if current_hour not in valid_hours:
            conn.close()
            return {
                'valid': False, 
                'reason': 'outside_working_hours', 
                'message': f'❌ Вне рабочих часов. Доступно: {valid_hours}',
                'current_hour': current_hour,
                'valid_hours': valid_hours
            }
        
        # Проверка лимита использования
        if key_data['usage_count'] >= key_data['max_usage']:
            conn.close()
            return {'valid': False, 'reason': 'usage_limit_exceeded', 'message': '❌ Превышен лимит использования'}
        
        # Проверка IP whitelist (если указан)
        if key_data['ip_whitelist'] and ip_address:
            whitelist = json.loads(key_data['ip_whitelist'])
            if ip_address not in whitelist:
                conn.close()
                return {'valid': False, 'reason': 'ip_not_whitelisted', 'message': '❌ IP адрес не в белом списке'}
        
        # Обновляем счетчик использования и время последнего использования
        cursor.execute('''
            UPDATE temp_keys 
            SET usage_count = usage_count + 1,
                last_used_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), key_data['id']))
        
        conn.commit()
        conn.close()
        
        return {
            'valid': True,
            'client_name': key_data['client_name'],
            'usage_count': key_data['usage_count'] + 1,
            'max_usage': key_data['max_usage'],
            'expires_at': key_data['expires_at']
        }
    
    def revoke_temp_key(self, key_hash: str) -> bool:
        """
        Отзыв временного ключа
        
        Args:
            key_hash: Хэш ключа
        
        Returns:
            True если ключ успешно отозван
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE temp_keys 
            SET status = 'revoked' 
            WHERE key_hash = ?
        ''', (key_hash,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            print(f"✅ Ключ отозван: {key_hash[:16]}...")
            return True
        else:
            print(f"❌ Ключ не найден: {key_hash[:16]}...")
            return False
    
    def list_temp_keys(self, status: str = None) -> List[Dict]:
        """
        Список всех временных ключей
        
        Args:
            status: Фильтр по статусу (active, expired, revoked)
        
        Returns:
            Список словарей с информацией о ключах
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM temp_keys WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM temp_keys ORDER BY created_at DESC')
        
        keys = []
        for row in cursor.fetchall():
            keys.append({
                'id': row['id'],
                'key_hash': row['key_hash'][:16] + "...",  # Показываем только начало
                'client_name': row['client_name'],
                'created_at': row['created_at'],
                'expires_at': row['expires_at'],
                'valid_hours': json.loads(row['valid_hours']),
                'status': row['status'],
                'usage_count': row['usage_count'],
                'max_usage': row['max_usage'],
                'last_used_at': row['last_used_at'],
                'created_by_admin': row['created_by_admin']
            })
        
        conn.close()
        return keys
    
    def cleanup_expired_keys(self) -> int:
        """
        Очистка истёкших ключей
        
        Returns:
            Количество обновлённых записей
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE temp_keys 
            SET status = 'expired' 
            WHERE status = 'active' AND expires_at < ?
        ''', (current_time,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            print(f"🗑️ Истекло ключей: {rows_affected}")
        
        return rows_affected
    
    # ============================================
    # ЛОГИРОВАНИЕ
    # ============================================
    
    def log_access(self, user_type: str, identifier: str, endpoint: str, 
                   method: str, status_code: int, ip_address: str = None,
                   user_agent: str = None, hidden_mode: bool = False):
        """
        Логирование доступа к системе
        
        Args:
            user_type: Тип пользователя (admin, client)
            identifier: Идентификатор (username или client_name)
            endpoint: Эндпоинт API
            method: HTTP метод
            status_code: HTTP статус код
            ip_address: IP адрес
            user_agent: User-Agent
            hidden_mode: Скрытый режим (не показывать в общих логах)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO access_logs (user_type, identifier, endpoint, method, 
                                    status_code, timestamp, ip_address, 
                                    user_agent, hidden_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_type,
            identifier,
            endpoint,
            method,
            status_code,
            datetime.now().isoformat(),
            ip_address,
            user_agent,
            1 if hidden_mode else 0
        ))
        
        conn.commit()
        conn.close()
    
    def get_access_logs(self, limit: int = 100, include_hidden: bool = False) -> List[Dict]:
        """
        Получение логов доступа
        
        Args:
            limit: Количество записей
            include_hidden: Включать скрытые записи
        
        Returns:
            Список словарей с логами
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if include_hidden:
            cursor.execute('SELECT * FROM access_logs ORDER BY timestamp DESC LIMIT ?', (limit,))
        else:
            cursor.execute('''
                SELECT * FROM access_logs 
                WHERE hidden_mode = 0 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
        
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return logs


# ============================================
# ДЕМОНСТРАЦИЯ ИСПОЛЬЗОВАНИЯ
# ============================================

if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔐 ДЕМОНСТРАЦИЯ СИСТЕМЫ АУТЕНТИФИКАЦИИ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Инициализация
    auth = AuthManager(
        db_path="data/auth.db",
        secret_key="your-secret-key-change-in-production"
    )
    
    print("\n1️⃣ Создание администратора...")
    try:
        admin = auth.create_admin(
            username="admin",
            password="secure_password_123",
            role="super_admin"
        )
        print(f"   ID: {admin['id']}")
        print(f"   Роль: {admin['role_name']}")
        print(f"   Права: {', '.join(admin['permissions'])}")
    except ValueError as e:
        print(f"   {e}")
    
    print("\n2️⃣ Вход администратора...")
    result = auth.authenticate_admin("admin", "secure_password_123", hidden_mode=True)
    if result:
        print(f"   Токен: {result['token'][:50]}...")
        print(f"   Пользователь: {result['user']['username']}")
        
        # Проверка токена
        print("\n3️⃣ Проверка токена...")
        payload = auth.verify_admin_token(result['token'])
        if payload:
            print(f"   ✅ Токен валиден")
            print(f"   Пользователь: {payload['username']}")
            print(f"   Права: {', '.join(payload['permissions'])}")
    
    print("\n4️⃣ Генерация временного ключа...")
    raw_key, key_info = auth.generate_temp_key(
        client_name="Клиент А",
        valid_hours=[9, 10, 11, 14, 15, 16, 17, 18, 19, 20],
        ttl_minutes=120,
        max_usage=500,
        created_by_admin="admin"
    )
    
    print(f"\n   ⚠️ ВАЖНО: Ключ показывается только один раз!")
    print(f"   Ключ: {raw_key}")
    print(f"   Клиент: {key_info['client_name']}")
    print(f"   Истекает: {key_info['expires_at']}")
    
    print("\n5️⃣ Проверка временного ключа...")
    validation = auth.validate_temp_key(raw_key)
    if validation['valid']:
        print(f"   ✅ Ключ валиден")
        print(f"   Клиент: {validation['client_name']}")
        print(f"   Использовано: {validation['usage_count']}/{validation['max_usage']}")
    else:
        print(f"   {validation['message']}")
    
    print("\n6️⃣ Список всех ключей...")
    keys = auth.list_temp_keys()
    print(f"   Всего ключей: {len(keys)}")
    for key in keys[:3]:
        print(f"   - {key['client_name']}: {key['usage_count']}/{key['max_usage']} ({key['status']})")
    
    print("\n7️⃣ Очистка истёкших ключей...")
    expired_count = auth.cleanup_expired_keys()
    print(f"   Очищено: {expired_count} ключей")
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Демонстрация завершена!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
