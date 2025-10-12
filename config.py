"""
КОНФИГУРАЦИОННЫЙ ФАЙЛ ДЛЯ НАСТРОЙКИ СИСТЕМЫ
==========================================

Здесь вы можете настроить систему под ваше конкретное казино.
"""

# 🎰 НАСТРОЙКИ КАЗИНО
CASINO_CONFIG = {
    'name': 'Ваше Казино',  # Название казино
    'timezone': 'Europe/Moscow',  # Часовой пояс
    'currency': 'RUB',  # Валюта
    'min_bet': 10,  # Минимальная ставка
    'max_bet': 100000,  # Максимальная ставка
}

# 🔗 НАСТРОЙКИ ПОДКЛЮЧЕНИЯ
CONNECTION_CONFIG = {
    'method': 'mock',  # mock, api, scraping, manual
    'update_interval': 120,  # Интервал обновления в секундах
    'timeout': 30,  # Таймаут подключения
    'retry_attempts': 3,  # Количество попыток при ошибке
}

# 📡 API НАСТРОЙКИ (если используете API)
API_CONFIG = {
    'base_url': 'https://api.yourcasino.com',
    'endpoints': {
        'live_results': '/roulette/live',
        'history': '/roulette/history',
        'balance': '/account/balance'
    },
    'headers': {
        'Authorization': 'Bearer YOUR_API_KEY_HERE',
        'Content-Type': 'application/json',
        'User-Agent': 'RouletteAnalyzer/1.0'
    },
    'rate_limit': 60  # Запросов в минуту
}

# 🕷️ WEB SCRAPING НАСТРОЙКИ (если используете скрапинг)
SCRAPING_CONFIG = {
    'base_url': 'https://yourcasino.com',
    'live_page': '/live-roulette',
    'selectors': {
        'number': '.roulette-number',
        'color': '.roulette-color', 
        'timestamp': '.result-time',
        'spin_id': '.spin-id'
    },
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
}

# 💰 НАСТРОЙКИ СТРАТЕГИЙ
STRATEGY_CONFIG = {
    'base_bet': 100,  # Базовая ставка
    'max_bet': 10000,  # Максимальная ставка
    'bankroll': 100000,  # Общий банкролл
    'stop_loss': 20000,  # Стоп-лосс
    'take_profit': 50000,  # Тейк-профит
    'multipliers': {
        'color': 2.1,  # Мультипликатор для цветов
        'dozen': 3.1,  # Мультипликатор для дюжин
        'number': 36.0  # Мультипликатор для чисел
    }
}

# 📊 НАСТРОЙКИ АНАЛИЗА
ANALYSIS_CONFIG = {
    'min_data_points': 100,  # Минимум данных для анализа
    'history_days': 30,  # Дней истории для анализа
    'update_frequency': 300,  # Частота обновления анализа (сек)
    'alert_thresholds': {
        'long_streak': 8,  # Длинная серия
        'hot_number': 10,  # Горячее число
        'deviation': 0.1  # Отклонение от нормы
    }
}

# 🔔 НАСТРОЙКИ УВЕДОМЛЕНИЙ
NOTIFICATION_CONFIG = {
    'enabled': True,
    'telegram': {
        'bot_token': 'YOUR_BOT_TOKEN',
        'chat_id': 'YOUR_CHAT_ID',
        'enabled': False
    },
    'email': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'your.email@gmail.com',
        'password': 'your_app_password',
        'to_email': 'alerts@yourdomain.com',
        'enabled': False
    },
    'desktop': {
        'enabled': True  # Системные уведомления Windows
    }
}

# 🛡️ НАСТРОЙКИ БЕЗОПАСНОСТИ
SECURITY_CONFIG = {
    'max_daily_loss': 50000,  # Максимальная дневная потеря
    'max_session_time': 14400,  # Максимальное время сессии (4 часа)
    'force_break_after': 7200,  # Принудительный перерыв после (2 часа)
    'min_break_duration': 1800,  # Минимальная длительность перерыва (30 мин)
    'enable_limits': True  # Включить лимиты
}

# 📁 НАСТРОЙКИ ФАЙЛОВ И ЛОГОВ
FILE_CONFIG = {
    'database_path': 'data/roulette.db',
    'log_path': 'logs/',
    'export_path': 'exports/',
    'backup_path': 'backups/',
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'backup_frequency': 86400  # Резервное копирование каждые 24 часа
}

# 🎨 НАСТРОЙКИ ИНТЕРФЕЙСА
UI_CONFIG = {
    'language': 'ru',  # ru, en
    'theme': 'default',  # default, dark, light
    'show_tips': True,  # Показывать подсказки
    'auto_refresh': True,  # Автообновление данных
    'refresh_interval': 30  # Интервал автообновления (сек)
}