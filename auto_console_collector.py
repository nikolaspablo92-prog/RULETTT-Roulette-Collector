"""
🔄 АВТОМАТИЧЕСКИЙ СБОРЩИК ДАННЫХ ИЗ КОНСОЛИ
===========================================

Этот скрипт создает JavaScript код для автоматического сбора
данных с рулетки в браузере и их экспорта в Python.

ИСПОЛЬЗОВАНИЕ:
1. Запустите: py auto_console_collector.py
2. Скопируйте сгенерированный JavaScript код
3. Вставьте в консоль браузера Opera
4. Данные будут автоматически сохраняться и готовы для анализа
"""

import json
from pathlib import Path
from datetime import datetime


def generate_console_code() -> str:
    """Генерирует JavaScript код для вставки в консоль"""
    
    js_code = '''
// ============================================
// 🎰 АВТОМАТИЧЕСКИЙ СБОРЩИК ДАННЫХ РУЛЕТКИ
// ============================================

(function() {
    // Конфигурация
    const CONFIG = {
        selector: ".game-area__history-line--Lkj9A",
        updateInterval: 30000,  // 30 секунд
        maxResults: 100,        // Максимум результатов
        autoExport: true,       // Автоматический экспорт
        storageKey: "rouletteData"
    };
    
    // Хранилище данных
    let allResults = [];
    let lastCheck = null;
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎰 АВТОМАТИЧЕСКИЙ СБОРЩИК ДАННЫХ ЗАПУЩЕН!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('⏰ Обновление каждые', CONFIG.updateInterval / 1000, 'секунд');
    console.log('📊 Максимум результатов:', CONFIG.maxResults);
    console.log('⏹️  Остановка: stopRouletteCollector()');
    console.log('📋 Экспорт данных: exportRouletteData()');
    console.log('📈 Показать статистику: showRouletteStats()');
    console.log('🗑️  Очистить данные: clearRouletteData()');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    
    // Загружаем сохраненные данные
    function loadSavedData() {
        try {
            const saved = localStorage.getItem(CONFIG.storageKey);
            if (saved) {
                allResults = JSON.parse(saved);
                console.log('📂 Загружено', allResults.length, 'сохраненных результатов');
            }
        } catch (e) {
            console.error('❌ Ошибка загрузки данных:', e);
        }
    }
    
    // Сохраняем данные
    function saveData() {
        try {
            localStorage.setItem(CONFIG.storageKey, JSON.stringify(allResults));
        } catch (e) {
            console.error('❌ Ошибка сохранения:', e);
        }
    }
    
    // Функция сбора данных
    function collectData() {
        const element = document.querySelector(CONFIG.selector);
        
        if (!element) {
            console.warn('⚠️ Элемент рулетки не найден');
            return;
        }
        
        const allText = element.innerText + ' ' + element.innerHTML;
        const numbers = allText.match(/\\b([0-9]|[1-2][0-9]|3[0-6])\\b/g);
        
        if (!numbers || numbers.length === 0) {
            return;
        }
        
        // Фильтруем числа рулетки
        const validNumbers = numbers.filter(n => {
            const num = parseInt(n);
            return num >= 0 && num <= 36;
        });
        
        // Определяем цвет
        const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
        
        // Добавляем новые результаты
        validNumbers.forEach(numStr => {
            const num = parseInt(numStr);
            const color = num === 0 ? 'green' : (reds.includes(num) ? 'red' : 'black');
            
            // Проверяем что это новый результат
            const isDuplicate = allResults.some(r => 
                r.number === num && 
                Math.abs(new Date(r.timestamp) - new Date()) < 60000
            );
            
            if (!isDuplicate) {
                allResults.unshift({
                    number: num,
                    color: color,
                    timestamp: new Date().toISOString(),
                    table: "console_collector"
                });
            }
        });
        
        // Ограничиваем размер
        if (allResults.length > CONFIG.maxResults) {
            allResults = allResults.slice(0, CONFIG.maxResults);
        }
        
        // Сохраняем
        saveData();
        
        // Показываем последнее число
        if (allResults.length > 0 && (!lastCheck || allResults[0].timestamp !== lastCheck)) {
            const latest = allResults[0];
            const emoji = latest.color === 'red' ? '🔴' : 
                         latest.color === 'black' ? '⚫' : '🟢';
            const time = new Date(latest.timestamp).toLocaleTimeString('ru-RU');
            
            console.log(time, emoji, latest.number, '- Всего:', allResults.length, 'результатов');
            lastCheck = latest.timestamp;
        }
    }
    
    // Экспорт данных
    window.exportRouletteData = function() {
        const jsonData = JSON.stringify(allResults, null, 2);
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 ЭКСПОРТ ДАННЫХ ДЛЯ PYTHON АНАЛИЗА');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📊 Всего результатов:', allResults.length);
        console.log('');
        console.log('1️⃣ Данные скопированы в буфер обмена!');
        console.log('2️⃣ Создайте файл: roulette_console_data.json');
        console.log('3️⃣ Вставьте данные (Ctrl+V)');
        console.log('4️⃣ Запустите: py console_to_analysis.py');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('');
        console.log(jsonData);
        console.log('');
        
        // Копируем в буфер
        navigator.clipboard.writeText(jsonData)
            .then(() => console.log('✅ Данные скопированы в буфер обмена!'))
            .catch(() => console.log('⚠️ Скопируйте JSON выше вручную'));
        
        return allResults;
    };
    
    // Показать статистику
    window.showRouletteStats = function() {
        if (allResults.length === 0) {
            console.log('❌ Нет данных для статистики');
            return;
        }
        
        const colors = {red: 0, black: 0, green: 0};
        const numbers = {};
        
        allResults.forEach(r => {
            colors[r.color]++;
            numbers[r.number] = (numbers[r.number] || 0) + 1;
        });
        
        const total = allResults.length;
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📊 СТАТИСТИКА СОБРАННЫХ ДАННЫХ');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('🎰 Всего спинов:', total);
        console.log('');
        console.log('🎨 Распределение цветов:');
        console.log('  🔴 Красных:', colors.red, `(${(colors.red/total*100).toFixed(1)}%)`);
        console.log('  ⚫ Черных:', colors.black, `(${(colors.black/total*100).toFixed(1)}%)`);
        console.log('  🟢 Зеленых:', colors.green, `(${(colors.green/total*100).toFixed(1)}%)`);
        console.log('');
        
        const topNumbers = Object.entries(numbers)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
        
        console.log('🔥 Топ-5 чисел:');
        topNumbers.forEach(([num, count], i) => {
            const n = parseInt(num);
            const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
            const emoji = n === 0 ? '🟢' : (reds.includes(n) ? '🔴' : '⚫');
            console.log(`  ${i+1}. ${emoji} ${num}: ${count} раз`);
        });
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    };
    
    // Очистить данные
    window.clearRouletteData = function() {
        allResults = [];
        localStorage.removeItem(CONFIG.storageKey);
        console.log('🗑️ Данные очищены');
    };
    
    // Остановить сборщик
    window.stopRouletteCollector = function() {
        if (window.rouletteCollectorInterval) {
            clearInterval(window.rouletteCollectorInterval);
            console.log('⏹️ Сборщик данных остановлен');
            console.log('📊 Собрано результатов:', allResults.length);
            console.log('💡 Экспорт: exportRouletteData()');
        }
    };
    
    // Загружаем сохраненные данные
    loadSavedData();
    
    // Первый сбор
    collectData();
    
    // Запускаем автоматический сбор
    window.rouletteCollectorInterval = setInterval(collectData, CONFIG.updateInterval);
    
    console.log('✅ Сборщик активен! Данные обновляются автоматически...');
    console.log('');
    
})();

// ============================================
// 🎯 ГОТОВО! СБОРЩИК РАБОТАЕТ!
// ============================================
'''
    
    return js_code


