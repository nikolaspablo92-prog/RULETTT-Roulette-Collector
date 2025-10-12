"""
ТЕСТ С ВАШИМ CSS СЕЛЕКТОРОМ
============================

CSS Селектор (который вы предоставили):
#root > div > div.app-container > div.games-slots--kYClr > div > div.game-node--pwxxn > div > div > div.game-table > div.game-table__game-specific > div > div.game-area__history-line--Lkj9A > div > div:nth-child(3)

Преобразуем в XPath для использования в скрапере...
"""

def convert_css_to_xpath_and_test():
    """Преобразует CSS селектор в XPath и тестирует"""
    
    # Исходный CSS селектор
    css_selector = "#root > div > div.app-container > div.games-slots--kYClr > div > div.game-node--pwxxn > div > div > div.game-table > div.game-table__game-specific > div > div.game-area__history-line--Lkj9A > div > div:nth-child(3)"
    
    # Упрощенные варианты XPath
    xpath_options = [
        # Вариант 1: По классу game-area__history-line
        "//div[contains(@class, 'game-area__history-line')]//div",
        
        # Вариант 2: По классу game-table__game-specific
        "//div[contains(@class, 'game-table__game-specific')]//div[contains(@class, 'game-area__history-line')]",
        
        # Вариант 3: Прямой путь
        "//*[@id='root']/div/div[contains(@class, 'app-container')]//div[contains(@class, 'game-area__history-line')]",
        
        # Вариант 4: Самый простой
        "//div[contains(@class, 'history-line')]",
        
        # Вариант 5: По ID root и дальше
        "//*[@id='root']//div[contains(@class, 'game-area__history-line')]//div[3]"
    ]
    
    print(__doc__)
    print("\n🎯 ПРЕОБРАЗОВАННЫЕ XPATH ВАРИАНТЫ:")
    print("="*70)
    
    for i, xpath in enumerate(xpath_options, 1):
        print(f"\n{i}. {xpath}")
    
    print("\n" + "="*70)
    print("\n💡 РЕКОМЕНДАЦИЯ:")
    print("Начните с варианта 1 (самый простой)")
    print("Если не сработает, попробуйте другие варианты")
    
    return xpath_options

if __name__ == "__main__":
    xpaths = convert_css_to_xpath_and_test()
    
    print("\n" + "="*70)
    print("🚀 ГОТОВЫ К ТЕСТИРОВАНИЮ")
    print("="*70)
    
    print("\nВАРИАНТ А: Тест с автоматическим перебором XPath")
    print("-"*70)
    print("Запустите: python test_css_selector.py")
    print("Скрипт автоматически попробует все варианты XPath")
    
    print("\n\nВАРИАНТ Б: Ручной тест")
    print("-"*70)
    print("1. Запустите: python quick_scraper_test.py")
    print("2. Введите URL вашей рулетки")
    print("3. Введите один из XPath выше (рекомендуется вариант 1)")
    
    print("\n\n🎯 РЕКОМЕНДУЕМЫЙ XPATH ДЛЯ НАЧАЛА:")
    print("="*70)
    print(xpaths[0])
    print("="*70)