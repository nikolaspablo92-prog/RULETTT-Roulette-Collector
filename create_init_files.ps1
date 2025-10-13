# 📦 Скрипт 4: Создание __init__.py для src/
# create_init_files.ps1

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📦 СОЗДАНИЕ __init__.py ДЛЯ src/" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Шаг 1: Проверка существования src/
Write-Host "🔍 Проверка наличия папки src/..." -ForegroundColor Yellow

$srcPath = "src"

if (-Not (Test-Path $srcPath)) {
    Write-Host "   ❌ Папка src/ не найдена!" -ForegroundColor Red
    exit 1
}

Write-Host "   ✅ Папка src/ найдена" -ForegroundColor Green

# Шаг 2: Анализ модулей в src/
Write-Host ""
Write-Host "📊 Анализ модулей в src/..." -ForegroundColor Yellow

$modules = Get-ChildItem -Path $srcPath -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" }
$moduleCount = $modules.Count

Write-Host "   📄 Найдено модулей: $moduleCount" -ForegroundColor White

foreach ($module in $modules) {
    Write-Host "      - $($module.Name)" -ForegroundColor Gray
}

# Шаг 3: Создать src/__init__.py
Write-Host ""
Write-Host "📝 Создание src/__init__.py..." -ForegroundColor Yellow

$initContent = @"
"""
RULETTT - Система сбора и анализа данных европейской рулетки

Основные модули:
- utils: Утилиты для работы с рулеткой (RouletteUtils)
- data_collector: Сбор и хранение данных (DataCollector)
- game_analyzer: Анализ стратегий (GameAnalyzer, GameStrategy, PredefinedStrategies)
- ai_assistant: AI-помощник (AIAssistant)
- user_strategies: Пользовательские стратегии
- bot_simulator: Симулятор бота (BotSimulator)
- auth_manager: Управление аутентификацией (AuthManager)
- paddypower_auto_collector: Автосбор с PaddyPower (PaddyPowerCollector, AntiDetectBrowser)

Примеры использования:

    # Базовое использование
    from src.utils import RouletteUtils
    from src.data_collector import DataCollector
    
    collector = DataCollector()
    color = RouletteUtils.get_color(17)  # "black"
    
    # Анализ стратегий
    from src.game_analyzer import PredefinedStrategies
    
    strategy = PredefinedStrategies.martingale_red()
    result = strategy.analyze_session(collector)
    
    # AI анализ
    from src.ai_assistant import AIAssistant
    
    ai = AIAssistant(collector)
    patterns = ai.find_hot_cold_numbers()

Версия: 2.0.0
Лицензия: MIT
Автор: RULETTT Team
"""

__version__ = "2.0.0"
__author__ = "RULETTT Team"
__license__ = "MIT"

# Импорты основных классов
try:
    from .utils import RouletteUtils
except ImportError:
    RouletteUtils = None

try:
    from .data_collector import DataCollector
except ImportError:
    DataCollector = None

try:
    from .game_analyzer import GameAnalyzer, GameStrategy, PredefinedStrategies
except ImportError:
    GameAnalyzer = None
    GameStrategy = None
    PredefinedStrategies = None

try:
    from .ai_assistant import AIAssistant
except ImportError:
    AIAssistant = None

try:
    from .bot_simulator import BotSimulator
except ImportError:
    BotSimulator = None

try:
    from .auth_manager import AuthManager
except ImportError:
    AuthManager = None

try:
    from .paddypower_auto_collector import PaddyPowerCollector, AntiDetectBrowser
except ImportError:
    PaddyPowerCollector = None
    AntiDetectBrowser = None

# Экспортируемые символы
__all__ = [
    # Версия и метаданные
    "__version__",
    "__author__",
    "__license__",
    
    # Основные классы
    "RouletteUtils",
    "DataCollector",
    "GameAnalyzer",
    "GameStrategy",
    "PredefinedStrategies",
    "AIAssistant",
    "BotSimulator",
    "AuthManager",
    "PaddyPowerCollector",
    "AntiDetectBrowser",
]

# Проверка доступности модулей
def get_available_modules():
    """Возвращает список доступных модулей"""
    available = []
    for module_name in __all__:
        if module_name.startswith("__"):
            continue
        module = globals().get(module_name)
        if module is not None:
            available.append(module_name)
    return available