def create_sample_json():
    """Создает пример JSON файла"""
    sample_data = [
        {"number": 6, "color": "black", "timestamp": datetime.now().isoformat(), "table": "console_collector"},
        {"number": 24, "color": "black", "timestamp": datetime.now().isoformat(), "table": "console_collector"},
        {"number": 4, "color": "black", "timestamp": datetime.now().isoformat(), "table": "console_collector"},
    ]
    
    with open("roulette_console_data_example.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    return sample_data


def main():
    """Основная функция"""
    print("="*70)
    print("🔄 ГЕНЕРАТОР АВТОМАТИЧЕСКОГО СБОРЩИКА ДАННЫХ")
    print("="*70)
    print()
    
    # Генерируем код
    js_code = generate_console_code()
    
    # Сохраняем в файл
    output_file = "auto_collector_console_code.js"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(js_code)
    
    print(f"✅ JavaScript код сохранен в: {output_file}")
    print()
    
    # Создаем пример JSON
    sample = create_sample_json()
    print(f"✅ Пример JSON создан: roulette_console_data_example.json")
    print()
    
    print("="*70)
    print("📋 ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:")
    print("="*70)
    print()
    print("1️⃣ Откройте файл:", output_file)
    print("2️⃣ Скопируйте весь код (Ctrl+A, Ctrl+C)")
    print("3️⃣ Откройте страницу рулетки в Opera")
    print("4️⃣ Откройте консоль (Ctrl+Shift+I → Console)")
    print("5️⃣ Вставьте код и нажмите Enter")
    print()
    print("🎯 СБОРЩИК ЗАПУЩЕН! Он будет:")
    print("   ✅ Автоматически собирать данные каждые 30 секунд")
    print("   ✅ Сохранять их в localStorage браузера")
    print("   ✅ Показывать новые результаты в консоли")
    print()
    print("="*70)
    print("🛠️ ДОСТУПНЫЕ КОМАНДЫ В КОНСОЛИ:")
    print("="*70)
    print()
    print("exportRouletteData()     - Экспорт данных для Python")
    print("showRouletteStats()      - Показать статистику")
    print("stopRouletteCollector()  - Остановить сборщик")
    print("clearRouletteData()      - Очистить все данные")
    print()
    print("="*70)
    print("📊 АНАЛИЗ ДАННЫХ В PYTHON:")
    print("="*70)
    print()
    print("1️⃣ В консоли браузера: exportRouletteData()")
    print("2️⃣ Данные скопируются в буфер обмена")
    print("3️⃣ Создайте файл: roulette_console_data.json")
    print("4️⃣ Вставьте данные (Ctrl+V)")
    print("5️⃣ Запустите: py console_to_analysis.py")
    print()
    print("✅ Готово! Система будет анализировать ваши данные!")
    print()
    print("="*70)


if __name__ == "__main__":
    main()
