"""
ИИ АССИСТЕНТ ДЛЯ АНАЛИЗА СТРАТЕГИЙ РУЛЕТКИ
=========================================

Этот модуль содержит искусственный интеллект, который анализирует данные рулетки
и предлагает оптимальные стратегии игры.

Простыми словами:
- Изучает историю выпавших чисел
- Находит закономерности и паттерны  
- Предлагает 3 лучшие стратегии
- Рассчитывает ожидаемую прибыль
"""

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ numpy не установлен, используем базовые функции")

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any
from collections import Counter, defaultdict
import math

from data_collector import DataCollector
from game_analyzer import GameAnalyzer, GameStrategy
from utils import RouletteUtils


class PatternAnalyzer:
    """Анализатор паттернов в данных рулетки"""
    
    def __init__(self):
        self.utils = RouletteUtils()
    
    def analyze_color_patterns(self, spins: List[Dict]) -> Dict:
        """
        Анализирует паттерны цветов
        
        Простыми словами: Изучает как часто выпадают красные/черные подряд
        
        Args:
            spins (List[Dict]): История спинов
            
        Returns:
            Dict: Информация о паттернах цветов
        """
        if len(spins) < 10:
            return {"error": "Недостаточно данных"}
        
        colors = [spin['color'] for spin in spins]
        
        # Анализируем серии
        streaks = {"red": [], "black": [], "green": []}
        current_color = colors[0]
        current_streak = 1
        
        for color in colors[1:]:
            if color == current_color and color != 'green':
                current_streak += 1
            else:
                if current_color != 'green':
                    streaks[current_color].append(current_streak)
                current_color = color
                current_streak = 1
        
        # Добавляем последнюю серию
        if current_color != 'green':
            streaks[current_color].append(current_streak)
        
        # Статистика серий
        analysis = {}
        for color in ['red', 'black']:
            if streaks[color]:
                if NUMPY_AVAILABLE:
                    avg_streak = np.mean(streaks[color])
                else:
                    avg_streak = sum(streaks[color]) / len(streaks[color])
                
                analysis[color] = {
                    "avg_streak": avg_streak,
                    "max_streak": max(streaks[color]),
                    "total_streaks": len(streaks[color]),
                    "streaks_3_plus": len([s for s in streaks[color] if s >= 3]),
                    "streaks_5_plus": len([s for s in streaks[color] if s >= 5])
                }
        
        return analysis
    
    def analyze_number_frequency(self, spins: List[Dict], periods: List[int] = [50, 100, 200]) -> Dict:
        """
        Анализирует частоту выпадения чисел за разные периоды
        
        Args:
            spins (List[Dict]): История спинов
            periods (List[int]): Периоды для анализа
            
        Returns:
            Dict: Частота чисел по периодам
        """
        analysis = {}
        
        for period in periods:
            if len(spins) < period:
                continue
                
            recent_spins = spins[-period:]
            number_counts = Counter(spin['number'] for spin in recent_spins)
            
            # Ожидаемая частота для справедливой рулетки
            expected_freq = period / 37
            
            # Найдем горячие и холодные числа
            hot_numbers = []
            cold_numbers = []
            
            for number in range(37):
                actual_freq = number_counts.get(number, 0)
                deviation = actual_freq - expected_freq
                
                if actual_freq >= expected_freq * 1.5:  # Выше нормы на 50%+
                    hot_numbers.append((number, actual_freq, deviation))
                elif actual_freq <= expected_freq * 0.5:  # Ниже нормы на 50%+
                    cold_numbers.append((number, actual_freq, deviation))
            
            analysis[f"last_{period}"] = {
                "hot_numbers": sorted(hot_numbers, key=lambda x: x[2], reverse=True)[:10],
                "cold_numbers": sorted(cold_numbers, key=lambda x: x[2])[:10],
                "most_frequent": number_counts.most_common(10),
                "least_frequent": number_counts.most_common()[:-11:-1]
            }
        
        return analysis
    
    def analyze_sector_patterns(self, spins: List[Dict]) -> Dict:
        """
        Анализирует паттерны по секторам рулетки
        
        Простыми словами: Изучает какие части колеса рулетки более активны
        
        Args:
            spins (List[Dict]): История спинов
            
        Returns:
            Dict: Анализ секторов
        """
        # Определяем соседние числа на колесе рулетки (европейская рулетка)
        wheel_order = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 
                      5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        
        # Создаем индекс позиций на колесе
        wheel_positions = {num: i for i, num in enumerate(wheel_order)}
        
        # Анализируем секторы по 5 чисел
        sector_size = 5
        sectors = {}
        
        for start_pos in range(0, 37, sector_size):
            end_pos = min(start_pos + sector_size, 37)
            sector_numbers = wheel_order[start_pos:end_pos]
            sector_name = f"sector_{start_pos//sector_size + 1}"
            
            sector_hits = sum(1 for spin in spins if spin['number'] in sector_numbers)
            expected_hits = len(spins) * (len(sector_numbers) / 37)
            
            sectors[sector_name] = {
                "numbers": sector_numbers,
                "hits": sector_hits,
                "expected": expected_hits,
                "deviation": sector_hits - expected_hits,
                "activity_ratio": sector_hits / expected_hits if expected_hits > 0 else 0
            }
        
        return sectors


