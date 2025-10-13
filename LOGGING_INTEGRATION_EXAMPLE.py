"""
📊 RULETTT - Пример Интеграции Логирования
==========================================

Показывает как интегрировать систему логирования в существующие модули
"""

# ============ ВАРИАНТ 1: Базовая интеграция ============

from src.logger import main_logger, log_execution_time, log_function_call
from src.error_tracker import error_tracker, track_exception_decorator

# Пример 1: Простое логирование
def simple_function():
    main_logger.info("🎲 Функция начала работу")
    result = 42
    main_logger.debug(f"Результат вычисления: {result}")
    return result

# Пример 2: Логирование с замером времени выполнения
@log_execution_time(main_logger)
def slow_operation():
    """Операция с автоматическим замером времени"""
    import time
    time.sleep(0.5)
    return "completed"

# Пример 3: Автоматическое логирование вызовов функции
@log_function_call(main_logger, log_args=True)
def calculate_something(x, y, operation="add"):
    """Функция с автоматическим логированием аргументов"""
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y
    return 0

# Пример 4: Отслеживание ошибок с контекстом
@track_exception_decorator
def risky_operation(value):
    """Функция с автоматическим отслеживанием ошибок"""
    if value < 0:
        raise ValueError("Значение должно быть положительным")
    return value * 2

# ============ ВАРИАНТ 2: Интеграция в API роуты ============

"""
В api_server.py добавьте:

from src.logger import api_logger, log_execution_time
from src.error_tracker import error_tracker, action_tracker

@app.route('/api/spins', methods=['POST'])
@log_execution_time(api_logger)
def add_spin():
    try:
        data = request.get_json()
        
        # Логируем действие пользователя
        action_tracker.track_action(
            action_type='api_call',
            details={
                'endpoint': '/api/spins',
                'method': 'POST',
                'data': data
            }
        )
        
        # Ваш код обработки...
        result = api.add_spin(data)
        
        api_logger.info(f"✅ Спин добавлен: {data.get('number')}")
        return jsonify(result)
        
    except Exception as e:
        # Автоматически логируем ошибку с контекстом
        error_tracker.track_error(
            error=e,
            context={'endpoint': '/api/spins', 'data': data}
        )
        api_logger.error(f"❌ Ошибка добавления спина: {str(e)}")
        return jsonify({'error': str(e)}), 500
"""

# ============ ВАРИАНТ 3: Интеграция в HTML ============

"""
В каждую HTML страницу добавьте перед </body>:

<!-- Event Tracker -->
<script src="event-tracker.js"></script>
<script>
    // Трекер автоматически инициализируется
    
    // Можно добавить кастомные события:
    window.roulettTracker.trackCustomEvent('page_loaded', {
        page: 'dashboard',
        user_id: getCurrentUserId()
    });
    
    // Отслеживание кнопок:
    document.getElementById('myButton').addEventListener('click', () => {
        window.roulettTracker.trackButtonClick({
            button: 'myButton',
            action: 'start_game'
        });
    });
    
    // Отслеживание форм:
    document.getElementById('myForm').addEventListener('submit', (e) => {
        window.roulettTracker.trackFormSubmit({
            form: 'login',
            fields: ['username', 'password']
        });
    });
</script>
"""

# ============ ВАРИАНТ 4: Интеграция в DataCollector ============

"""
В src/data_collector.py добавьте:

from logger import collector_logger, log_execution_time
from error_tracker import track_exception_decorator

class DataCollector:
    
    @log_execution_time(collector_logger)
    def save_spin(self, number: int, color: str):
        '''Сохранение спина с логированием времени'''
        collector_logger.debug(f"Сохраняем спин: {number} ({color})")
        
        try:
            # Ваш код сохранения
            result = self._save_to_db(number, color)
            collector_logger.info(f"✅ Спин сохранён: {number}")
            return result
            
        except Exception as e:
            collector_logger.error(f"❌ Ошибка сохранения: {str(e)}")
            raise
    
    @track_exception_decorator
    def generate_test_data(self, num_spins=500):
        '''Генерация тестовых данных с отслеживанием ошибок'''
        collector_logger.info(f"🎲 Генерируем {num_spins} тестовых спинов")
        
        for i in range(num_spins):
            number = self._generate_random_number()
            self.save_spin(number, self._get_color(number))
            
            if i % 100 == 0:
                collector_logger.debug(f"Прогресс: {i}/{num_spins}")
        
        collector_logger.info("✅ Генерация завершена")
"""

