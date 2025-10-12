#!/usr/bin/env python3
"""
Тест сравнения стратегий
"""

import sys
import os
from pathlib import Path

# Добавляем путь к src
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "src"))

try:
    from src.main import RouletteAnalysisSystem
    
    print("=== ТЕСТ СРАВНЕНИЯ СТРАТЕГИЙ ===")
    
    # Создаем систему
    system = RouletteAnalysisSystem()
    
    print("Тестируем метод compare_strategies...")
    
    # Тестируем наличие метода
    if hasattr(system, 'compare_strategies'):
        print("✅ Метод compare_strategies найден")
    else:
        print("❌ Метод compare_strategies НЕ найден")
    
    print("\nВсе методы системы:")
    methods = [method for method in dir(system) if not method.startswith('_')]
    for method in methods:
        print(f"  - {method}")

except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()