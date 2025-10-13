# 🖥️ RULETTT Desktop Application - Руководство

## 📋 Обзор

**RULETTT Desktop** - полноценное Windows приложение с графическим интерфейсом для сбора и анализа данных рулетки.

### ✨ Возможности

- ✅ **Графический интерфейс** - удобное управление всеми функциями
- ✅ **Автозапуск серверов** - API и Web сервер запускаются автоматически
- ✅ **Иконка в трее** - приложение работает в фоне
- ✅ **Быстрый доступ** - одна кнопка для Dashboard, логов, CLI
- ✅ **Мониторинг** - отслеживание статуса серверов в реальном времени
- ✅ **Логирование** - все операции записываются в журнал
- ✅ **Standalone** - работает без установки Python (после сборки)

---

## 🚀 Быстрый старт

### Вариант 1: Запуск из исходников (для разработки)

```powershell
# 1. Установите зависимости
pip install -r requirements_desktop.txt

# 2. Запустите приложение
python rulettt_desktop.py

# ИЛИ используйте батник
run_desktop.bat
```

### Вариант 2: Standalone .exe (для пользователей)

```powershell
# 1. Соберите приложение
build_desktop.bat

# 2. Запустите
dist\RULETTT\RULETTT.exe
```

---

## 📦 Сборка приложения

### Шаг 1: Подготовка

Убедитесь что установлено:
- Python 3.8+ ✅
- PyQt5 ✅
- PyInstaller ✅

```powershell
pip install -r requirements_desktop.txt
```

### Шаг 2: Сборка .exe

```powershell
# Автоматическая сборка
build_desktop.bat
```

Или вручную:
```powershell
pyinstaller --clean rulettt_desktop.spec
```

**Результат:** `dist\RULETTT\RULETTT.exe` (готовое приложение)

### Шаг 3: Создание инсталлятора (опционально)

