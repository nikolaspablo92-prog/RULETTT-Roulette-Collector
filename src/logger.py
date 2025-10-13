"""
🔍 RULETTT Advanced Logging System
Централизованная система логирования с ротацией файлов, уровнями логов и детальным контекстом
"""

import logging
import logging.handlers
import json
import traceback
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import functools
import time

# Создаём директорию для логов
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

class ContextFilter(logging.Filter):
    """Добавляет контекстную информацию к логам"""
    
    def filter(self, record):
        record.user_id = getattr(record, 'user_id', 'anonymous')
        record.session_id = getattr(record, 'session_id', 'no-session')
        record.request_id = getattr(record, 'request_id', 'no-request')
        return True

class JSONFormatter(logging.Formatter):
    """Форматирует логи в JSON для лучшей обработки"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'user_id': getattr(record, 'user_id', 'anonymous'),
            'session_id': getattr(record, 'session_id', 'no-session'),
            'request_id': getattr(record, 'request_id', 'no-request'),
        }
        
        # Добавляем exception info если есть
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Добавляем extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'levelno', 'lineno', 'module', 'msecs',
                          'message', 'pathname', 'process', 'processName', 'relativeCreated',
                          'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info',
                          'user_id', 'session_id', 'request_id']:
                log_data[key] = value
        
        return json.dumps(log_data, ensure_ascii=False, default=str)

class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для консоли"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    EMOJIS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨',
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        emoji = self.EMOJIS.get(record.levelname, '📝')
        
        record.levelname = f"{emoji} {color}{record.levelname:8}{self.RESET}"
        return super().format(record)

def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True,
    json_format: bool = False
) -> logging.Logger:
    """
    Настраивает и возвращает logger с указанными параметрами
    
    Args:
        name: Имя логгера
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Логировать в файл
        log_to_console: Логировать в консоль
        json_format: Использовать JSON формат для файлов
    
    Returns:
        Настроенный logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Удаляем существующие handlers чтобы избежать дублирования
    logger.handlers.clear()
    
    # Добавляем контекстный фильтр
    logger.addFilter(ContextFilter())
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = ColoredFormatter(
            '%(levelname)s %(asctime)s [%(name)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handlers
    if log_to_file:
        # Основной лог файл с ротацией (10MB, 5 backup files)
        file_handler = logging.handlers.RotatingFileHandler(
            LOGS_DIR / f"{name}.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        if json_format:
            file_handler.setFormatter(JSONFormatter())
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(user_id)s/%(session_id)s] - '
                '%(module)s:%(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
        
        # Отдельный файл для ERROR и выше
        error_handler = logging.handlers.RotatingFileHandler(
            LOGS_DIR / f"{name}_errors.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        if json_format:
            error_handler.setFormatter(JSONFormatter())
        else:
            error_handler.setFormatter(file_formatter)
        
        logger.addHandler(error_handler)
    
    return logger

def log_execution_time(logger: Optional[logging.Logger] = None):
    """
    Декоратор для логирования времени выполнения функции
    
    Usage:
        @log_execution_time(logger)
        def my_function():
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            start_time = time.time()
            logger.debug(f"🚀 Starting {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(
                    f"✅ {func.__name__} completed in {execution_time:.3f}s",
                    extra={'execution_time': execution_time}
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"❌ {func.__name__} failed after {execution_time:.3f}s: {str(e)}",
                    exc_info=True,
                    extra={'execution_time': execution_time}
                )
                raise
        
        return wrapper
    return decorator

def log_function_call(logger: Optional[logging.Logger] = None, log_args: bool = False):
    """
    Декоратор для логирования вызовов функций с аргументами
    
    Usage:
        @log_function_call(logger, log_args=True)
        def my_function(a, b):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            if log_args:
                logger.debug(
                    f"📞 Calling {func.__name__}",
                    extra={
                        'function': func.__name__,
                        'args': str(args)[:200],  # Ограничиваем длину
                        'kwargs': str(kwargs)[:200]
                    }
                )
            else:
                logger.debug(f"📞 Calling {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"✅ {func.__name__} returned successfully")
                return result
            except Exception as e:
                logger.error(
                    f"❌ {func.__name__} raised {type(e).__name__}: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator

class LoggerContext:
    """
    Context manager для добавления контекстной информации к логам
    
    Usage:
        with LoggerContext(logger, user_id='123', session_id='abc'):
            logger.info("Some message")  # Будет включать user_id и session_id
    """
    
    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)

# Создаём основные логгеры для приложения
main_logger = setup_logger('rulettt', level=logging.INFO, json_format=False)
api_logger = setup_logger('rulettt.api', level=logging.INFO, json_format=False)
collector_logger = setup_logger('rulettt.collector', level=logging.DEBUG, json_format=False)
analyzer_logger = setup_logger('rulettt.analyzer', level=logging.INFO, json_format=False)
auth_logger = setup_logger('rulettt.auth', level=logging.INFO, json_format=True)
error_logger = setup_logger('rulettt.errors', level=logging.ERROR, json_format=True)

# Вспомогательные функции для быстрого использования
def log_info(message: str, **kwargs):
    """Быстрое логирование INFO"""
    main_logger.info(message, extra=kwargs)

def log_warning(message: str, **kwargs):
    """Быстрое логирование WARNING"""
    main_logger.warning(message, extra=kwargs)

def log_error(message: str, exc_info: bool = True, **kwargs):
    """Быстрое логирование ERROR"""
    error_logger.error(message, exc_info=exc_info, extra=kwargs)

def log_critical(message: str, exc_info: bool = True, **kwargs):
    """Быстрое логирование CRITICAL"""
    error_logger.critical(message, exc_info=exc_info, extra=kwargs)

def log_debug(message: str, **kwargs):
    """Быстрое логирование DEBUG"""
    main_logger.debug(message, extra=kwargs)

if __name__ == "__main__":
    # Тестирование системы логирования
    print("🔍 Testing RULETTT Logging System...")
    print(f"📁 Logs directory: {LOGS_DIR}")
    print()
    
    # Тест основных уровней
    main_logger.debug("This is a DEBUG message")
    main_logger.info("This is an INFO message")
    main_logger.warning("This is a WARNING message")
    main_logger.error("This is an ERROR message")
    main_logger.critical("This is a CRITICAL message")
    
    # Тест контекста
    with LoggerContext(main_logger, user_id='test_user', session_id='test_session'):
        main_logger.info("Message with context")
    
    # Тест декоратора
    @log_execution_time(main_logger)
    def test_function():
        time.sleep(0.1)
        return "Success"
    
    result = test_function()
    
    # Тест обработки ошибок
    try:
        raise ValueError("Test error for logging")
    except Exception:
        log_error("Caught an exception during testing")
    
    print()
    print("✅ Logging system test completed!")
    print(f"📄 Check logs in: {LOGS_DIR}")
