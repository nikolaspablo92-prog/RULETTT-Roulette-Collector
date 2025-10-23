# 📊 RULETTT - Руководство по Системе Логирования

## 🎯 Обзор

Комплексная система логирования для отслеживания всех событий, ошибок и действий пользователей в реальном времени.

## 🏗️ Архитектура

```
📦 Система логирования
├── 🐍 Backend (Python)
│   ├── src/logger.py - Централизованное логирование
│   ├── src/error_tracker.py - Отслеживание ошибок
│   └── api_server.py - API endpoints для логов
│
├── 🌐 Frontend (JavaScript)
│   ├── webapp/event-tracker.js - Трекер событий
│   └── webapp/logs_dashboard.html - Dashboard
│
└── 💾 Хранилище
    ├── logs/*.log - Файлы логов (ротация 10MB)
    └── data/errors.db - SQLite БД ошибок
```

## 🚀 Быстрый старт

### 1. Backend интеграция

```python
# В любом Python файле:

from src.logger import main_logger, log_execution_time
from src.error_tracker import error_tracker, track_exception_decorator

# Простое логирование
main_logger.info("✅ Операция выполнена")
main_logger.error("❌ Ошибка выполнения")

# Автоматический замер времени
@log_execution_time(main_logger)
def my_function():
    # Время выполнения логируется автоматически
    return "result"

# Автоматическое отслеживание ошибок
@track_exception_decorator
def risky_operation():
    # Ошибки автоматически записываются в БД
    raise ValueError("Что-то пошло не так")
```

### 2. Frontend интеграция

```html
<!-- В HTML страницу перед </body>: -->

<script src="event-tracker.js"></script>
<script>
    // Автоматически отслеживаются:
    // - Все клики
    // - Навигация
    // - JS ошибки
    // - Performance
    // - Network requests
    
    // Кастомные события:
    window.roulettTracker.trackCustomEvent('user_login', {
        userId: '123',
        timestamp: Date.now()
    });
</script>
```

### 3. API Integration

```javascript
// Отправка событий на сервер
fetch('/api/events', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        type: 'button_click',
        details: {button: 'start_game'},
        level: 'info'
    })
});

// Получение логов
fetch('/api/logs?limit=100&level=ERROR')
    .then(r => r.json())
    .then(logs => console.log(logs));
```

## 📚 API Endpoints

### Логи

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/logs` | GET | Получить логи (с фильтрами) |
| `/api/logs/stats` | GET | Статистика логов |
| `/api/logs/stats/detailed` | GET | Детальная статистика |
| `/api/logs/clear` | POST | Очистить логи (с backup) |

**Параметры запроса:**
- `limit` (int) - Количество записей (по умолчанию: 100)
- `level` (str) - Уровень: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `module` (str) - Фильтр по модулю
- `search` (str) - Поиск в сообщениях

**Пример:**
```
GET /api/logs?limit=50&level=ERROR&module=api_server
```

### Ошибки

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/errors/unresolved` | GET | Нерешённые ошибки |
| `/api/errors/{id}/resolve` | POST | Пометить решённой |

**Пример:**
```json
POST /api/errors/123/resolve
{
    "notes": "Исправлено в коммите abc123"
}
```

### События

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/events` | POST | Отправить событие |
| `/api/events` | GET | Получить события |

**Формат события:**
```json
{
    "type": "button_click",
    "level": "info",
    "details": {
        "button": "start_game",
        "timestamp": 1234567890
    }
}
```

## 🎨 Dashboard

Откройте в браузере: `http://localhost:8080/logs_dashboard.html`

### Возможности:

