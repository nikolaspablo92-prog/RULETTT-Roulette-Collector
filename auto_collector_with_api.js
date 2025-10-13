// ============================================
// 🎰 АВТОМАТИЧЕСКИЙ СБОРЩИК С ОТПРАВКОЙ НА API
// ============================================
// Этот коллектор отправляет данные НАПРЯМУЮ на сервер
// без необходимости экспорта JSON файлов

(function() {
    // Конфигурация
    const CONFIG = {
        // ⚠️ ВАЖНО: Измените этот селектор под ваше казино!
        selector: ".game-area__history-line--Lkj9A",
        
        // URL вашего API сервера
        apiUrl: "http://localhost:5000/api/spins",
        
        // Интервалы
        updateInterval: 30000,  // 30 секунд - проверка новых спинов
        maxResults: 100,        // Максимум в localStorage
        
        // Автоотправка на API
        autoSendToAPI: true,    // true = отправлять автоматически
        
        // Название казино/стола
        casinoName: "live_casino", // Измените на название вашего казино
        tableName: "auto_roulette_1", // Название стола
        
        // localStorage
        storageKey: "rouletteData"
    };
    
    // Хранилище данных
    let allResults = [];
    let lastCheck = null;
    let sentCount = 0;
    let failedCount = 0;
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎰 АВТОМАТИЧЕСКИЙ СБОРЩИК С API ЗАПУЩЕН!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🌐 API URL:', CONFIG.apiUrl);
    console.log('🎲 Казино:', CONFIG.casinoName);
    console.log('🎯 Стол:', CONFIG.tableName);
    console.log('⏰ Обновление каждые', CONFIG.updateInterval / 1000, 'секунд');
    console.log('📡 Автоотправка на API:', CONFIG.autoSendToAPI ? 'ВКЛ ✅' : 'ВЫКЛ ❌');
    console.log('');
    console.log('📋 КОМАНДЫ:');
    console.log('  stopRouletteCollector()  - Остановить сборщик');
    console.log('  showRouletteStats()      - Показать статистику');
    console.log('  sendAllToAPI()           - Отправить все на API');
    console.log('  clearRouletteData()      - Очистить данные');
    console.log('  getAPIStatus()           - Проверить связь с API');
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
    
    // Отправка на API
    async function sendToAPI(spinData) {
        try {
            const payload = {
                number: spinData.number,
                color: spinData.color,
                timestamp: spinData.timestamp,
                casino_name: CONFIG.casinoName,
                table_name: CONFIG.tableName,
                source: "browser_console_auto"
            };
            
            const response = await fetch(CONFIG.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                sentCount++;
                console.log('✅ Отправлено на API:', spinData.number, `(${spinData.color})`, '| Всего отправлено:', sentCount);
                return true;
            } else {
                failedCount++;
                console.warn('⚠️ API ответил с ошибкой:', response.status, response.statusText);
                return false;
            }
        } catch (error) {
            failedCount++;
            console.error('❌ Ошибка отправки на API:', error.message);
            console.log('💡 Проверьте: 1) Запущен ли API сервер, 2) Правильный ли URL');
            return false;
        }
    }
    
    // Функция сбора данных
    async function collectData() {
        const element = document.querySelector(CONFIG.selector);
        
        if (!element) {
            console.warn('⚠️ Элемент рулетки не найден. Селектор:', CONFIG.selector);
            console.log('💡 Инструкция: Правый клик на историю → Inspect → Copy selector');
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
        
        // Создаем запись
        const spinData = {
            number: num,
            color: color,
            timestamp: new Date().toISOString(),
            casino: CONFIG.casinoName,
            table: CONFIG.tableName
        };
        
        // Добавляем новый результат
        allResults.unshift(spinData);
        
        // Ограничиваем размер
        if (allResults.length > CONFIG.maxResults) {
            allResults = allResults.slice(0, CONFIG.maxResults);
        }
        
        // Сохраняем в localStorage
        saveData();
        
        // Показываем новое число
        const emoji = color === 'red' ? '🔴' : color === 'black' ? '⚫' : '🟢';
        const time = new Date().toLocaleTimeString('ru-RU');
        
        console.log(time, emoji, num, '| Локально:', allResults.length);
        
        // Отправляем на API если включено
        if (CONFIG.autoSendToAPI) {
            await sendToAPI(spinData);
        }
    }
    
    // Проверка связи с API
    window.getAPIStatus = async function() {
        console.log('🔍 Проверка связи с API...');
        try {
            const response = await fetch(CONFIG.apiUrl.replace('/spins', '/health'));
            if (response.ok) {
                const data = await response.json();
                console.log('✅ API доступен:', data);
                return true;
            } else {
                console.warn('⚠️ API вернул ошибку:', response.status);
                return false;
            }
        } catch (error) {
            console.error('❌ API недоступен:', error.message);
            console.log('💡 Убедитесь что запущен: py api_server.py');
            return false;
        }
    };
    
    // Отправить все данные на API
    window.sendAllToAPI = async function() {
        if (allResults.length === 0) {
            console.log('❌ Нет данных для отправки');
            return;
        }
        
        console.log('📤 Отправка', allResults.length, 'спинов на API...');
        
        let success = 0;
        let failed = 0;
        
        for (let i = 0; i < allResults.length; i++) {
            const spin = allResults[i];
            const sent = await sendToAPI(spin);
            if (sent) {
                success++;
            } else {
                failed++;
            }
            
            // Небольшая задержка между запросами
            if (i < allResults.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📊 РЕЗУЛЬТАТ МАССОВОЙ ОТПРАВКИ:');
        console.log('  ✅ Успешно:', success);
        console.log('  ❌ Ошибок:', failed);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
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
        console.log('📡 Отправлено на API:', sentCount);
        console.log('❌ Ошибок отправки:', failedCount);
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
            console.log(`  ${i+1}. ${emoji} ${num}: ${count} раз (${(count/total*100).toFixed(1)}%)`);
        });
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    };
    
    // Очистить данные
    window.clearRouletteData = function() {
        const confirmed = confirm('Вы уверены? Все данные будут удалены!');
        if (!confirmed) return;
        
        allResults = [];
        sentCount = 0;
        failedCount = 0;
        localStorage.removeItem(CONFIG.storageKey);
        console.log('🗑️ Данные очищены');
    };
    
    // Остановить сборщик
    window.stopRouletteCollector = function() {
        if (window.rouletteCollectorInterval) {
            clearInterval(window.rouletteCollectorInterval);
            console.log('⏹️ Сборщик данных остановлен');
            console.log('');
            console.log('📊 ИТОГОВАЯ СТАТИСТИКА:');
            console.log('  🎰 Собрано результатов:', allResults.length);
            console.log('  ✅ Отправлено на API:', sentCount);
            console.log('  ❌ Ошибок отправки:', failedCount);
            console.log('');
            console.log('💡 Для повторной отправки: sendAllToAPI()');
        }
    };
    
    // Экспорт в JSON (на случай если API недоступен)
    window.exportRouletteData = function() {
        const jsonData = JSON.stringify(allResults, null, 2);
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 ЭКСПОРТ ДАННЫХ (РЕЗЕРВНАЯ КОПИЯ)');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📊 Всего результатов:', allResults.length);
        console.log('');
        console.log(jsonData);
        console.log('');
        
        // Копируем в буфер
        navigator.clipboard.writeText(jsonData)
            .then(() => {
                console.log('✅ Данные скопированы в буфер обмена!');
                console.log('💡 Сохраните в файл: roulette_console_data.json');
            })
            .catch(() => console.log('⚠️ Скопируйте JSON выше вручную'));
        
        return allResults;
    };
    
    // Загружаем сохраненные данные
    loadSavedData();
    
    // Проверяем связь с API
    getAPIStatus();
    
    // Первый сбор
    collectData();
    
    // Запускаем автоматический сбор
    window.rouletteCollectorInterval = setInterval(collectData, CONFIG.updateInterval);
    
    console.log('✅ Сборщик активен! Данные обновляются и отправляются автоматически...');
    console.log('');
    
})();

// ============================================
// 🎯 ГОТОВО! СБОРЩИК С API РАБОТАЕТ!
// ============================================
