"""
🎭 ИСПРАВЛЕННЫЙ КОД ДЛЯ OPERA - БЕЗ ОШИБОК!
==========================================

❌ ОШИБКА: "Uncaught SyntaxError: Unexpected token 'const'"
✅ РЕШЕНИЕ: Используем немедленно вызываемую функцию (IIFE)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 РАБОЧИЙ КОД - СКОПИРУЙТЕ И ВСТАВЬТЕ В КОНСОЛЬ OPERA:
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
            
            const results = unique.map(num => {
                const n = parseInt(num);
                const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
                return {
                    number: n, 
                    color: n === 0 ? 'green' : (reds.includes(n) ? 'red' : 'black')
                };
            });
            
            console.table(results);
            
            const jsonResults = JSON.stringify(results, null, 2);
            
            navigator.clipboard.writeText(jsonResults).then(() => {
                console.log('');
                console.log('✅ ✅ ✅ ГОТОВО! ✅ ✅ ✅');
                console.log('📋 Результаты скопированы в буфер обмена!');
                console.log('💾 Нажмите Ctrl+V в текстовом редакторе');
            }).catch(() => {
                console.log('📋 JSON для копирования:');
                console.log(jsonResults);
            });
            
        } else {
            console.log('❌ Числа не найдены');
            console.log('📄 Содержимое элемента:', allText.substring(0, 200));
        }
    } else {
        console.log('❌ Элемент не найден с основным селектором');
        console.log('');
        console.log('🔄 Пробуем альтернативные селекторы...');
        
        const alternatives = [
            ".game-area__history-line--Lkj9A",
            ".game-area__history-line",
            "[class*='history-line']",
            ".game-table__game-specific"
        ];
        
        for (let altSelector of alternatives) {
            console.log('🔍 Пробуем:', altSelector);
            const altElement = document.querySelector(altSelector);
            if (altElement) {
                console.log('✅ ✅ НАЙДЕН! Используйте этот селектор:');
                console.log(altSelector);
                console.log('');
                console.log('📝 Повторите код с этим селектором!');
                break;
            }
        }
    }
})();

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ЧТО ИЗМЕНИЛОСЬ:
==================

✅ Код обернут в (function() { ... })(); 
✅ Избегает конфликтов с уже объявленными переменными
✅ Работает при повторном запуске
✅ Автоматически пробует альтернативные селекторы

💡 УПРОЩЕННЫЕ ВАРИАНТЫ (если основной не работает):
==================================================

ВАРИАНТ 1 - Упрощенный селектор:
────────────────────────────────

(function() {
    const elem = document.querySelector(".game-area__history-line--Lkj9A");
    if (elem) {
        const nums = (elem.innerText + ' ' + elem.innerHTML).match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
        if (nums) {
            const unique = [...new Set(nums.filter(n => n >= 0 && n <= 36))];
            console.log('✅ Числа:', unique.join(', '));
            navigator.clipboard.writeText(JSON.stringify(unique));
            console.log('📋 Скопировано!');
        }
    } else {
        console.log('❌ Элемент не найден');
    }
})();


ВАРИАНТ 2 - Еще проще (по классу):
───────────────────────────────────

(function() {
    const elem = document.querySelector("[class*='history-line']");
    if (elem) {
        const nums = elem.innerText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
        if (nums) {
            console.log('✅ Найдено:', nums.length, 'чисел');
            console.log('📊 Числа:', nums.join(', '));
            navigator.clipboard.writeText(nums.join(', '));
        }
    }
})();


ВАРИАНТ 3 - По game-table:
──────────────────────────

(function() {
    const elem = document.querySelector(".game-table__game-specific");
    if (elem) {
        const nums = elem.innerText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
        if (nums) {
            const unique = [...new Set(nums)];
            console.log('🎰 Числа:', unique.join(', '));
        }
    }
})();

🔄 АВТОМОНИТОРИНГ (обновление каждые 30 сек):
=============================================

(function() {
    let lastNumbers = [];
    
    console.log('🔄 Запуск автомониторинга рулетки...');
    console.log('⏰ Обновление каждые 30 секунд');
    console.log('⏹️  Для остановки: location.reload()');
    console.log('');
    
    setInterval(() => {
        const elem = document.querySelector("[class*='history-line']");
        if (elem) {
            const nums = elem.innerText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
            if (nums) {
                const unique = [...new Set(nums)].sort((a,b) => a-b);
                const changed = JSON.stringify(unique) !== JSON.stringify(lastNumbers);
                
                if (changed) {
                    const time = new Date().toLocaleTimeString('ru-RU');
                    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                    console.log('🕐', time, '- ОБНОВЛЕНИЕ');
                    console.log('🎰 Числа:', unique.join(', '));
                    console.log('📊 Всего:', unique.length);
                    lastNumbers = unique;
                }
            }
        }
    }, 30000);
})();

═══════════════════════════════════════════════════════════
🎭 ГОТОВО! ВЫБЕРИТЕ ЛЮБОЙ ВАРИАНТ И ВСТАВЬТЕ В КОНСОЛЬ!
═══════════════════════════════════════════════════════════

Ctrl+Shift+I → Console → Вставить → Enter → Готово! 🎰✨
"""

if __name__ == "__main__":
    print(__doc__)