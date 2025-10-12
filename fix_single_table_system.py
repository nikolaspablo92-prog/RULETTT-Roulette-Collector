"""
ФИКС ОСНОВНОЙ СИСТЕМЫ - ТОЛЬКО ОДИН СТОЛ
========================================

Исправляем главную систему чтобы она работала ТОЛЬКО с одним столом roulettestura541
"""

import sys
from pathlib import Path

# Добавляем путь к строгому сборщику
sys.path.insert(0, str(Path(__file__).parent))
from strict_single_table import SingleTableOnlyCollector


def patch_main_system():
    """Патчим основную систему для работы с одним столом"""
    print("🔧 ПАТЧИНГ ОСНОВНОЙ СИСТЕМЫ...")
    print("🎯 НАСТРОЙКА НА ОДИН СТОЛ: roulettestura541")
    
    # Читаем main.py
    main_path = Path(__file__).parent / "src" / "main.py"
    if not main_path.exists():
        print(f"❌ Файл {main_path} не найден")
        return
    
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем импорт строгого сборщика в начало
        import_patch = '''
# ПАТЧ: Импорт строгого сборщика одного стола
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from strict_single_table import SingleTableOnlyCollector
    STRICT_COLLECTOR = SingleTableOnlyCollector("roulettestura541")
    print("✅ АКТИВИРОВАН СТРОГИЙ РЕЖИМ ОДНОГО СТОЛА: roulettestura541")
except ImportError as e:
    print(f"⚠️ Не удалось загрузить строгий сборщик: {e}")
    STRICT_COLLECTOR = None

'''
        
        # Вставляем патч после импортов
        if "from src.data_collector import DataCollector" in content:
            content = content.replace(
                "from src.data_collector import DataCollector",
                "from src.data_collector import DataCollector" + import_patch
            )
        
        # Патчим функцию получения реальных данных
        real_data_patch = '''
def get_real_data_single_table_only():
    """Получение данных ТОЛЬКО с одного стола"""
    print("🎯 ПОЛУЧЕНИЕ ДАННЫХ ТОЛЬКО С СТОЛА roulettestura541")
    
    if STRICT_COLLECTOR:
        try:
            results = STRICT_COLLECTOR.get_single_table_data(50)
            if results:
                print(f"✅ Получено {len(results)} результатов ТОЛЬКО с стола roulettestura541")
                
                # Сохраняем в основную базу данных
                data_collector = DataCollector()
                saved_count = 0
                
                for result in results:
                    try:
                        # Проверяем что результат с нужного стола
                        if result.get('table_id') == 'roulettestura541':
                            spin_id = data_collector.add_spin(
                                number=result['number'],
                                timestamp=result['timestamp'],
                                casino_name='Paddy Power + Pragmatic Play Live',
                                table_name='roulettestura541'
                            )
                            saved_count += 1
                        else:
                            print(f"🚫 Пропущен результат с чужого стола: {result.get('table_id')}")
                    except Exception as e:
                        print(f"⚠️ Ошибка сохранения результата: {e}")
                
                print(f"💾 Сохранено {saved_count} результатов в базу данных")
                
                # Показываем статистику
                show_single_table_stats(results)
                return True
            else:
                print("❌ Нет данных с указанного стола")
                return False
        except Exception as e:
            print(f"❌ Ошибка получения данных: {e}")
            return False
    else:
        print("❌ Строгий сборщик не доступен")
        return False

def show_single_table_stats(results):
    """Показывает статистику одного стола"""
    if not results:
        return
    
    print(f"\\n📊 СТАТИСТИКА СТОЛА roulettestura541:")
    print("-" * 40)
    
    # Последние результаты
    print("Последние результаты:")
    for i, result in enumerate(results[:10], 1):
        time_str = result['timestamp'].strftime("%H:%M:%S")
        print(f"  {i:2d}. {time_str}: {result['number']:2d} ({result['color']})")
    
    # Цветовая статистика
    colors = {'red': 0, 'black': 0, 'green': 0}
    for result in results:
        colors[result['color']] += 1
    
    total = len(results)
    print(f"\\nРаспределение цветов:")
    print(f"  Красные: {colors['red']} ({colors['red']/total*100:.1f}%)")
    print(f"  Черные: {colors['black']} ({colors['black']/total*100:.1f}%)")
    print(f"  Зеленые: {colors['green']} ({colors['green']/total*100:.1f}%)")

'''
        
        # Добавляем патч функций
        content += real_data_patch
        
        # Сохраняем патченый файл
        patched_path = Path(__file__).parent / "src" / "main_single_table.py"
        with open(patched_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Создан патченый файл: {patched_path}")
        print("🎯 Теперь используйте: python src/main_single_table.py")
        
    except Exception as e:
        print(f"❌ Ошибка патчинга: {e}")


def test_patched_system():
    """Тестируем патченую систему"""
    print("🧪 ТЕСТИРОВАНИЕ ПАТЧЕНОЙ СИСТЕМЫ")
    print("=" * 50)
    
    # Создаем строгий сборщик
    collector = SingleTableOnlyCollector("roulettestura541")
    
    # Получаем данные
    results = collector.get_single_table_data(20)
    
    if results:
        print(f"✅ Система работает! Получено {len(results)} результатов")
        
        # Проверяем что все с нужного стола
        wrong_table = [r for r in results if r.get('table_id') != 'roulettestura541']
        if wrong_table:
            print(f"❌ НАЙДЕНЫ ЧУЖИЕ СТОЛЫ: {len(wrong_table)}")
            for r in wrong_table:
                print(f"   - {r.get('table_id')}")
        else:
            print("✅ ВСЕ РЕЗУЛЬТАТЫ С ПРАВИЛЬНОГО СТОЛА!")
        
        # Статистика
        colors = {'red': 0, 'black': 0, 'green': 0}
        for result in results:
            colors[result['color']] += 1
        
        print(f"\\n📊 КРАТКАЯ СТАТИСТИКА:")
        print(f"Красные: {colors['red']}, Черные: {colors['black']}, Зеленые: {colors['green']}")
        
    else:
        print("❌ Нет данных")


if __name__ == "__main__":
    print("🔧 ИСПРАВЛЕНИЕ СИСТЕМЫ ДЛЯ РАБОТЫ С ОДНИМ СТОЛОМ")
    print("=" * 60)
    
    # Патчим систему
    patch_main_system()
    
    print("\\n" + "=" * 60)
    
    # Тестируем
    test_patched_system()
    
    print("\\n" + "=" * 60)
    print("🎯 ГОТОВО! Теперь система работает ТОЛЬКО с одним столом!")
    print("\\n📋 Команды для запуска:")
    print("  python src/main_single_table.py  # Патченая система")  
    print("  python strict_single_table.py    # Строгий сборщик")
    print("\\n⚠️  Больше никаких данных с других столов!")