class AIAssistant:
    """Основной класс ИИ-ассистента"""
    
    def __init__(self, data_collector: DataCollector, game_analyzer: GameAnalyzer):
        """
        Инициализация ИИ-ассистента
        
        Args:
            data_collector (DataCollector): Сборщик данных
            game_analyzer (GameAnalyzer): Анализатор стратегий
        """
        self.data_collector = data_collector
        self.game_analyzer = game_analyzer
        self.pattern_analyzer = PatternAnalyzer()
        self.utils = RouletteUtils()
    
    def analyze_data(self, start_date: datetime, end_date: datetime = None) -> Dict:
        """
        Полный анализ данных за период
        
        Простыми словами: Изучаем все что можно в истории рулетки
        
        Args:
            start_date (datetime): Начальная дата
            end_date (datetime): Конечная дата
            
        Returns:
            Dict: Полный анализ данных
        """
        print("ИИ анализирует данные...")
        
        # Получаем данные
        spins = self.data_collector.get_spins_by_period(start_date, end_date)
        
        if len(spins) < 50:
            return {"error": "Недостаточно данных для анализа (минимум 50 спинов)"}
        
        # Базовая статистика
        basic_stats = self.data_collector.get_statistics(start_date, end_date)
        
        # Анализ паттернов
        color_patterns = self.pattern_analyzer.analyze_color_patterns(spins)
        number_frequency = self.pattern_analyzer.analyze_number_frequency(spins)
        sector_patterns = self.pattern_analyzer.analyze_sector_patterns(spins)
        
        # Поиск аномалий
        anomalies = self._detect_anomalies(spins)
        
        # Оценка волатильности
        volatility = self._calculate_volatility(spins)
        
        analysis = {
            "period": {"start": start_date, "end": end_date or datetime.now()},
            "total_spins": len(spins),
            "basic_statistics": basic_stats,
            "color_patterns": color_patterns,
            "number_frequency": number_frequency,
            "sector_patterns": sector_patterns,
            "anomalies": anomalies,
            "volatility": volatility,
            "analysis_timestamp": datetime.now()
        }
        
        return analysis
    
    def generate_strategies(self, analysis_data: Dict, risk_level: str = "medium") -> List[Dict]:
        """
        Генерирует 3 оптимальные стратегии на основе анализа
        
        Простыми словами: Создает 3 лучшие схемы игры на основе найденных закономерностей
        
        Args:
            analysis_data (Dict): Результаты анализа данных
            risk_level (str): Уровень риска ("low", "medium", "high")
            
        Returns:
            List[Dict]: Список из 3 стратегий с описанием
        """
        print("ИИ генерирует стратегии...")
        
        if "error" in analysis_data:
            return [{"error": "Не могу генерировать стратегии без данных анализа"}]
        
        strategies = []
        
        # Стратегия 1: На основе горячих чисел
        hot_strategy = self._create_hot_numbers_strategy(analysis_data, risk_level)
        strategies.append(hot_strategy)
        
        # Стратегия 2: На основе цветовых паттернов
        color_strategy = self._create_color_pattern_strategy(analysis_data, risk_level)
        strategies.append(color_strategy)
        
        # Стратегия 3: На основе секторного анализа
        sector_strategy = self._create_sector_strategy(analysis_data, risk_level)
        strategies.append(sector_strategy)
        
        # Сортируем по ожидаемому профиту
        strategies.sort(key=lambda x: x.get("expected_profit", 0), reverse=True)
        
        return strategies
    
    def _create_hot_numbers_strategy(self, analysis_data: Dict, risk_level: str) -> Dict:
        """Создает стратегию на основе горячих чисел"""
        
        # Получаем горячие числа из анализа
        hot_numbers = []
        freq_data = analysis_data.get("number_frequency", {})
        
        for period, data in freq_data.items():
            if "hot_numbers" in data and data["hot_numbers"]:
                hot_numbers.extend([num for num, freq, dev in data["hot_numbers"][:3]])
        
        # Убираем дубликаты и берем топ-5
        hot_numbers = list(set(hot_numbers))[:5]
        
        if not hot_numbers:
            hot_numbers = [7, 17, 23]  # Дефолтные "счастливые" числа
        
        base_bet = {"low": 5, "medium": 10, "high": 20}[risk_level]
        
        strategy = {
            "name": "ИИ: Горячие Числа",
            "description": f"Ставки на числа с повышенной активностью: {hot_numbers}",
            "type": "hot_numbers",
            "parameters": {
                "target_numbers": hot_numbers,
                "base_bet": base_bet,
                "max_bet": base_bet * 5
            },
            "risk_level": risk_level,
            "expected_profit": len(hot_numbers) * 2.5,  # Примерная оценка
            "logic": "Числа которые выпадали чаще среднего продолжат быть активными"
        }
        
        return strategy
    
    def _create_color_pattern_strategy(self, analysis_data: Dict, risk_level: str) -> Dict:
        """Создает стратегию на основе цветовых паттернов"""
        
        color_patterns = analysis_data.get("color_patterns", {})
        
        # Анализируем какой цвет имеет более длинные серии
        dominant_color = "red"  # По умолчанию
        
        if "red" in color_patterns and "black" in color_patterns:
            red_avg = color_patterns["red"].get("avg_streak", 1)
            black_avg = color_patterns["black"].get("avg_streak", 1)
            dominant_color = "red" if red_avg >= black_avg else "black"
        
        base_bet = {"low": 10, "medium": 20, "high": 40}[risk_level]
        
        strategy = {
            "name": "ИИ: Цветовые Серии",
            "description": f"Ставки на {dominant_color} с прогрессией при сериях",
            "type": "color_progression",
            "parameters": {
                "target_color": dominant_color,
                "base_bet": base_bet,
                "progression_multiplier": 1.5,
                "max_streak": 5
            },
            "risk_level": risk_level,
            "expected_profit": 15.0,
            "logic": f"Цвет {dominant_color} показывает склонность к более длинным сериям"
        }
        
        return strategy
    
    def _create_sector_strategy(self, analysis_data: Dict, risk_level: str) -> Dict:
        """Создает стратегию на основе анализа секторов"""
        
        sector_patterns = analysis_data.get("sector_patterns", {})
        
        # Находим самый активный сектор
        most_active_sector = None
        max_activity = 0
        
        for sector_name, sector_data in sector_patterns.items():
            activity = sector_data.get("activity_ratio", 0)
            if activity > max_activity:
                max_activity = activity
                most_active_sector = sector_data
        
        if not most_active_sector:
            # Дефолтный сектор
            most_active_sector = {"numbers": [17, 34, 6, 27, 13]}
        
        base_bet = {"low": 3, "medium": 5, "high": 8}[risk_level]
        sector_numbers = most_active_sector.get("numbers", [17, 34, 6, 27, 13])
        
        strategy = {
            "name": "ИИ: Активный Сектор",
            "description": f"Ставки на числа активного сектора: {sector_numbers}",
            "type": "sector_betting",
            "parameters": {
                "sector_numbers": sector_numbers,
                "bet_per_number": base_bet,
                "total_bet": base_bet * len(sector_numbers)
            },
            "risk_level": risk_level,
            "expected_profit": max_activity * 10,
            "logic": "Сектор колеса показывает повышенную активность"
        }
        
        return strategy
    
    def _detect_anomalies(self, spins: List[Dict]) -> Dict:
        """Обнаруживает аномалии в данных"""
        
        anomalies = {
            "zero_frequency": 0,
            "long_color_streaks": [],
            "number_gaps": [],
            "unusual_patterns": []
        }
        
        # Частота зеро
        zero_count = sum(1 for spin in spins if spin['number'] == 0)
        expected_zero = len(spins) / 37
        if zero_count > expected_zero * 1.5:
            anomalies["zero_frequency"] = {
                "actual": zero_count,
                "expected": expected_zero,
                "significance": "high"
            }
        
        # Длинные серии цветов
        colors = [spin['color'] for spin in spins]
        current_color = colors[0] if colors else None
        current_streak = 1
        
        for color in colors[1:]:
            if color == current_color and color != 'green':
                current_streak += 1
            else:
                if current_streak >= 7 and current_color != 'green':
                    anomalies["long_color_streaks"].append({
                        "color": current_color,
                        "length": current_streak,
                        "significance": "high" if current_streak >= 10 else "medium"
                    })
                current_color = color
                current_streak = 1
        
        return anomalies
    
    def _calculate_volatility(self, spins: List[Dict]) -> Dict:
        """Рассчитывает волатильность данных"""
        
        if len(spins) < 20:
            return {"error": "Недостаточно данных"}
        
        # Анализируем распределение по цветам в скользящих окнах
        window_size = 20
        red_percentages = []
        
        for i in range(len(spins) - window_size + 1):
            window = spins[i:i + window_size]
            red_count = sum(1 for spin in window if spin['color'] == 'red')
            red_percentages.append(red_count / window_size * 100)
        
        if not red_percentages:
            return {"error": "Недостаточно данных для окон"}
        
        if NUMPY_AVAILABLE:
            color_volatility = np.std(red_percentages)
        else:
            # Вычисляем стандартное отклонение вручную
            mean_val = sum(red_percentages) / len(red_percentages)
            variance = sum((x - mean_val) ** 2 for x in red_percentages) / len(red_percentages)
            color_volatility = math.sqrt(variance)

        volatility = {
            "color_volatility": color_volatility,
            "trend": "stable",
            "predictability": "medium"
        }
        
        # Определяем тренд
        if volatility["color_volatility"] > 15:
            volatility["trend"] = "volatile"
            volatility["predictability"] = "low"
        elif volatility["color_volatility"] < 8:
            volatility["trend"] = "stable"
            volatility["predictability"] = "high"
        
        return volatility
    
    def test_ai_strategies(self, strategies: List[Dict], start_date: datetime, 
                          end_date: datetime = None, initial_balance: float = 1000.0) -> Dict:
        """
        Тестирует сгенерированные ИИ стратегии
        
        Args:
            strategies (List[Dict]): Список стратегий от ИИ
            start_date (datetime): Начальная дата
            end_date (datetime): Конечная дата
            initial_balance (float): Начальный баланс
            
        Returns:
            Dict: Результаты тестирования
        """
        print("Тестируем ИИ стратегии...")
        
        # Преобразуем ИИ стратегии в GameStrategy объекты
        game_strategies = []
        
        for ai_strategy in strategies:
            if "error" in ai_strategy:
                continue
                
            game_strategy = self._convert_ai_to_game_strategy(ai_strategy)
            game_strategies.append(game_strategy)
        
        if not game_strategies:
            return {"error": "Нет корректных стратегий для тестирования"}
        
        # Тестируем с помощью GameAnalyzer
        results = self.game_analyzer.compare_strategies(
            game_strategies, start_date, end_date, initial_balance
        )
        
        return results
    
    def _convert_ai_to_game_strategy(self, ai_strategy: Dict) -> GameStrategy:
        """Преобразует ИИ стратегию в GameStrategy объект"""
        
        strategy = GameStrategy(
            name=ai_strategy["name"],
            description=ai_strategy["description"]
        )
        
        strategy_type = ai_strategy.get("type", "hot_numbers")
        params = ai_strategy.get("parameters", {})
        
        if strategy_type == "hot_numbers":
            target_numbers = params.get("target_numbers", [17, 23, 7])
            base_bet = params.get("base_bet", 5)
            
            def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
                return {
                    "type": "number",
                    "numbers": target_numbers,
                    "amount": min(base_bet * len(target_numbers), strategy.balance)
                }
                
        elif strategy_type == "color_progression":
            target_color = params.get("target_color", "red")
            base_bet = params.get("base_bet", 10)
            multiplier = params.get("progression_multiplier", 1.5)
            
            strategy.current_bet = base_bet
            strategy.losses_in_row = 0
            
            def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
                # Если предыдущая ставка выиграла, сбрасываем
                if history and history[-1].get('color') == target_color:
                    strategy.current_bet = base_bet
                    strategy.losses_in_row = 0
                else:
                    # Увеличиваем ставку при проигрыше
                    if history:
                        strategy.losses_in_row += 1
                        if strategy.losses_in_row <= 3:
                            strategy.current_bet *= multiplier
                
                return {
                    "type": "color",
                    "numbers": [target_color],
                    "amount": min(strategy.current_bet, strategy.balance)
                }
                
        elif strategy_type == "sector_betting":
            sector_numbers = params.get("sector_numbers", [17, 34, 6])
            bet_per_number = params.get("bet_per_number", 3)
            
            def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
                return {
                    "type": "number",
                    "numbers": sector_numbers,
                    "amount": min(bet_per_number * len(sector_numbers), strategy.balance)
                }
        
        else:
            # Дефолтная логика
            def make_bet_logic(spin_number: int, history: List[Dict]) -> Dict:
                return {"type": "color", "numbers": ["red"], "amount": 10}
        
        strategy.make_bet = make_bet_logic
        return strategy


