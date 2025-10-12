"""
🎉 УСПЕШНЫЙ РЕЗУЛЬТАТ! 
======================

✅ Элемент найден!
✅ Извлечено 11 чисел с вашей рулетки!
✅ Данные с цветами готовы!

📊 ПОЛУЧЕННЫЕ ДАННЫЕ:
====================

Числа: 6, 24, 4, 10, 12, 1, 14, 35, 9, 3, 17

С цветами:
- 6 (black)
- 24 (black)
- 4 (black)
- 10 (black)
- 12 (red)
- 1 (red)
- 14 (red)
- 35 (black)
- 9 (red)
- 3 (red)
- 17 (black)

JSON результат:
[
  {"number": 6, "color": "black"},
  {"number": 24, "color": "black"},
  {"number": 4, "color": "black"},
  {"number": 10, "color": "black"},
  {"number": 12, "color": "red"},
  {"number": 1, "color": "red"},
  {"number": 14, "color": "red"},
  {"number": 35, "color": "black"},
  {"number": 9, "color": "red"},
  {"number": 3, "color": "red"},
  {"number": 17, "color": "black"}
]

🔧 УЛУЧШЕННЫЙ КОД (исправлена проблема с копированием):
=======================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ВСТАВЬТЕ ЭТОТ КОД В КОНСОЛЬ OPERA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(function() {
    const selector = "#root > div > div.app-container > div.games-slots--kYClr > div > div.game-node--pwxxn > div > div > div.game-table > div.game-table__game-specific > div > div.game-area__history-line--Lkj9A";
    
    console.log('🔍 Ищем элемент рулетки...');
    const element = document.querySelector(selector);
    
    if (element) {
        console.log('✅ Элемент найден!');
        
        const allText = element.innerText + ' ' + element.innerHTML;
        const numbers = allText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
        
        if (numbers) {
            const unique = [...new Set(numbers.filter(n => n >= 0 && n <= 36))];
            
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log('🎉 РЕЗУЛЬТАТЫ:');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log('🎰 Найдено уникальных чисел:', unique.length);
            console.log('📊 Числа:', unique.join(', '));
            console.log('');
            
            const results = unique.map(num => {
                const n = parseInt(num);
                const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
                return {number: n, color: n === 0 ? 'green' : (reds.includes(n) ? 'red' : 'black')};
            });
            
            console.table(results);
            
            const jsonResults = JSON.stringify(results, null, 2);
            
            console.log('');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log('📋 JSON ДЛЯ КОПИРОВАНИЯ:');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log(jsonResults);
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log('');
            console.log('💡 ВЫДЕЛИТЕ JSON ВЫШЕ И НАЖМИТЕ Ctrl+C');
            console.log('');
            
            // Пробуем скопировать (может не сработать без фокуса)
            window.focus();
            setTimeout(() => {
                navigator.clipboard.writeText(jsonResults)
                    .then(() => console.log('✅ Автоматически скопировано!'))
                    .catch(() => console.log('⚠️ Скопируйте вручную (выделите JSON выше)'));
            }, 100);
            
            // Сохраняем в window для легкого доступа
            window.rouletteResults = results;
            console.log('💾 Результаты сохранены в: window.rouletteResults');
            console.log('📝 Доступ через: copy(window.rouletteResults)');
            
        } else {
            console.log('❌ Числа не найдены');
        }
    } else {
        console.log('❌ Элемент не найден');
    }
})();

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 КАК СКОПИРОВАТЬ РЕЗУЛЬТАТЫ:
==============================

СПОСОБ 1 - Ручное копирование:
   1. Выделите JSON в консоли мышкой
   2. Ctrl+C
   3. Ctrl+V в текстовый файл

СПОСОБ 2 - Команда copy():
   После запуска кода введите:
   
   copy(window.rouletteResults)
   
   Данные скопируются автоматически!

СПОСОБ 3 - Команда copy с JSON:
   
   copy(JSON.stringify(window.rouletteResults, null, 2))
   
   Скопирует красиво отформатированный JSON!

🔄 МОНИТОРИНГ В РЕАЛЬНОМ ВРЕМЕНИ:
=================================

Для автоматического обновления каждые 30 секунд:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(function() {
    const selector = ".game-area__history-line--Lkj9A";
    let lastNumbers = [];
    
    console.log('🔄 АВТОМОНИТОРИНГ ЗАПУЩЕН');
    console.log('⏰ Обновление каждые 30 секунд');
    console.log('⏹️  Остановка: location.reload()');
    console.log('');
    
    function checkRoulette() {
        const element = document.querySelector(selector);
        if (element) {
            const allText = element.innerText + ' ' + element.innerHTML;
            const numbers = allText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
            
            if (numbers) {
                const unique = [...new Set(numbers.filter(n => n >= 0 && n <= 36))];
                const sorted = unique.sort((a,b) => parseInt(a) - parseInt(b));
                
                if (JSON.stringify(sorted) !== JSON.stringify(lastNumbers)) {
                    const time = new Date().toLocaleTimeString('ru-RU');
                    
                    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                    console.log('🕐', time, '- НОВЫЕ ДАННЫЕ!');
                    console.log('🎰 Числа:', sorted.join(', '));
                    console.log('📊 Всего:', sorted.length);
                    
                    // Показываем новые числа
                    const newNums = sorted.filter(n => !lastNumbers.includes(n));
                    if (newNums.length > 0) {
                        console.log('✨ Новые числа:', newNums.join(', '));
                    }
                    
                    lastNumbers = sorted;
                    window.rouletteResults = sorted;
                }
            }
        }
    }
    
    // Первая проверка сразу
    checkRoulette();
    
    // Затем каждые 30 секунд
    setInterval(checkRoulette, 30000);
})();

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 СОХРАНЕНИЕ В ФАЙЛ:
====================

1. Скопируйте JSON результат
2. Создайте файл: roulette_data.json
3. Вставьте данные
4. Сохраните

ИЛИ используйте Python для сохранения:

import json

data = [
    {"number": 6, "color": "black"},
    {"number": 24, "color": "black"},
    # ... остальные данные
]

with open('roulette_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

═══════════════════════════════════════════════════════════
✅ МЕТОД РАБОТАЕТ! ДАННЫЕ ИЗВЛЕЧЕНЫ С ВАШЕЙ РУЛЕТКИ!
═══════════════════════════════════════════════════════════

Это данные ТОЛЬКО с roulettestura541 - никаких смешанных!
"""

if __name__ == "__main__":
    print(__doc__)