def check_dependencies():
    """Проверяет наличие всех зависимостей и выводит отчет"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📦 RULETTT - Проверка зависимостей")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    # Основные модули
    print("🔧 Основные модули:")
    core_modules = [
        ("RouletteUtils", RouletteUtils),
        ("DataCollector", DataCollector),
        ("GameAnalyzer", GameAnalyzer),
        ("GameStrategy", GameStrategy),
        ("PredefinedStrategies", PredefinedStrategies),
    ]
    
    for name, module in core_modules:
        status = "✅" if module is not None else "❌"
        print(f"   {status} {name}")
    
    print()
    print("🤖 Опциональные модули:")
    optional_modules = [
        ("AIAssistant", AIAssistant),
        ("BotSimulator", BotSimulator),
        ("AuthManager", AuthManager),
        ("PaddyPowerCollector", PaddyPowerCollector),
        ("AntiDetectBrowser", AntiDetectBrowser),
    ]
    
    for name, module in optional_modules:
        status = "✅" if module is not None else "⚠️ "
        print(f"   {status} {name}")
    
    print()
    
    # Проверка внешних зависимостей
    print("📚 Внешние библиотеки:")
    
    dependencies = [
        ("numpy", "AI анализ"),
        ("pandas", "Обработка данных"),
        ("matplotlib", "Визуализация"),
        ("pyppeteer", "Автосбор данных"),
        ("flask", "API сервер"),
    ]
    
    for lib_name, description in dependencies:
        try:
            __import__(lib_name)
            print(f"   ✅ {lib_name:15} - {description}")
        except ImportError:
            print(f"   ⚠️  {lib_name:15} - {description} (не установлена)")
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Автоматическая проверка при импорте (если запущено напрямую)
if __name__ == "__main__":
    check_dependencies()
"@

$initPath = Join-Path $srcPath "__init__.py"
$initContent | Out-File -FilePath $initPath -Encoding UTF8 -Force

Write-Host "   ✅ src/__init__.py создан" -ForegroundColor Green

# Шаг 4: Создать webapp/__init__.py
Write-Host ""
Write-Host "📝 Создание webapp/__init__.py..." -ForegroundColor Yellow

$webappPath = "webapp"

if (Test-Path $webappPath) {
    $webappInitContent = @"
"""
RULETTT - Веб-интерфейс

Содержит HTML/CSS/JS файлы для:
- Дашборда (dashboard.html)
- Мобильной версии (mobile.html)
- Продвинутой аналитики (advanced_analytics.html)
- Глобального чата (global_chat.html)
- AI чата (ai_chat_test.html, copilot_chat.html)
- Коммуникации (communication.html)

Для запуска:
    python -m http.server 8080 --directory webapp
    
Или используйте Flask API (api_server.py), который уже настроен
на обслуживание этих файлов.
"""

__version__ = "2.0.0"
"@
    
    $webappInitPath = Join-Path $webappPath "__init__.py"
    $webappInitContent | Out-File -FilePath $webappInitPath -Encoding UTF8 -Force
    
    Write-Host "   ✅ webapp/__init__.py создан" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  webapp/ не найдена, пропускаем" -ForegroundColor Yellow
}

# Шаг 5: Создать docs/__init__.py
Write-Host ""
Write-Host "📝 Создание docs/__init__.py..." -ForegroundColor Yellow

$docsPath = "docs"

if (Test-Path $docsPath) {
    $docsInitContent = @"
"""
RULETTT - Документация

Содержит документацию проекта:
- explanation.md: Подробное объяснение всех модулей
- PROJECT_AUDIT_REPORT.md: Полный аудит проекта
- verified_apis.md: Документация API казино
- И другие документы

