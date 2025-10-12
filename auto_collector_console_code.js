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
    console.log('� Сохранить статистику: exportRouletteStats()');
    console.log('�🗑️  Очистить данные: clearRouletteData()');
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
        
        // Ищем ПЕРВЫЙ дочерний элемент (самое последнее число)
        const firstChild = element.querySelector('div:first-child');
        
        if (!firstChild) {
            console.warn('⚠️ Не найден первый элемент истории');
            return;
        }
        
        // Берем только текст из первого элемента
        const allText = firstChild.innerText + ' ' + firstChild.innerHTML;
        const numbers = allText.match(/\b([0-9]|[1-2][0-9]|3[0-6])\b/g);
        
        if (!numbers || numbers.length === 0) {
            return;
        }
        
        // Берем только ПЕРВОЕ число (самое последнее выпавшее)
        const numStr = numbers[0];
        const num = parseInt(numStr);
        
        if (num < 0 || num > 36) {
            return;
        }
        
        // Проверяем что это НОВОЕ число (не добавляли его недавно)
        const isDuplicate = allResults.some(r => 
            r.number === num && 
            Math.abs(new Date(r.timestamp) - new Date()) < 10000  // 10 секунд
        );
        
        if (isDuplicate) {
            return; // Это число уже есть, не добавляем дубликат
        }
        
        // Определяем цвет
        const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
        const color = num === 0 ? 'green' : (reds.includes(num) ? 'red' : 'black');
        
        // Добавляем новый результат
        allResults.unshift({
            number: num,
            color: color,
            timestamp: new Date().toISOString(),
            table: "roulettestura541_only"
        });
        
        // Ограничиваем размер
        if (allResults.length > CONFIG.maxResults) {
            allResults = allResults.slice(0, CONFIG.maxResults);
        }
        
        // Сохраняем
        saveData();
        
        // Показываем новое число
        const emoji = color === 'red' ? '🔴' : color === 'black' ? '⚫' : '🟢';
        const time = new Date().toLocaleTimeString('ru-RU');
        
        console.log(time, emoji, num, '- Всего:', allResults.length, 'результатов (ТОЛЬКО ваша рулетка)');
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
    
    // Экспорт статистики в текстовом формате
    window.saveRouletteStats = function() {
        if (allResults.length === 0) {
            console.log('❌ Нет данных для статистики');
            return;
        }
        
        const colors = {red: 0, black: 0, green: 0};
        const numbers = {};
        let maxRedSeries = 0, maxBlackSeries = 0;
        let currentRedSeries = 0, currentBlackSeries = 0;
        
        allResults.forEach(r => {
            colors[r.color]++;
            numbers[r.number] = (numbers[r.number] || 0) + 1;
            
            // Подсчет серий
            if (r.color === 'red') {
                currentRedSeries++;
                currentBlackSeries = 0;
                maxRedSeries = Math.max(maxRedSeries, currentRedSeries);
            } else if (r.color === 'black') {
                currentBlackSeries++;
                currentRedSeries = 0;
                maxBlackSeries = Math.max(maxBlackSeries, currentBlackSeries);
            } else {
                currentRedSeries = 0;
                currentBlackSeries = 0;
            }
        });
        
        const total = allResults.length;
        const topNumbers = Object.entries(numbers)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);
        
        const statsText = `
╔══════════════════════════════════════════════════════════════╗
║          📊 СТАТИСТИКА РУЛЕТКИ roulettestura541           ║
╚══════════════════════════════════════════════════════════════╝

📅 Дата: ${new Date().toLocaleString('ru-RU')}
🎰 Всего спинов: ${total}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 РАСПРЕДЕЛЕНИЕ ЦВЕТОВ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Красные: ${colors.red} раз (${(colors.red/total*100).toFixed(2)}%)
⚫ Черные:  ${colors.black} раз (${(colors.black/total*100).toFixed(2)}%)
🟢 Зеленые: ${colors.green} раз (${(colors.green/total*100).toFixed(2)}%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 МАКСИМАЛЬНЫЕ СЕРИИ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Красных подряд: ${maxRedSeries}
⚫ Черных подряд:  ${maxBlackSeries}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 ТОП-10 САМЫХ ЧАСТЫХ ЧИСЕЛ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${topNumbers.map(([num, count], i) => {
    const n = parseInt(num);
    const reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36];
    const emoji = n === 0 ? '🟢' : (reds.includes(n) ? '🔴' : '⚫');
    const percent = (count/total*100).toFixed(2);
    return `${i+1}. ${emoji} ${num.padStart(2, ' ')} - ${count} раз (${percent}%)`;
}).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ПОСЛЕДНИЕ 20 СПИНОВ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${allResults.slice(0, 20).map(r => {
    const emoji = r.color === 'red' ? '🔴' : r.color === 'black' ? '⚫' : '🟢';
    const time = new Date(r.timestamp).toLocaleTimeString('ru-RU');
    return `${time} ${emoji} ${r.number}`;
}).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Для полного анализа стратегий запустите:
   py console_to_analysis.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`;
        
        console.log(statsText);
        
        // Копируем в буфер обмена
        navigator.clipboard.writeText(statsText)
            .then(() => {
                console.log('✅ Статистика скопирована в буфер обмена!');
                console.log('📝 Вставьте (Ctrl+V) в файл roulette_stats.txt');
            })
            .catch(() => console.log('⚠️ Скопируйте статистику выше вручную'));
        
        return statsText;
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
