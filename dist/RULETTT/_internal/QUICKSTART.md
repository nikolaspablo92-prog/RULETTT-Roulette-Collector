# 🚀 RULETTT - Быстрый старт системы логирования

## ⚡ За 3 минуты

### 1. Запустите сервисы (2 минуты)

```powershell
# Терминал 1: API сервер
python api_server.py

# Терминал 2: Веб-сервер
python -m http.server 8080 --directory webapp
```

### 2. Откройте dashboard (30 секунд)

```
http://localhost:8080/logs_dashboard.html
```

### 3. Тестируйте систему (30 секунд)

```powershell
# Запустите тестовый пример
python LOGGING_INTEGRATION_EXAMPLE.py
```

**Готово!** 🎉 Откройте dashboard и увидите логи в реальном времени.

---

## 📊 Что вы получили

### ✅ Backend логирование
- Автоматическая ротация файлов (10MB)
- 6 специализированных логгеров
- Отслеживание ошибок в SQLite БД
- История действий пользователя (50 последних)

### ✅ Frontend мониторинг
- Автотрекинг всех кликов
- Отслеживание JS ошибок
- Performance метрики
- Network requests

### ✅ Dashboard
- 4 вкладки: Логи, Ошибки, События, Статистика
- Фильтры и поиск
- Автообновление каждые 10 секунд

### ✅ API
- 8 новых endpoints для логов и ошибок
- Статистика в реальном времени
- Экспорт данных

---

## 🎯 Первые шаги

### 1. Интегрируйте в свой код

```python
# В любом Python файле:
from src.logger import main_logger, log_execution_time
from src.error_tracker import track_exception_decorator

@log_execution_time(main_logger)
@track_exception_decorator
def my_function():
    main_logger.info("✅ Функция работает!")
    return "result"
```

### 2. Добавьте в HTML

```html
<!-- Перед </body>: -->
<script src="event-tracker.js"></script>
```

### 3. Смотрите результаты

Откройте `http://localhost:8080/logs_dashboard.html`

---

## 📚 Документация

- **LOGGING_GUIDE.md** - Полное руководство (500+ строк)
- **LOGGING_INTEGRATION_EXAMPLE.py** - Примеры кода
- **LOGGING_SYSTEM_REPORT.md** - Отчёт о реализации

---

## 🆘 Проблемы?

### Логи не создаются?
```python
import os
os.makedirs('logs', exist_ok=True)
```

### Dashboard не работает?
Проверьте, что оба сервиса запущены:
- API: http://localhost:5000/api/health
- Web: http://localhost:8080

### События не отправляются?
Откройте консоль браузера (F12):
```javascript
console.log(window.roulettTracker);
window.roulettTracker.flush(true);
```

---

## 🎓 Что дальше?

1. **Изучите примеры:** `LOGGING_INTEGRATION_EXAMPLE.py`
2. **Прочитайте гайд:** `LOGGING_GUIDE.md`
3. **Интегрируйте в модули:** добавьте импорты в свои файлы
4. **Настройте алерты:** создайте систему уведомлений

---

**Версия:** 1.0.0  
**Статус:** Production Ready ✅  
**Создано:** 15.01.2025
