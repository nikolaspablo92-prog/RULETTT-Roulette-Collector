# 🎯 RULETTT - Шпаргалка по использованию

## 🚀 Быстрый старт (3 команды)

```powershell
# 1. Запустить систему
START_RULETTT.bat

# 2. Открыть Dashboard
start http://localhost:8080/dashboard.html

# 3. Открыть мониторинг логов
start http://localhost:8080/logs_dashboard.html
```

---

## 📊 Основные URL

| Что | URL | Описание |
|-----|-----|----------|
| **Главный Dashboard** | http://localhost:8080/dashboard.html | Статистика рулетки |
| **Логи Dashboard** | http://localhost:8080/logs_dashboard.html | Мониторинг системы |
| **API Health** | http://localhost:5000/api/health | Проверка API |
| **API Статистика** | http://localhost:5000/api/statistics | JSON данные |
| **API Спины** | http://localhost:5000/api/spins | Список спинов |

---

## 🎰 Сбор данных рулетки

### Вариант 1: Browser Console (Рекомендуется)

1. Откройте сайт с рулеткой
2. Нажмите `F12` (консоль)
3. Скопируйте код из `auto_collector_console_code.js`
4. Вставьте в консоль
5. Данные собираются автоматически!

### Вариант 2: API запрос

```powershell
# PowerShell
curl -X POST http://localhost:5000/api/spins `
  -H "Content-Type: application/json" `
  -d '{"number": 17, "color": "black", "casino_name": "test"}'
```

```python
# Python
import requests
requests.post('http://localhost:5000/api/spins', 
    json={"number": 17, "color": "black", "casino_name": "test"})
```

### Вариант 3: Генератор тестовых данных

```powershell
py src/main.py
# → 1. Управление данными
# → 2. Генерация тестовых данных
```

---

## 🧪 Тестирование

```powershell
# Все тесты
py RUN_ALL_TESTS.py

# Быстрая проверка
py SMOKE_TEST.py

# Тест логирования
py test_logging.py

# Системный тест
py tests/test_system.py
```

---

## 📈 Анализ данных

### Через Dashboard
- Откройте: http://localhost:8080/dashboard.html
- Смотрите: графики, статистику, серии

### Через API
```powershell
# Статистика
curl http://localhost:5000/api/statistics

# Последние 100 спинов
curl http://localhost:5000/api/spins?limit=100

# Спины по казино
curl http://localhost:5000/api/spins?casino=pragmatic
```

### Через Python CLI
```powershell
py src/main.py
# → 1. Управление данными → 3. Просмотр статистики
```

---

## 🎯 Тестирование стратегий

```powershell
py src/main.py
# → 2. Анализ стратегий
# → Выберите стратегию:
#    • Мартингейл
#    • Фибоначчи
#    • Д'Аламбер
#    • Flat Bet
```

**Встроенные стратегии:**
- `martingale_red` - Удвоение на красное
- `fibonacci` - Последовательность Фибоначчи
- `dalembert` - Постепенное увеличение
- `flat_bet` - Фиксированная ставка

---

## 📝 Логирование

### Добавить логирование в свой код

```python
from src.logger import main_logger, log_execution_time
from src.error_tracker import track_exception_decorator

# Простое логирование
main_logger.info("✅ Операция выполнена")

# Автоматический замер времени
@log_execution_time(main_logger)
def my_function():
    return "result"

# Автоматическое отслеживание ошибок
@track_exception_decorator
def risky_operation():
    return 42 / 0
```

### Просмотр логов

```powershell
# В Dashboard
start http://localhost:8080/logs_dashboard.html

# В файлах
cat logs/rulettt_2025-10-13.log

# Через API
curl http://localhost:5000/api/logs?limit=50
```

---

## 🔍 Мониторинг ошибок

### Dashboard
http://localhost:8080/logs_dashboard.html
- Вкладка "Ошибки"
- Фильтры по типу
- Группировка одинаковых

