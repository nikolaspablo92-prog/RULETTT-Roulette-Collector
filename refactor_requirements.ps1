# 🔧 Скрипт 2: Разделение requirements
# refactor_requirements.ps1

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔧 РЕФАКТОРИНГ: Разделение requirements" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Шаг 1: requirements-core.txt (ОБЯЗАТЕЛЬНЫЕ)
Write-Host "📦 Создание requirements-core.txt..." -ForegroundColor Yellow

$coreReqs = @"
# ═══════════════════════════════════════════════════════════
# RULETTT - Основные зависимости (ОБЯЗАТЕЛЬНЫЕ)
# ═══════════════════════════════════════════════════════════
# Установка: pip install -r requirements-core.txt
#
# Минимальные зависимости для работы системы анализа

# Веб-сервер и API
flask==3.0.0
flask-cors==4.0.0

# Конфигурация
python-dotenv==1.0.0

# Аутентификация
pyjwt==2.8.0
bcrypt==4.0.1

# Планировщик задач
apscheduler==3.10.4

# Работа с JSON/данными (стандартные библиотеки)
# sqlite3 - встроенная
# json - встроенная
# datetime - встроенная
"@

$coreReqs | Out-File -FilePath "requirements-core.txt" -Encoding UTF8 -Force
Write-Host "   ✅ requirements-core.txt создан" -ForegroundColor Green

# Шаг 2: requirements-optional.txt (ОПЦИОНАЛЬНЫЕ)
Write-Host ""
Write-Host "🎨 Создание requirements-optional.txt..." -ForegroundColor Yellow

$optionalReqs = @"
# ═══════════════════════════════════════════════════════════
# RULETTT - Опциональные зависимости
# ═══════════════════════════════════════════════════════════
# Установка: pip install -r requirements-optional.txt
#
# Эти зависимости НЕ обязательны. Система работает без них,
# но некоторые функции будут недоступны.

# ─────────────────────────────────────────────────────────────
# АВТОМАТИЧЕСКИЙ СБОР (для paddypower_auto_collector.py)
# ─────────────────────────────────────────────────────────────
pyppeteer==1.0.2
playwright==1.40.0
selenium==4.15.0

# ─────────────────────────────────────────────────────────────
# AI АНАЛИЗ (для ai_assistant.py)
# ─────────────────────────────────────────────────────────────
numpy==1.24.0
pandas==2.0.0

# ─────────────────────────────────────────────────────────────
# ВИЗУАЛИЗАЦИЯ (для графиков и отчетов)
# ─────────────────────────────────────────────────────────────
matplotlib==3.7.0
seaborn==0.12.0

# ─────────────────────────────────────────────────────────────
# МАШИННОЕ ОБУЧЕНИЕ (для продвинутого AI)
# ─────────────────────────────────────────────────────────────
scikit-learn==1.3.0

# ─────────────────────────────────────────────────────────────
# ЭКСПОРТ ДАННЫХ (для Excel/CSV)
# ─────────────────────────────────────────────────────────────
openpyxl==3.1.2
xlsxwriter==3.1.9

# ─────────────────────────────────────────────────────────────
# ОБЛАЧНАЯ СИНХРОНИЗАЦИЯ
# ─────────────────────────────────────────────────────────────
firebase-admin==6.2.0
requests==2.31.0
aiohttp==3.9.0
"@

$optionalReqs | Out-File -FilePath "requirements-optional.txt" -Encoding UTF8 -Force
Write-Host "   ✅ requirements-optional.txt создан" -ForegroundColor Green

# Шаг 3: requirements-dev.txt (РАЗРАБОТКА)
Write-Host ""
Write-Host "🛠️  Создание requirements-dev.txt..." -ForegroundColor Yellow

$devReqs = @"
# ═══════════════════════════════════════════════════════════
# RULETTT - Зависимости для разработки
# ═══════════════════════════════════════════════════════════
# Установка: pip install -r requirements-dev.txt
#
# Эти зависимости нужны ТОЛЬКО разработчикам

# ─────────────────────────────────────────────────────────────
# ТЕСТИРОВАНИЕ
# ─────────────────────────────────────────────────────────────
pytest==7.4.0
pytest-cov==4.1.0
pytest-asyncio==0.21.1
pytest-mock==3.12.0

# ─────────────────────────────────────────────────────────────
# КАЧЕСТВО КОДА
# ─────────────────────────────────────────────────────────────
black==23.7.0
flake8==6.1.0
pylint==3.0.0
isort==5.12.0

# ─────────────────────────────────────────────────────────────
# ТИПИЗАЦИЯ
# ─────────────────────────────────────────────────────────────
mypy==1.5.0
types-requests==2.31.0
types-python-dotenv==1.0.0