# ============ ВАРИАНТ 5: Интеграция в GameAnalyzer ============

"""
В src/game_analyzer.py добавьте:

from logger import analyzer_logger, log_execution_time
from error_tracker import error_tracker, action_tracker

class GameAnalyzer:
    
    @log_execution_time(analyzer_logger)
    def test_strategy(self, strategy, spins):
        '''Тестирование стратегии с логированием'''
        analyzer_logger.info(f"🎯 Тестируем стратегию: {strategy.name}")
        
        # Логируем начало тестирования
        action_tracker.track_action(
            action_type='strategy_test_start',
            details={
                'strategy': strategy.name,
                'num_spins': len(spins)
            }
        )
        
        try:
            result = strategy.backtest(spins)
            
            analyzer_logger.info(
                f"✅ Тест завершён: Прибыль={result.profit}, "
                f"Винрейт={result.winrate}%"
            )
            
            # Логируем результат
            action_tracker.track_action(
                action_type='strategy_test_complete',
                details={
                    'strategy': strategy.name,
                    'profit': result.profit,
                    'winrate': result.winrate
                }
            )
            
            return result
            
        except Exception as e:
            analyzer_logger.error(f"❌ Ошибка тестирования: {str(e)}")
            error_tracker.track_error(e, context={
                'strategy': strategy.name,
                'num_spins': len(spins)
            })
            raise
"""

# ============ ВАРИАНТ 6: Контекстное логирование ============

from src.logger import LoggerContext, main_logger

def process_user_request(user_id, session_id, request_data):
    """Логирование с контекстом пользователя"""
    
    # Создаём контекст для всех логов в этой функции
    with LoggerContext(main_logger, user_id=user_id, session_id=session_id):
        main_logger.info("🔵 Начинаем обработку запроса")
        
        try:
            # Обрабатываем данные
            result = process_data(request_data)
            
            main_logger.info(f"✅ Запрос обработан успешно")
            return result
            
        except Exception as e:
            # Контекст автоматически добавляется к логам ошибок
            main_logger.error(f"❌ Ошибка обработки: {str(e)}")
            raise

def process_data(data):
    """Вложенная функция - контекст наследуется"""
    main_logger.debug(f"Обрабатываем данные: {len(data)} элементов")
    return {"status": "ok", "count": len(data)}

# ============ ТЕСТИРОВАНИЕ ============

if __name__ == "__main__":
    print("📊 Тестирование интеграции логирования\n")
    
    # Тест 1: Простое логирование
    print("1️⃣ Простое логирование:")
    simple_function()
    
    # Тест 2: Замер времени
    print("\n2️⃣ Замер времени выполнения:")
    result = slow_operation()
    print(f"Результат: {result}")
    
    # Тест 3: Логирование аргументов
    print("\n3️⃣ Логирование аргументов:")
    result = calculate_something(10, 5, operation="multiply")
    print(f"Результат: {result}")
    
    # Тест 4: Отслеживание ошибок
    print("\n4️⃣ Отслеживание ошибок:")
    try:
        risky_operation(-5)
    except ValueError as e:
        print(f"Ошибка перехвачена: {e}")
    
    # Тест 5: Контекстное логирование
    print("\n5️⃣ Контекстное логирование:")
    process_user_request(
        user_id="user123",
        session_id="session456",
        request_data={"action": "test"}
    )
    
    print("\n✅ Все тесты пройдены!")
    print("\n📁 Логи сохранены в директорию: logs/")
    print("🗄️ Ошибки записаны в БД: data/errors.db")