Требует [Inno Setup](https://jrsoftware.org/isdl.php):

1. Установите Inno Setup
2. Откройте `installer_script.iss`
3. Compile → Run

**Результат:** `installer\RULETTT_Setup_v1.0.0.exe`

---

## 🎯 Использование приложения

### Главное окно

После запуска вы увидите:

```
┌─────────────────────────────────────────┐
│  🎰 RULETTT - Анализ данных рулетки    │
├─────────────────────────────────────────┤
│  [Управление] [Логи] [О программе]      │
│                                         │
│  ┌── Статус серверов ──────────────┐   │
│  │ API Server: 🟢 Работает          │   │
│  │ Web Server: 🟢 Работает          │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌── Управление серверами ─────────┐   │
│  │ [🚀 Запустить всё]               │   │
│  │ [⏹️ Остановить всё]              │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌── Быстрый доступ ───────────────┐   │
│  │ [🌐 Открыть Dashboard]           │   │
│  │ [📊 Открыть Logs Dashboard]      │   │
│  │ [🐍 Запустить Python CLI]        │   │
│  │ [📋 Открыть коллектор (JS)]      │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌── Документация ──────────────────┐   │
│  │ [📖 Как собрать реальные данные] │   │
│  │ [📝 Шпаргалка]                   │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Вкладка "Логи"

Все операции приложения записываются в журнал:

```
[14:30:15] 🚀 Автозапуск серверов...
[14:30:15] ▶️ Запуск серверов...
[14:30:16] API: API сервер запущен на порту 5000
[14:30:16] Web: Web сервер запущен на порту 8080
[14:30:20] 🌐 Открыт Dashboard: http://localhost:8080/dashboard.html
```

### Иконка в трее

При сворачивании приложение уходит в системный трей (возле часов).

**Правый клик** → показывает меню:
- Показать
- Открыть Dashboard
- Выход

**Двойной клик** → разворачивает окно

---

## ⚙️ Конфигурация

### Порты серверов

По умолчанию:
- API Server: `5000`
- Web Server: `8080`

Изменить можно в `rulettt_desktop.py`:
```python
self.api_port = 5000  # Ваш порт
self.web_port = 8080  # Ваш порт
```

### Автозапуск при входе в Windows

**Вариант 1: Через инсталлятор**
- При установке выберите опцию "Запускать при входе в систему"

**Вариант 2: Вручную**
1. Создайте ярлык на `RULETTT.exe`
2. Скопируйте его в: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

**Вариант 3: Планировщик задач**
```powershell
# Откройте Планировщик задач
taskschd.msc

# Создайте задачу:
# Триггер: При входе в систему
# Действие: Запуск программы → RULETTT.exe
```

---

## 🔧 Устранение неполадок

### ❌ "PyQt5 не установлен"

```powershell
pip install PyQt5 PyQtWebEngine
```

### ❌ "Порт уже занят"

Проверьте что порты 5000 и 8080 свободны:
```powershell
netstat -an | findstr ":5000"
netstat -an | findstr ":8080"
```

Завершите процессы:
```powershell
# Найдите PID
netstat -ano | findstr ":5000"

# Завершите процесс
taskkill /PID <номер> /F
```

### ❌ Ошибка сборки PyInstaller

1. Очистите кэш:
```powershell
rmdir /s /q build dist __pycache__
```

2. Пересоберите:
```powershell
pyinstaller --clean rulettt_desktop.spec
```

3. Проверьте логи в `build\RULETTT\`

### ❌ Приложение не запускается

1. Запустите с консолью (для отладки):
```powershell
# В rulettt_desktop.spec измените:
console=True  # Было: False
```

2. Проверьте наличие всех файлов:
```
dist\RULETTT\
├── RULETTT.exe
├── webapp\
├── src\
├── data\
└── *.md файлы
```

---

## 📁 Структура проекта

```
RULETTT/
├── rulettt_desktop.py          # Главный файл приложения
├── rulettt_desktop.spec        # Конфигурация PyInstaller
├── build_desktop.bat           # Скрипт сборки
├── run_desktop.bat             # Быстрый запуск
├── installer_script.iss        # Inno Setup скрипт
├── requirements_desktop.txt    # Зависимости desktop
├── LICENSE.txt                 # Лицензия
│
├── dist/                       # Собранное приложение
│   └── RULETTT/
│       ├── RULETTT.exe        # Готовый .exe
│       └── ...                # Зависимости
│
└── installer/                  # Инсталлятор
    └── RULETTT_Setup_v1.0.0.exe
```

---

## 🎨 Кастомизация

### Изменение иконки

1. Создайте файл `icon.ico` (256x256 или 128x128)
2. Поместите в корень проекта
3. Пересоберите: `build_desktop.bat`

### Изменение стилей

В `rulettt_desktop.py` метод `apply_styles()`:
```python
def apply_styles(self):
    self.setStyleSheet("""
        QPushButton {
            background-color: #0078d4;  /* Ваш цвет */
            /* ... */
        }
    """)
```

### Добавление функций

Добавьте методы в класс `RoulettDesktopApp`:
```python
def my_new_function(self):
    """Новая функция"""
    self.log("Выполнение новой функции")
    # Ваш код
```

Добавьте кнопку:
```python
btn_new = QPushButton("🆕 Новая функция")
btn_new.clicked.connect(self.my_new_function)
layout.addWidget(btn_new)
```

---

## 📊 Системные требования

### Минимальные:
- Windows 7/8/10/11 (64-bit)
- 2 GB RAM
- 200 MB свободного места
- Python 3.8+ (для запуска из исходников)

### Рекомендуемые:
- Windows 10/11 (64-bit)
- 4 GB RAM
- 500 MB свободного места

---

## 🔄 Обновление приложения

### Из исходников:
```powershell
git pull origin main
pip install -r requirements_desktop.txt --upgrade
python rulettt_desktop.py
```

### Standalone:
1. Скачайте новую версию
2. Удалите старую папку `RULETTT`
3. Распакуйте новую
4. Запустите `RULETTT.exe`

---

## 🍎 macOS версия (в разработке)

Планируется:
- ✅ Нативный .app bundle
- ✅ DMG инсталлятор
- ✅ Menu bar integration
- ✅ Retina display support

**Статус:** В разработке (следующий этап)

---

## 📞 Поддержка

### Документация
- `REAL_DATA_START.md` - Сбор реальных данных
- `CHEATSHEET.md` - Быстрая шпаргалка
- `README.md` - Общая информация

### Помощь
- GitHub Issues: https://github.com/nikolaspablo92-prog/RULETTT/issues
- Email: support@rulettt.project

---

## 📝 Changelog

### v1.0.0 (13 октября 2025)
- ✨ Первый релиз desktop приложения
- ✅ GUI интерфейс с PyQt5
- ✅ Автозапуск серверов
- ✅ Иконка в системном трее
- ✅ Мониторинг статуса
- ✅ Быстрый доступ к функциям
- ✅ Логирование операций
- ✅ PyInstaller сборка

---

**🎰 RULETTT Desktop v1.0.0**  
**© 2025 RULETTT Project**