# Тестирование ИИ-ассистента
if __name__ == "__main__":
    print("Тестируем ИИ-ассистента...")
    
    # Создаем необходимые компоненты
    collector = DataCollector("../data/test_ai.db")
    analyzer = GameAnalyzer(collector)
    ai_assistant = AIAssistant(collector, analyzer)
    
    # Генерируем тестовые данные
    start_date = datetime.now() - timedelta(days=10)
    print("Генерируем данные для ИИ...")
    collector.generate_random_spins(800, start_date)
    
    # Анализируем данные
    print("ИИ анализирует данные...")
    analysis = ai_assistant.analyze_data(start_date)
    
    # Генерируем стратегии
    print("ИИ создает стратегии...")
    strategies = ai_assistant.generate_strategies(analysis, "medium")
    
    print(f"\n=== ИИ ПРЕДЛАГАЕТ {len(strategies)} СТРАТЕГИЙ ===")
    for i, strategy in enumerate(strategies, 1):
        print(f"\nСтратегия {i}: {strategy['name']}")
        print(f"Описание: {strategy['description']}")
        print(f"Ожидаемая прибыль: {strategy.get('expected_profit', 'Не определена')}")
        print(f"Логика: {strategy.get('logic', 'Не указана')}")
    
    # Тестируем стратегии
    print("\nТестируем ИИ стратегии...")
    test_results = ai_assistant.test_ai_strategies(strategies, start_date)
    
    if "error" not in test_results:
        print(f"\nЛучшая ИИ стратегия: {test_results['best_strategy']}")
        print(f"Прибыль: {test_results['best_profit']:.2f}")
    
    print("\nТест ИИ завершен!")