# ─────────────────────────────────────────────────────────────
# ДОКУМЕНТАЦИЯ
# ─────────────────────────────────────────────────────────────
sphinx==7.2.0
sphinx-rtd-theme==1.3.0

# ─────────────────────────────────────────────────────────────
# ПРОФИЛИРОВАНИЕ
# ─────────────────────────────────────────────────────────────
memory-profiler==0.61.0
py-spy==0.3.14

# ─────────────────────────────────────────────────────────────
# АВТОМАТИЗАЦИЯ
# ─────────────────────────────────────────────────────────────
pre-commit==3.5.0
tox==4.11.0
"@

$devReqs | Out-File -FilePath "requirements-dev.txt" -Encoding UTF8 -Force
Write-Host "   ✅ requirements-dev.txt создан" -ForegroundColor Green

# Шаг 4: Обновить requirements.txt
Write-Host ""
Write-Host "📝 Обновление requirements.txt..." -ForegroundColor Yellow

$mainReqs = @"
# ═══════════════════════════════════════════════════════════
# RULETTT - Зависимости проекта
# ═══════════════════════════════════════════════════════════
# Это главный файл зависимостей. Он включает:
# - requirements-core.txt (обязательные)
# - requirements-optional.txt (опциональные)
#
# УСТАНОВКА:
# 1. Минимальная (только core):
#    pip install -r requirements-core.txt
#
# 2. Полная (core + optional):
#    pip install -r requirements.txt
#
# 3. Для разработки (core + optional + dev):
#    pip install -r requirements.txt
#    pip install -r requirements-dev.txt

# ─────────────────────────────────────────────────────────────
# ОСНОВНЫЕ (ОБЯЗАТЕЛЬНЫЕ)
# ─────────────────────────────────────────────────────────────
-r requirements-core.txt

# ─────────────────────────────────────────────────────────────
# ОПЦИОНАЛЬНЫЕ (рекомендуются для полной функциональности)
# ─────────────────────────────────────────────────────────────
-r requirements-optional.txt
"@

$mainReqs | Out-File -FilePath "requirements.txt" -Encoding UTF8 -Force
Write-Host "   ✅ requirements.txt обновлен" -ForegroundColor Green

# Шаг 5: Создать setup.py
Write-Host ""
Write-Host "🚀 Создание setup.py..." -ForegroundColor Yellow

$setupPy = @"
# setup.py
"""
RULETTT - Система сбора и анализа данных рулетки
"""

from setuptools import setup, find_packages
from pathlib import Path

# Читаем README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Читаем зависимости
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f 
                if line.strip() and not line.startswith('#') and not line.startswith('-r')]

setup(
    name="rulettt",
    version="2.0.0",
    author="RULETTT Team",
    author_email="support@rulettt.dev",
    description="Система сбора и анализа данных европейской рулетки",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikolaspablo92-prog/RULETTT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements-core.txt"),
    extras_require={
        "full": read_requirements("requirements-optional.txt"),
        "auto": [
            "pyppeteer>=1.0.2",
            "playwright>=1.40.0",
        ],
        "ai": [
            "numpy>=1.24.0",
            "pandas>=2.0.0",
            "scikit-learn>=1.3.0",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
        ],
        "dev": read_requirements("requirements-dev.txt"),
    },
    entry_points={
        "console_scripts": [
            "rulettt=main:main",
            "rulettt-single=main_single_table:main",
            "rulettt-test=test_system:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.js", "*.json", "*.txt", "*.md"],
    },
)
"@

$setupPy | Out-File -FilePath "setup.py" -Encoding UTF8 -Force
Write-Host "   ✅ setup.py создан" -ForegroundColor Green

# Итоги
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ РЕФАКТОРИНГ ЗАВЕРШЕН!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Созданы файлы:" -ForegroundColor Yellow
Write-Host "   ✅ requirements-core.txt (обязательные)" -ForegroundColor Green
Write-Host "   ✅ requirements-optional.txt (опциональные)" -ForegroundColor Green
Write-Host "   ✅ requirements-dev.txt (для разработки)" -ForegroundColor Green
Write-Host "   ✅ requirements.txt (обновлен)" -ForegroundColor Green
Write-Host "   ✅ setup.py (установка пакета)" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Следующие шаги:" -ForegroundColor Yellow
Write-Host "   1. Минимальная установка:" -ForegroundColor White
Write-Host "      pip install -r requirements-core.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Полная установка:" -ForegroundColor White
Write-Host "      pip install -r requirements.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Для разработки:" -ForegroundColor White
Write-Host "      pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "      pip install -r requirements-dev.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "   4. Установка как пакет:" -ForegroundColor White
Write-Host "      pip install -e .[full]" -ForegroundColor Gray
Write-Host ""