Для просмотра документации рекомендуется использовать
Markdown-редактор или VS Code с расширением Markdown Preview.
"""

__version__ = "2.0.0"
"@
    
    $docsInitPath = Join-Path $docsPath "__init__.py"
    $docsInitContent | Out-File -FilePath $docsInitPath -Encoding UTF8 -Force
    
    Write-Host "   ✅ docs/__init__.py создан" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  docs/ не найдена, пропускаем" -ForegroundColor Yellow
}

# Шаг 6: Обновить .gitignore
Write-Host ""
Write-Host "🔒 Обновление .gitignore..." -ForegroundColor Yellow

$gitignorePath = ".gitignore"

# Читаем существующий .gitignore
$existingGitignore = ""
if (Test-Path $gitignorePath) {
    $existingGitignore = Get-Content $gitignorePath -Raw
}

# Добавляем новые правила, если их еще нет
$newRules = @"

# ═══════════════════════════════════════════════════════════
# Python кэш и временные файлы
# ═══════════════════════════════════════════════════════════
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# ═══════════════════════════════════════════════════════════
# Виртуальные окружения
# ═══════════════════════════════════════════════════════════
venv/
ENV/
env/
.venv

# ═══════════════════════════════════════════════════════════
# IDE
# ═══════════════════════════════════════════════════════════
.vscode/
.idea/
*.swp
*.swo
*~

# ═══════════════════════════════════════════════════════════
# Базы данных (кроме примеров)
# ═══════════════════════════════════════════════════════════
data/*.db
!data/example.db

# ═══════════════════════════════════════════════════════════
# Логи
# ═══════════════════════════════════════════════════════════
*.log
logs/

# ═══════════════════════════════════════════════════════════
# Конфигурация (может содержать секреты)
# ═══════════════════════════════════════════════════════════
.env
config.local.py
secrets.json

# ═══════════════════════════════════════════════════════════
# Архивы (слишком большие для Git)
# ═══════════════════════════════════════════════════════════
archives/*.zip
archives/*.tar.gz
archives/*.7z

# ═══════════════════════════════════════════════════════════
# Тестирование
# ═══════════════════════════════════════════════════════════
.pytest_cache/
.coverage
htmlcov/
.tox/

# ═══════════════════════════════════════════════════════════
# OS
# ═══════════════════════════════════════════════════════════
.DS_Store
Thumbs.db
"@

if (-Not $existingGitignore.Contains("__pycache__")) {
    $existingGitignore + $newRules | Out-File -FilePath $gitignorePath -Encoding UTF8 -Force
    Write-Host "   ✅ .gitignore обновлен" -ForegroundColor Green
} else {
    Write-Host "   ✅ .gitignore уже содержит нужные правила" -ForegroundColor Green
}

# Шаг 7: Создать MANIFEST.in
Write-Host ""
Write-Host "📝 Создание MANIFEST.in..." -ForegroundColor Yellow

$manifestContent = @"
# Включить документацию
include README.md
include LICENSE
include CHANGELOG.md
recursive-include docs *.md *.txt

# Включить конфигурационные файлы
include requirements*.txt
include setup.py
include pytest.ini

# Включить JavaScript коллекторы
include *.js
recursive-include webapp *.html *.css *.js *.json

# Исключить ненужное
global-exclude __pycache__
global-exclude *.py[co]
global-exclude .DS_Store
prune tests
prune archives
"@

$manifestContent | Out-File -FilePath "MANIFEST.in" -Encoding UTF8 -Force
Write-Host "   ✅ MANIFEST.in создан" -ForegroundColor Green

# Итоги
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ СОЗДАНИЕ __init__.py ЗАВЕРШЕНО!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Созданы файлы:" -ForegroundColor Yellow
Write-Host "   ✅ src/__init__.py" -ForegroundColor Green
Write-Host "   ✅ webapp/__init__.py" -ForegroundColor Green
Write-Host "   ✅ docs/__init__.py" -ForegroundColor Green
Write-Host "   ✅ .gitignore (обновлен)" -ForegroundColor Green
Write-Host "   ✅ MANIFEST.in" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Следующие шаги:" -ForegroundColor Yellow
Write-Host "   1. Проверить импорты:" -ForegroundColor White
Write-Host "      python -c `"from src import RouletteUtils; print(RouletteUtils)`"" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Проверить зависимости:" -ForegroundColor White
Write-Host "      python -m src" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Установить как пакет:" -ForegroundColor White
Write-Host "      pip install -e ." -ForegroundColor Gray
Write-Host ""
Write-Host "   4. Запустить тесты:" -ForegroundColor White
Write-Host "      pytest tests/" -ForegroundColor Gray
Write-Host ""
