"""
🎭 МЕТОД ДЛЯ OPERA BROWSER - ПОЛУЧИТЬ ДАННЫЕ ПРЯМО СЕЙЧАС!
==========================================================

Opera работает отлично! Вот что нужно сделать:

📋 ПОШАГОВАЯ ИНСТРУКЦИЯ:
========================

ШАГ 1: У вас уже открыта рулетка roulettestura541 в Opera ✅

ШАГ 2: Откройте Developer Tools (Инструменты разработчика):
         
         Нажмите: Ctrl + Shift + I
         ИЛИ
         Нажмите: F12
         ИЛИ
         ПКМ на странице → "Inspect Element" (Просмотреть код элемента)

ШАГ 3: Перейдите на вкладку "Console" (Консоль)
         
         В верхней части панели найдите вкладку "Console"

ШАГ 4: Вставьте этот код и нажмите Enter:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 🎰 ИЗВЛЕЧЕНИЕ ЧИСЕЛ ИЗ ВАШЕЙ РУЛЕТКИ (OPERA)

const selector = "#root > div > div.app-container > div.games-slots--kYClr > div > div.game-node--pwxxn > div > div > div.game-table > div.game-table__game-specific > div > div.game-area__history-line--Lkj9A";

console.log('🔍 Ищем элемент рулетки...');

const element = document.querySelector(selector);

if (element) {
    console.log('✅ Элемент найден!');
    
    // Извлекаем весь текст
    const allText = element.innerText + ' ' + element.innerHTML;
    console.log('📄 Текст элемента:', allText.substring(0, 100) + '...');
    
    // Ищем все числа рулетки (0-36)
    const numbers = allText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
    
    if (numbers && numbers.length > 0) {
        // Фильтруем и убираем дубликаты
        const validNumbers = numbers.filter(n => {
            const num = parseInt(n);
            return num >= 0 && num <= 36;
        });
        
        const unique = [...new Set(validNumbers)];
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('🎉 РЕЗУЛЬТАТЫ:');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('🎰 Найдено уникальных чисел:', unique.length);
        console.log('📊 Числа:', unique.join(', '));
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        
        // Создаем результат с цветами
        const results = unique.map(num => {
            const n = parseInt(num);
            let color = 'green';
            if (n > 0) {
                const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
                color = reds.includes(n) ? 'red' : 'black';
            }
            return {number: n, color: color};
        });
        
        console.log('');
        console.log('📋 Полные результаты с цветами:');
        console.table(results);
        
        // Копируем в буфер обмена
        const jsonResults = JSON.stringify(results, null, 2);
        
        // Для Opera используем navigator.clipboard
        if (navigator.clipboard) {
            navigator.clipboard.writeText(jsonResults).then(() => {
                console.log('');
                console.log('✅ ✅ ✅ ГОТОВО! ✅ ✅ ✅');
                console.log('📋 Результаты скопированы в буфер обмена!');
                console.log('💾 Нажмите Ctrl+V в текстовом редакторе');
            }).catch(() => {
                console.log('⚠️ Автокопирование не удалось');
                console.log('📋 Скопируйте JSON вручную:');
                console.log(jsonResults);
            });
        } else {
            console.log('📋 JSON результат:');
            console.log(jsonResults);
            console.log('');
            console.log('💡 Скопируйте JSON выше вручную (Ctrl+C)');
        }
        
    } else {
        console.log('❌ Числа рулетки не найдены в элементе');
        console.log('💡 Показываем содержимое элемента:');
        console.log(element);
    }
} else {
    console.log('❌ Элемент не найден с основным селектором');
    console.log('');
    console.log('🔄 Пробуем альтернативные селекторы...');
    console.log('');
    
    // Пробуем упрощенные селекторы
    const alternatives = [
        ".game-area__history-line",
        "[class*='history-line']",
        ".game-table__game-specific",
        ".game-table"
    ];
    
    for (let altSelector of alternatives) {
        console.log('🔍 Пробуем:', altSelector);
        const altElement = document.querySelector(altSelector);
        if (altElement) {
            console.log('✅ Найден! Используйте этот селектор:');
            console.log('const selector = "' + altSelector + '";');
            break;
        }
    }
}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ШАГ 5: Смотрите результаты в консоли!
         Данные автоматически скопируются в буфер обмена

ШАГ 6: Нажмите Ctrl+V в текстовом редакторе
         Сохраните в файл roulette_data.json

🎉 ЧТО ВЫ ПОЛУЧИТЕ:
===================

[
  {"number": 25, "color": "red"},
  {"number": 14, "color": "red"},
  {"number": 0, "color": "green"},
  {"number": 32, "color": "red"},
  {"number": 15, "color": "black"},
  ...
]

Это данные ТОЛЬКО с вашей рулетки roulettestura541!
Никаких смешанных результатов с других столов!

🔄 ЕСЛИ ЭЛЕМЕНТ НЕ НАЙДЕН:
==========================

Код автоматически попробует альтернативные селекторы:
- .game-area__history-line
- [class*='history-line']
- .game-table__game-specific
- .game-table

Если найдет - покажет рабочий селектор!

📊 МОНИТОРИНГ В РЕАЛЬНОМ ВРЕМЕНИ (ОПЦИЯ):
=========================================

Для автообновления каждые 30 секунд вставьте этот код:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 🔄 АВТОМОНИТОРИНГ РУЛЕТКИ

const selector = ".game-area__history-line";
let lastNumbers = [];

console.log('🔄 Запуск автомониторинга...');
console.log('⏰ Обновление каждые 30 секунд');
console.log('⏹️  Для остановки обновите страницу (F5)');
console.log('');

setInterval(() => {
    const element = document.querySelector(selector);
    if (element) {
        const allText = element.innerText + ' ' + element.innerHTML;
        const numbers = allText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
        
        if (numbers) {
            const unique = [...new Set(numbers.filter(n => n >= 0 && n <= 36))];
            
            // Проверяем изменения
            if (JSON.stringify(unique.sort()) !== JSON.stringify(lastNumbers.sort())) {
                const time = new Date().toLocaleTimeString('ru-RU');
                console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                console.log('🕐 ' + time + ' - НОВЫЕ ДАННЫЕ!');
                console.log('🎰 Числа:', unique.join(', '));
                console.log('📊 Всего:', unique.length);
                
                // Показываем новые числа
                const newNumbers = unique.filter(n => !lastNumbers.includes(n));
                if (newNumbers.length > 0) {
                    console.log('✨ Новые:', newNumbers.join(', '));
                }
                
                lastNumbers = unique;
            }
        }
    }
}, 30000); // 30 секунд
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 СОВЕТЫ ДЛЯ OPERA:
====================

✅ Консоль Opera работает так же, как в Chrome
✅ Поддерживает все современные JS функции
✅ Можно держать консоль открытой во время игры
✅ Результаты копируются автоматически

🔧 ЕСЛИ ВОЗНИКЛИ ПРОБЛЕМЫ:
==========================

1. Элемент не найден?
   → Попробуйте упрощенный селектор: ".game-area__history-line"

2. Числа не извлекаются?
   → Откройте Elements (Элементы) и найдите нужный div вручную
   → ПКМ → Copy → Copy selector

3. Автокопирование не работает?
   → Скопируйте JSON вручную из консоли (выделите и Ctrl+C)

4. Нужна помощь?
   → Сделайте скриншот консоли
   → Покажите, что выводится

═══════════════════════════════════════════════════════════
🎭 ГОТОВО ДЛЯ OPERA! ОТКРОЙТЕ КОНСОЛЬ И НАЧНИТЕ!
═══════════════════════════════════════════════════════════

Ctrl+Shift+I → Console → Вставить код → Enter → Готово! 🎰✨
"""

if __name__ == "__main__":
    print(__doc__)