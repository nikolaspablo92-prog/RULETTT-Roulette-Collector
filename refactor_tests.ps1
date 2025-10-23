# 🔧 Скрипт 1: Организация тестов
# refactor_tests.ps1

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔧 РЕФАКТОРИНГ: Организация тестов" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Шаг 1: Создать папку tests
Write-Host "📁 Создание папки tests..." -ForegroundColor Yellow
if (!(Test-Path "tests")) {
    New-Item -ItemType Directory -Force -Path tests | Out-Null
    Write-Host "   ✅ Папка tests создана" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  Папка tests уже существует" -ForegroundColor Blue
}

# Шаг 2: Переместить тесты
Write-Host ""
Write-Host "📦 Перемещение test_*.py файлов..." -ForegroundColor Yellow

$testFiles = Get-ChildItem -Path . -Filter "test_*.py" -File
$movedCount = 0

foreach ($file in $testFiles) {
    try {
        Move-Item $file.FullName "tests\" -Force
        Write-Host "   ✅ $($file.Name)" -ForegroundColor Green
        $movedCount++
    } catch {
        Write-Host "   ❌ Ошибка перемещения $($file.Name): $_" -ForegroundColor Red
    }
}

if ($movedCount -eq 0) {
    Write-Host "   ℹ️  Нет файлов для перемещения" -ForegroundColor Blue
} else {
    Write-Host "   📊 Перемещено файлов: $movedCount" -ForegroundColor Green
}

# Шаг 3: Создать __init__.py
Write-Host ""
Write-Host "📝 Создание tests/__init__.py..." -ForegroundColor Yellow

$initContent = @"
# tests/__init__.py
"""
RULETTT Test Suite
==================

Тесты для всех модулей системы.
"""

__version__ = "2.0.0"
"@

try {
    $initContent | Out-File -FilePath "tests\__init__.py" -Encoding UTF8 -Force
    Write-Host "   ✅ tests/__init__.py создан" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Ошибка создания __init__.py: $_" -ForegroundColor Red
}

# Шаг 4: Создать pytest.ini
Write-Host ""
Write-Host "⚙️  Создание pytest.ini..." -ForegroundColor Yellow

$pytestConfig = @"
[pytest]
# Конфигурация pytest для RULETTT

# Где искать тесты
testpaths = tests

# Паттерны файлов
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Опции
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings

# Маркеры
markers =
    slow: медленные тесты
    integration: интеграционные тесты
    unit: юнит-тесты
"@

try {
    $pytestConfig | Out-File -FilePath "pytest.ini" -Encoding UTF8 -Force
    Write-Host "   ✅ pytest.ini создан" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Ошибка создания pytest.ini: $_" -ForegroundColor Red
}

# Шаг 5: Создать conftest.py
Write-Host ""
Write-Host "🔧 Создание tests/conftest.py..." -ForegroundColor Yellow

$conftestContent = @"
# tests/conftest.py
"""
Общие фикстуры для всех тестов
"""

import pytest
import sys
from pathlib import Path

# Добавляем src/ в путь
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def sample_data():
    """Тестовые данные рулетки"""
    return [
        {"number": 17, "color": "black"},
        {"number": 23, "color": "red"},
        {"number": 0, "color": "green"},
    ]

@pytest.fixture
def test_db_path(tmp_path):
    """Путь к временной тестовой БД"""
    return tmp_path / "test.db"
"@

try {
    $conftestContent | Out-File -FilePath "tests\conftest.py" -Encoding UTF8 -Force
    Write-Host "   ✅ tests/conftest.py создан" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Ошибка создания conftest.py: $_" -ForegroundColor Red
}

# Итоги
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ РЕФАКТОРИНГ ЗАВЕРШЕН!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Результаты:" -ForegroundColor Yellow
Write-Host "   ✅ Папка tests/ создана" -ForegroundColor Green
Write-Host "   ✅ Тесты перемещены: $movedCount файлов" -ForegroundColor Green
Write-Host "   ✅ tests/__init__.py создан" -ForegroundColor Green
Write-Host "   ✅ pytest.ini создан" -ForegroundColor Green
Write-Host "   ✅ tests/conftest.py создан" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Следующие шаги:" -ForegroundColor Yellow
Write-Host "   1. Установите pytest: pip install pytest" -ForegroundColor White
Write-Host "   2. Запустите тесты: pytest tests/" -ForegroundColor White
Write-Host "   3. С coverage: pytest --cov=src tests/" -ForegroundColor White
Write-Host ""