### API
```powershell
# Нерешённые ошибки
curl http://localhost:5000/api/errors/unresolved

# Статистика
curl http://localhost:5000/api/logs/stats

# Пометить решённой
curl -X POST http://localhost:5000/api/errors/123/resolve `
  -H "Content-Type: application/json" `
  -d '{"notes": "Исправлено"}'
```

---

## 🗄️ Работа с базами данных

### Файлы БД
- `data/rulettt_cloud.db` - Основная БД
- `data/final_single_table.db` - Единая таблица
- `data/test_strategies.db` - Стратегии
- `data/errors.db` - Ошибки

### Просмотр данных

```powershell
# SQLite CLI
sqlite3 data/rulettt_cloud.db
> SELECT COUNT(*) FROM roulette_spins;
> SELECT * FROM roulette_spins LIMIT 10;
```

```python
# Python
import sqlite3
conn = sqlite3.connect('data/rulettt_cloud.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM roulette_spins LIMIT 10")
print(cursor.fetchall())
```

---

## 🛠️ Управление сервисами

### Запуск
```powershell
# Автозапуск
START_RULETTT.bat

# Ручной запуск
py api_server.py                    # Терминал 1
cd webapp && py -m http.server 8080  # Терминал 2

# VS Code Task
Ctrl+Shift+P → "Tasks: Run Task" → "🎲 Запустить все сервисы"
```

### Проверка статуса
```powershell
# Проверка портов
netstat -an | findstr ":5000"
netstat -an | findstr ":8080"

# Health check
curl http://localhost:5000/api/health
```

### Остановка
```powershell
# Закрыть окна терминалов
# Или Ctrl+C в каждом терминале
```

---

## 💡 Полезные советы

### 1. Автоматическая ротация логов
Файлы логов автоматически ротируются при достижении 10MB

### 2. Группировка ошибок
Одинаковые ошибки группируются по MD5 хэшу

### 3. Dashboard автообновление
Обновляется каждые 10 секунд автоматически

### 4. История действий
Сохраняются последние 50 действий перед ошибкой

### 5. Performance метрики
- Логирование: 126,000+ ops/sec
- API response: <100ms
- Dashboard load: <200ms

---

## 📚 Документация

| Файл | Описание |
|------|----------|
| **QUICKSTART.md** | Быстрый старт (5 мин) |
| **LOGGING_GUIDE.md** | Полное руководство по логированию |
| **TEST_REPORT.md** | Отчёт о тестировании |
| **LOGGING_INTEGRATION_EXAMPLE.py** | Примеры кода |
| **START_GUIDE.py** | Интерактивное руководство |

---

## 🆘 Troubleshooting

### API не работает
```powershell
# Проверить
curl http://localhost:5000/api/health

# Перезапустить
# Закрыть терминал с api_server.py
py api_server.py
```

### Dashboard не открывается
```powershell
# Проверить веб-сервер
curl http://localhost:8080

# Перезапустить
cd webapp
py -m http.server 8080
```

### Логи не создаются
```powershell
# Создать директорию
mkdir logs

# Проверить права
```

### БД не найдена
```powershell
# Создать директорию
mkdir data

# Проверить путь
ls data/*.db
```

---

## 🎓 Обучающие материалы

### Видео-туториалы (планируется)
- [ ] Запуск системы
- [ ] Сбор данных
- [ ] Анализ стратегий
- [ ] Создание своих стратегий

### Примеры кода
См. `LOGGING_INTEGRATION_EXAMPLE.py`

### API Reference
См. `LOGGING_GUIDE.md` → раздел "API Endpoints"

---

## 📞 Поддержка

- **GitHub:** https://github.com/nikolaspablo92-prog/RULETTT
- **Issues:** Создайте issue на GitHub
- **Документация:** См. файлы *.md

---

**Версия:** 1.0.0  
**Дата:** 13 октября 2025  
**Статус:** Production Ready ✅