1. **📜 Вкладка "Логи"**
   - Фильтрация по уровню (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - Поиск по модулю и тексту
   - Просмотр stack trace для ошибок
   - Автообновление каждые 10 секунд

2. **🚨 Вкладка "Ошибки"**
   - Список нерешённых ошибок
   - Группировка одинаковых ошибок
   - Счётчик повторений
   - Детали: модуль, функция, строка, stack trace

3. **📊 Вкладка "События"**
   - Лента всех событий от фронтенда
   - Клики, навигация, формы
   - JSON детали каждого события

4. **📈 Вкладка "Статистика"**
   - Общее количество ошибок
   - Нерешённые ошибки
   - Ошибки за 24 часа
   - Топ модулей с ошибками
   - Статистика по типам ошибок

## 🔧 Конфигурация

### Logger (src/logger.py)

```python
from src.logger import setup_logger

# Создание кастомного логгера
my_logger = setup_logger(
    name='my_module',           # Имя логгера
    level=logging.INFO,         # Уровень: DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_to_file=True,           # Писать в файл
    log_to_console=True,        # Выводить в консоль
    json_format=False           # Формат: JSON или текст
)

# Использование
my_logger.info("Сообщение")
my_logger.debug("Отладка")
my_logger.warning("Предупреждение")
my_logger.error("Ошибка")
my_logger.critical("Критическая ошибка")
```

### Error Tracker (src/error_tracker.py)

```python
from src.error_tracker import error_tracker, action_tracker

# Отслеживание действия пользователя
action_tracker.track_action(
    action_type='button_click',
    details={'button': 'start', 'page': 'dashboard'}
)

# Отслеживание ошибки
try:
    risky_operation()
except Exception as e:
    error_tracker.track_error(
        error=e,
        context={'user': 'user123', 'operation': 'risky'}
    )
```

### Event Tracker (webapp/event-tracker.js)

```javascript
// Конфигурация в начале файла:
const CONFIG = {
    apiEndpoint: '/api/events',
    flushInterval: 5000,        // Интервал отправки (мс)
    maxQueueSize: 100,          // Макс размер очереди
    debug: true                 // Debug режим
};

// Отключить автотрекинг:
window.roulettTracker.stopTracking();

// Включить обратно:
window.roulettTracker.init();
```

## 📋 Уровни логирования

| Уровень | Использование | Пример |
|---------|---------------|--------|
| **DEBUG** | Отладочная информация | `logger.debug("Переменная x = 10")` |
| **INFO** | Обычные события | `logger.info("✅ Пользователь вошёл")` |
| **WARNING** | Предупреждения | `logger.warning("⚠️ Медленный запрос")` |
| **ERROR** | Ошибки | `logger.error("❌ Не удалось сохранить")` |
| **CRITICAL** | Критические ошибки | `logger.critical("🔥 База данных недоступна")` |

## 🎭 Декораторы

### @log_execution_time

Автоматически измеряет и логирует время выполнения функции:

```python
from src.logger import main_logger, log_execution_time

@log_execution_time(main_logger)
def slow_function():
    # Код функции
    pass

# В логах будет:
# ⏱️ slow_function выполнена за 0.523 секунд
```

### @log_function_call

Логирует вызовы функции с аргументами:

```python
from src.logger import main_logger, log_function_call

@log_function_call(main_logger, log_args=True)
def calculate(x, y, operation="add"):
    # Код функции
    pass

# В логах будет:
# 📞 Вызов функции: calculate(x=10, y=5, operation='add')
```

### @track_exception_decorator

Автоматически отслеживает и записывает ошибки в БД:

```python
from src.error_tracker import track_exception_decorator

@track_exception_decorator
def risky_operation():
    raise ValueError("Ошибка!")

# Ошибка автоматически:
# - Записана в data/errors.db
# - Сохранены последние 20 действий пользователя
# - Создан stack trace
# - Подсчитаны повторения
```

## 🔍 Примеры использования

### 1. Логирование API запроса

```python
from src.logger import api_logger, log_execution_time
from src.error_tracker import action_tracker, error_tracker

@app.route('/api/spins', methods=['POST'])
@log_execution_time(api_logger)
def add_spin():
    try:
        data = request.get_json()
        
        # Логируем действие
        action_tracker.track_action('api_call', {
            'endpoint': '/api/spins',
            'method': 'POST'
        })
        
        # Обработка
        result = process_spin(data)
        
        api_logger.info(f"✅ Спин добавлен: {data['number']}")
        return jsonify(result)
        
    except Exception as e:
        error_tracker.track_error(e, context={'data': data})
        api_logger.error(f"❌ Ошибка: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

### 2. Контекстное логирование

```python
from src.logger import LoggerContext, main_logger

def process_user_request(user_id, session_id):
    # Все логи в этом блоке будут содержать user_id и session_id
    with LoggerContext(main_logger, user_id=user_id, session_id=session_id):
        main_logger.info("Начинаем обработку")
        # ... код обработки ...
        main_logger.info("Обработка завершена")
```

### 3. Frontend трекинг

```javascript
// Отслеживание клика кнопки
document.getElementById('startButton').addEventListener('click', () => {
    window.roulettTracker.trackButtonClick({
        button: 'start',
        page: 'game'
    });
});

// Отслеживание отправки формы
document.getElementById('loginForm').addEventListener('submit', (e) => {
    window.roulettTracker.trackFormSubmit({
        form: 'login',
        fields: ['username', 'password']
    });
});

// Кастомное событие
window.roulettTracker.trackCustomEvent('game_started', {
    game_id: 123,
    bet_amount: 100
});
```

## 🗂️ Структура логов

### Файлы логов

```
logs/
├── rulettt_2025-01-15.log          # Основные логи
├── rulettt_2025-01-15_errors.log   # Только ошибки
├── rulettt.api_2025-01-15.log      # API логи
├── rulettt.collector_2025-01-15.log # Collector логи
└── backup/                          # Резервные копии
```

### Формат лога (JSON)

```json
{
    "timestamp": "2025-01-15 15:30:45",
    "level": "ERROR",
    "module": "api_server",
    "function": "add_spin",
    "line": 123,
    "message": "❌ Ошибка сохранения спина",
    "user_id": "user123",
    "session_id": "session456",
    "exception": {
        "type": "ValueError",
        "message": "Invalid number",
        "traceback": ["...", "..."]
    }
}
```

### БД ошибок (errors.db)

```sql
-- Таблица errors
CREATE TABLE errors (
    id INTEGER PRIMARY KEY,
    error_hash TEXT,           -- MD5 для группировки
    timestamp DATETIME,
    level TEXT,
    error_type TEXT,
    error_message TEXT,
    module TEXT,
    function TEXT,
    line_number INTEGER,
    stack_trace TEXT,
    context TEXT,              -- JSON контекст
    user_actions TEXT,         -- JSON последние действия
    user_id TEXT,
    session_id TEXT,
    request_id TEXT,
    resolved BOOLEAN DEFAULT 0,
    resolution_notes TEXT,
    occurrences INTEGER DEFAULT 1,
    first_seen DATETIME,
    last_seen DATETIME
);
```

## 🔔 Система алертов (готовится)

Планируемые функции:

- ✅ Email уведомления (SMTP)
- ✅ Telegram бот для критических ошибок
- ✅ Webhook интеграция (Slack, Discord)
- ✅ Правила алертов (частота, уровень, модуль)
- ✅ Дневные отчёты

## 📊 Метрики

Отслеживаются автоматически:

- **Performance**:
  - Время загрузки страницы
  - Время выполнения функций
  - Медленные запросы (>1s)
  - Long tasks (>50ms)

- **Ошибки**:
  - Общее количество
  - Нерешённые
  - За последние 24 часа
  - Топ модулей с ошибками
  - Топ типов ошибок

- **Действия пользователя**:
  - Клики (элемент, координаты)
  - Навигация (URL, transitions)
  - Формы (отправки, поля)
  - Кастомные события

## 🐛 Troubleshooting

### Логи не создаются

```python
# Проверьте, что директория logs/ существует
import os
os.makedirs('logs', exist_ok=True)

# Проверьте права доступа
os.access('logs', os.W_OK)  # True = можно писать
```

### События не отправляются

```javascript
// Проверьте консоль браузера
console.log('Tracker:', window.roulettTracker);

// Проверьте очередь событий
console.log('Queue:', window.roulettTracker.eventQueue);

// Вручную отправьте события
window.roulettTracker.flush(true);
```

### БД ошибок не создаётся

```python
# Создайте директорию data/
import os
os.makedirs('data', exist_ok=True)

# Проверьте создание БД
from src.error_tracker import error_db
print(f"БД находится в: {error_db.db_path}")
```

## 📖 Дополнительно

- См. `LOGGING_INTEGRATION_EXAMPLE.py` - примеры интеграции
- См. `src/logger.py` - документация API
- См. `src/error_tracker.py` - работа с ошибками
- См. `webapp/event-tracker.js` - frontend трекинг

## 🎯 Best Practices

1. **Используйте правильный уровень**:
   - DEBUG - только для разработки
   - INFO - нормальные события
   - WARNING - потенциальные проблемы
   - ERROR - ошибки выполнения
   - CRITICAL - система не работает

2. **Добавляйте контекст**:
   ```python
   logger.info("Пользователь вошёл", extra={
       'user_id': user_id,
       'ip': request.remote_addr
   })
   ```

3. **Используйте emoji** для быстрого визуального поиска:
   - ✅ SUCCESS
   - ❌ ERROR
   - ⚠️ WARNING
   - 🔵 INFO
   - 🐛 DEBUG

4. **Группируйте логи** по модулям:
   ```python
   api_logger.info("API запрос")
   collector_logger.info("Сбор данных")
   analyzer_logger.info("Анализ")
   ```

5. **Не логируйте чувствительные данные**:
   - Пароли
   - Токены
   - Персональные данные
   - API ключи

---

**Версия:** 1.0.0  
**Дата:** 15.01.2025  
**Автор:** RULETTT Team
