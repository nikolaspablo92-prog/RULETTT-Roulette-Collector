"""
БЫСТРЫЙ ТЕСТ ВЕБ-СКРАПЕРА
=========================

Простой тест для проверки что скрапер может получить данные с вашей рулетки
"""

def quick_test():
    """Быстрый тест скрапера"""
    print("🧪 БЫСТРЫЙ ТЕСТ ВЕБ-СКРАПЕРА")
    print("="*60)
    
    # Проверяем установку Selenium
    print("\n1️⃣ Проверка установки Selenium...")
    try:
        from selenium import webdriver
        print("   ✅ Selenium установлен")
    except ImportError:
        print("   ❌ Selenium не установлен")
        print("   Установите: py -m pip install selenium webdriver-manager")
        return
    
    # Проверяем ChromeDriver
    print("\n2️⃣ Проверка ChromeDriver...")
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        service = Service(ChromeDriverManager().install())
        print("   ✅ ChromeDriver доступен")
    except Exception as e:
        print(f"   ⚠️ ChromeDriver: {e}")
        print("   Попробуем использовать системный ChromeDriver...")
    
    # Получаем информацию от пользователя
    print("\n" + "="*60)
    print("📋 ИНФОРМАЦИЯ ДЛЯ ТЕСТИРОВАНИЯ:")
    print("="*60)
    
    url = input("\n🌐 Введите URL страницы с рулеткой: ").strip()
    if not url:
        print("❌ URL не введен")
        return
    
    xpath = input("\n📍 Введите XPath элемента с результатами\n   (или Enter для использования по умолчанию): ").strip()
    if not xpath:
        xpath = "/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[4]"
    
    print(f"\n🎯 URL: {url}")
    print(f"🎯 XPath: {xpath}")
    
    confirm = input("\n▶️  Запустить тест? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Тест отменен")
        return
    
    # Запускаем тест
    print("\n" + "="*60)
    print("🚀 ЗАПУСК ТЕСТА...")
    print("="*60)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        # Настройка браузера
        print("\n🔧 Настройка браузера...")
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Создаем драйвер
        print("🌐 Запуск Chrome...")
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            driver = webdriver.Chrome(options=chrome_options)
        
        # Открываем страницу
        print(f"🌐 Открытие страницы: {url}")
        driver.get(url)
        
        # Ждем загрузку
        print("⏳ Ожидание загрузки страницы (10 секунд)...")
        time.sleep(10)
        
        # Ищем элемент
        print(f"\n🔍 Поиск элемента по XPath...")
        print(f"   XPath: {xpath}")
        
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            print("✅ Элемент найден!")
            
            # Получаем данные
            element_text = element.text
            element_html = element.get_attribute('innerHTML')
            
            print(f"\n📊 СОДЕРЖИМОЕ ЭЛЕМЕНТА:")
            print("-"*60)
            if element_text:
                print(f"Текст ({len(element_text)} символов):")
                print(element_text[:500])
            else:
                print("⚠️ Элемент не содержит текста")
            
            print(f"\nHTML ({len(element_html)} символов):")
            print(element_html[:500])
            
            # Ищем дочерние элементы
            children = element.find_elements(By.XPATH, ".//*")
            print(f"\n📊 Дочерних элементов: {len(children)}")
            
            if children:
                print("\nПервые 5 дочерних элементов:")
                for i, child in enumerate(children[:5], 1):
                    child_text = child.text
                    child_tag = child.tag_name
                    child_class = child.get_attribute('class')
                    print(f"  {i}. <{child_tag}> class='{child_class}': {child_text[:50]}")
            
            # Пытаемся найти числа
            print(f"\n🔢 ПОИСК ЧИСЕЛ РУЛЕТКИ (0-36)...")
            import re
            
            all_text = element_text + " " + element_html
            numbers_found = re.findall(r'\b([0-9]|[1-2][0-9]|3[0-6])\b', all_text)
            
            if numbers_found:
                unique_numbers = list(set([int(n) for n in numbers_found if 0 <= int(n) <= 36]))
                print(f"✅ Найдено чисел: {len(unique_numbers)}")
                print(f"Числа: {sorted(unique_numbers)[:20]}")
            else:
                print("❌ Числа рулетки не найдены")
                print("⚠️ Возможно нужен другой XPath")
            
            print("\n✅ ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
            print("\n💡 СЛЕДУЮЩИЕ ШАГИ:")
            print("1. Если числа найдены - используйте этот XPath")
            print("2. Если чисел нет - попробуйте другой элемент на странице")
            print("3. Запустите полный скрапер: python web_scraper_single_roulette.py")
            
        except Exception as e:
            print(f"❌ Элемент не найден: {e}")
            print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
            print("1. Неправильный XPath")
            print("2. Элемент загружается динамически (нужно больше ждать)")
            print("3. Элемент скрыт или не виден")
            print("\n💡 ПОПРОБУЙТЕ:")
            print("1. Проверьте XPath в консоли браузера:")
            print(f"   $x('{xpath}')")
            print("2. Попробуйте упрощенный XPath:")
            print("   //div[contains(@class, 'history')]")
            print("   //div[contains(@class, 'result')]")
        
        input("\n⏸️  Нажмите Enter для закрытия браузера...")
        driver.quit()
        print("✅ Браузер закрыт")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        print("\n💡 ВОЗМОЖНЫЕ РЕШЕНИЯ:")
        print("1. Установите Selenium: py -m pip install selenium webdriver-manager")
        print("2. Обновите Chrome до последней версии")
        print("3. Проверьте интернет-соединение")


if __name__ == "__main__":
    import time
    quick_test()