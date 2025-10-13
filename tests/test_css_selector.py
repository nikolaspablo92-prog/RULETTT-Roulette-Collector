"""
АВТОМАТИЧЕСКИЙ ТЕСТ ВСЕХ XPATH ВАРИАНТОВ
========================================

Тестирует все варианты XPath чтобы найти правильный элемент с вашей рулетки
"""

import time
import sys


def test_all_xpaths():
    """Тестирует все варианты XPath"""
    
    print("🧪 АВТОМАТИЧЕСКИЙ ТЕСТ XPATH ВАРИАНТОВ")
    print("="*70)
    
    # URL страницы
    url = input("\n🌐 Введите URL страницы с рулеткой: ").strip()
    if not url:
        print("❌ URL не введен")
        return
    
    # Варианты XPath
    xpath_options = {
        "1. По классу history-line (простой)": "//div[contains(@class, 'game-area__history-line')]//div",
        "2. По game-table__game-specific": "//div[contains(@class, 'game-table__game-specific')]//div[contains(@class, 'game-area__history-line')]",
        "3. От root элемента": "//*[@id='root']//div[contains(@class, 'game-area__history-line')]",
        "4. Упрощенный history": "//div[contains(@class, 'history-line')]",
        "5. С индексом [3]": "//*[@id='root']//div[contains(@class, 'game-area__history-line')]//div[3]",
        "6. Прямой путь от root": "//*[@id='root']/div/div/div/div/div/div/div/div/div/div/div/div[contains(@class, 'history')]",
        "7. Любой div с историей": "//div[contains(@class, 'history')]",
        "8. CSS селектор как есть": "#root > div > div.app-container > div.games-slots--kYClr > div > div.game-node--pwxxn > div > div > div.game-table > div.game-table__game-specific > div > div.game-area__history-line--Lkj9A > div > div:nth-child(3)"
    }
    
    print(f"\n🎯 URL: {url}")
    print(f"\n🔍 Будем тестировать {len(xpath_options)} вариантов XPath")
    
    confirm = input("\n▶️  Начать тестирование? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Тест отменен")
        return
    
    # Импорты
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
    except ImportError:
        print("❌ Selenium не установлен!")
        print("   Запустите: py -m pip install selenium webdriver-manager")
        return
    
    # Настройка браузера
    print("\n🔧 Настройка браузера...")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except:
        driver = webdriver.Chrome(options=chrome_options)
    
    # Открываем страницу
    print(f"🌐 Открытие страницы...")
    driver.get(url)
    
    print("⏳ Ожидание загрузки (15 секунд)...")
    time.sleep(15)
    
    # Тестируем каждый XPath
    successful_xpaths = []
    
    print("\n" + "="*70)
    print("🔍 ТЕСТИРОВАНИЕ XPATH ВАРИАНТОВ:")
    print("="*70)
    
    for description, xpath in xpath_options.items():
        print(f"\n📍 Тестируем: {description}")
        print(f"   XPath: {xpath[:80]}...")
        
        try:
            # Для CSS селектора используем другой метод
            if xpath.startswith("#"):
                print("   ℹ️  Это CSS селектор, конвертируем...")
                # Используем CSS_SELECTOR вместо XPATH
                try:
                    element = driver.find_element(By.CSS_SELECTOR, xpath)
                    element_text = element.text
                    element_html = element.get_attribute('innerHTML')
                    children = element.find_elements(By.XPATH, ".//*")
                    
                    print(f"   ✅ НАЙДЕН! (CSS селектор)")
                    print(f"   📊 Текст: {element_text[:100]}")
                    print(f"   📊 Дочерних элементов: {len(children)}")
                    
                    successful_xpaths.append({
                        'description': description,
                        'selector': xpath,
                        'type': 'CSS',
                        'text': element_text,
                        'children': len(children)
                    })
                except:
                    print(f"   ❌ Не найден (CSS)")
                continue
            
            # Для XPath
            wait = WebDriverWait(driver, 5)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            # Получаем данные
            element_text = element.text
            element_html = element.get_attribute('innerHTML')
            children = element.find_elements(By.XPATH, ".//*")
            
            print(f"   ✅ НАЙДЕН!")
            print(f"   📊 Текст ({len(element_text)} символов): {element_text[:100]}")
            print(f"   📊 HTML ({len(element_html)} символов): {element_html[:100]}")
            print(f"   📊 Дочерних элементов: {len(children)}")
            
            # Ищем числа
            import re
            numbers = re.findall(r'\b([0-9]|[1-2][0-9]|3[0-6])\b', element_text + " " + element_html)
            if numbers:
                unique_numbers = list(set([int(n) for n in numbers if 0 <= int(n) <= 36]))
                print(f"   🎯 Найдено чисел рулетки: {len(unique_numbers)}")
                print(f"   🎯 Числа: {sorted(unique_numbers)[:10]}")
            
            successful_xpaths.append({
                'description': description,
                'xpath': xpath,
                'type': 'XPATH',
                'text': element_text,
                'children': len(children),
                'numbers': numbers if numbers else []
            })
            
        except Exception as e:
            print(f"   ❌ Не найден: {str(e)[:50]}")
    
    # Результаты
    print("\n" + "="*70)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print("="*70)
    
    if successful_xpaths:
        print(f"\n✅ УСПЕШНО НАЙДЕНО: {len(successful_xpaths)} вариант(ов)")
        
        for i, result in enumerate(successful_xpaths, 1):
            print(f"\n{i}. {result['description']}")
            print(f"   Тип: {result['type']}")
            if result['type'] == 'XPATH':
                print(f"   XPath: {result['xpath']}")
            else:
                print(f"   CSS: {result['selector']}")
            print(f"   Дочерних: {result['children']}")
            if 'numbers' in result and result['numbers']:
                print(f"   Чисел найдено: {len(result['numbers'])}")
        
        print("\n" + "="*70)
        print("💡 РЕКОМЕНДАЦИЯ:")
        print("="*70)
        
        # Находим лучший вариант (с числами и детьми)
        best = None
        for result in successful_xpaths:
            if 'numbers' in result and result['numbers'] and result['children'] > 0:
                if not best or len(result['numbers']) > len(best.get('numbers', [])):
                    best = result
        
        if best:
            print(f"\n🏆 ЛУЧШИЙ ВАРИАНТ: {best['description']}")
            if best['type'] == 'XPATH':
                print(f"\n📋 Используйте этот XPath:")
                print(f"{best['xpath']}")
            else:
                print(f"\n📋 Используйте этот CSS селектор:")
                print(f"{best['selector']}")
            
            print(f"\n🎯 В этом элементе найдено {len(best.get('numbers', []))} чисел рулетки")
            print(f"🎯 Дочерних элементов: {best['children']}")
        else:
            print(f"\n🎯 Используйте первый успешный вариант:")
            if successful_xpaths[0]['type'] == 'XPATH':
                print(f"{successful_xpaths[0]['xpath']}")
            else:
                print(f"{successful_xpaths[0]['selector']}")
    else:
        print("\n❌ НИ ОДИН ВАРИАНТ НЕ СРАБОТАЛ")
        print("\n💡 ПОПРОБУЙТЕ:")
        print("1. Увеличить время ожидания загрузки")
        print("2. Проверить что страница полностью загружена")
        print("3. Найти элемент вручную в DevTools")
        print("4. Использовать более простой селектор:")
        print("   //div[contains(@class, 'ball')]")
        print("   //div[contains(@class, 'number')]")
    
    input("\n⏸️  Нажмите Enter для закрытия браузера...")
    driver.quit()
    print("✅ Браузер закрыт")


if __name__ == "__main__":
    test_all_xpaths()