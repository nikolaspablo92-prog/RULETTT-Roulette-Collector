"""
🤖 Бот-симулятор человеческого поведения
Эмуляция естественных действий пользователя для обхода anti-bot систем
"""

import random
import time
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import math


class HumanBehaviorSimulator:
    """Симулятор человеческого поведения"""
    
    # Конфигурация паттернов поведения
    CONFIG = {
        "delays": {
            "min_action": 0.5,          # Минимальная задержка между действиями (сек)
            "max_action": 3.5,          # Максимальная задержка между действиями (сек)
            "thinking_mean": 0.8,       # Среднее время "раздумий" (сек)
            "thinking_stddev": 0.3,     # Стандартное отклонение времени раздумий
            "reading_per_word": 0.15,   # Время чтения одного слова (сек)
        },
        "mouse": {
            "move_steps": (20, 40),     # Количество шагов при движении мыши
            "jitter_range": (-2, 2),    # Диапазон микро-дрожания (пиксели)
            "step_delay": (0.01, 0.03), # Задержка между шагами (сек)
            "overshoot_chance": 0.15,   # Вероятность промахнуться и скорректировать
            "curve_factor": 0.3,        # Фактор изгиба траектории (0-1)
        },
        "scroll": {
            "speed_range": (100, 300),  # Скорость прокрутки (пикс/сек)
            "pause_chance": 0.3,        # Вероятность остановки для "чтения"
            "pause_duration": (1, 4),   # Длительность паузы (сек)
            "back_scroll_chance": 0.15, # Вероятность прокрутить назад
            "momentum": 0.8,            # Инерция прокрутки (0-1)
        },
        "click": {
            "hover_before": 0.7,        # Вероятность навести курсор перед кликом
            "hover_duration": (0.3, 1.5),# Длительность наведения (сек)
            "double_check": 0.3,        # Вероятность навести курсор дважды
            "miss_rate": 0.05,          # Вероятность промаха
            "miss_correction": (0.1, 0.3),# Время на коррекцию промаха (сек)
        },
        "typing": {
            "wpm_range": (40, 80),      # Слова в минуту
            "typo_rate": 0.03,          # Вероятность опечатки
            "typo_correction_delay": (0.2, 0.5),  # Задержка перед исправлением
            "pause_on_punctuation": True,  # Пауза на знаках препинания
            "punctuation_pause": (0.2, 0.5),  # Длительность паузы
        }
    }
    
    def __init__(self, config: Dict = None):
        """
        Инициализация симулятора
        
        Args:
            config: Пользовательская конфигурация (перезапишет значения по умолчанию)
        """
        if config:
            self._update_config(config)
        
        self.action_history = []
        self.session_start = datetime.now()
        
        print("✅ Симулятор человеческого поведения инициализирован")
    
    def _update_config(self, config: Dict):
        """Обновление конфигурации"""
        for category, settings in config.items():
            if category in self.CONFIG:
                self.CONFIG[category].update(settings)
    
    # ============================================
    # ВРЕМЕННЫЕ ЗАДЕРЖКИ
    # ============================================
    
    def human_delay(self, base_delay: float = None) -> float:
        """
        Генерация человекоподобной задержки
        
        Args:
            base_delay: Базовая задержка (если None, используется случайная)
        
        Returns:
            Время задержки в секундах
        """
        if base_delay is None:
            base_delay = random.uniform(
                self.CONFIG["delays"]["min_action"],
                self.CONFIG["delays"]["max_action"]
            )
        
        # Добавляем "раздумья" с нормальным распределением
        thinking_delay = random.gauss(
            self.CONFIG["delays"]["thinking_mean"],
            self.CONFIG["delays"]["thinking_stddev"]
        )
        
        total_delay = max(0.1, base_delay + thinking_delay)
        return total_delay
    
    def reading_delay(self, text: str) -> float:
        """
        Задержка для "чтения" текста
        
        Args:
            text: Текст для чтения
        
        Returns:
            Время чтения в секундах
        """
        word_count = len(text.split())
        reading_time = word_count * self.CONFIG["delays"]["reading_per_word"]
        
        # Добавляем вариативность (некоторые читают быстрее/медленнее)
        variance = random.uniform(0.8, 1.3)
        return reading_time * variance
    
    async def wait_human(self, delay: float = None):
        """
        Асинхронная человекоподобная задержка
        
        Args:
            delay: Задержка в секундах (если None, генерируется автоматически)
        """
        if delay is None:
            delay = self.human_delay()
        
        await asyncio.sleep(delay)
    
    # ============================================
    # ДВИЖЕНИЕ МЫШИ
    # ============================================
    
    def bezier_curve(self, start: Tuple[float, float], 
                    end: Tuple[float, float], 
                    control: Tuple[float, float], 
                    t: float) -> Tuple[float, float]:
        """
        Квадратичная кривая Безье для плавного движения
        
        Args:
            start: Начальная точка (x, y)
            end: Конечная точка (x, y)
            control: Контрольная точка (x, y)
            t: Параметр кривой (0-1)
        
        Returns:
            Координаты точки на кривой
        """
        x = (1 - t)**2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0]
        y = (1 - t)**2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]
        return (x, y)
    
    def generate_mouse_path(self, start_x: float, start_y: float, 
                           end_x: float, end_y: float) -> List[Tuple[float, float]]:
        """
        Генерация естественной траектории движения мыши
        
        Args:
            start_x, start_y: Начальная позиция
            end_x, end_y: Конечная позиция
        
        Returns:
            Список координат траектории
        """
        steps = random.randint(*self.CONFIG["mouse"]["move_steps"])
        
        # Контрольная точка для кривой Безье (создаёт изгиб)
        curve_factor = self.CONFIG["mouse"]["curve_factor"]
        mid_x = (start_x + end_x) / 2 + random.uniform(-100, 100) * curve_factor
        mid_y = (start_y + end_y) / 2 + random.uniform(-100, 100) * curve_factor
        
        path = []
        for i in range(steps + 1):
            t = i / steps
            
            # Вычисляем точку на кривой Безье
            x, y = self.bezier_curve(
                (start_x, start_y),
                (end_x, end_y),
                (mid_x, mid_y),
                t
            )
            
            # Добавляем микро-дрожание
            jitter_x = random.uniform(*self.CONFIG["mouse"]["jitter_range"])
            jitter_y = random.uniform(*self.CONFIG["mouse"]["jitter_range"])
            
            path.append((x + jitter_x, y + jitter_y))
        
        # Возможный промах с коррекцией
        if random.random() < self.CONFIG["mouse"]["overshoot_chance"]:
            overshoot_x = end_x + random.uniform(-10, 10)
            overshoot_y = end_y + random.uniform(-10, 10)
            path.append((overshoot_x, overshoot_y))
            path.append((end_x, end_y))  # Коррекция
        
        return path
    
    async def move_mouse_human(self, page, target_x: float, target_y: float, 
                              current_x: float = 0, current_y: float = 0):
        """
        Движение мыши с эмуляцией человека (для Puppeteer/Playwright)
        
        Args:
            page: Объект страницы браузера
            target_x, target_y: Целевые координаты
            current_x, current_y: Текущие координаты
        """
        path = self.generate_mouse_path(current_x, current_y, target_x, target_y)
        
        for x, y in path:
            await page.mouse.move(x, y)
            delay = random.uniform(*self.CONFIG["mouse"]["step_delay"])
            await asyncio.sleep(delay)
        
        # Логирование действия
        self.action_history.append({
            "action": "mouse_move",
            "from": (current_x, current_y),
            "to": (target_x, target_y),
            "timestamp": datetime.now().isoformat(),
            "path_length": len(path)
        })
    
    # ============================================
    # КЛИКИ
    # ============================================
    
    async def click_human(self, page, element_selector: str = None, 
                         x: float = None, y: float = None):
        """
        Клик с эмуляцией человека
        
        Args:
            page: Объект страницы браузера
            element_selector: CSS селектор элемента (если None, используется x, y)
            x, y: Координаты клика (если element_selector не указан)
        """
        # Получаем координаты элемента
        if element_selector:
            element = await page.query_selector(element_selector)
            if not element:
                print(f"❌ Элемент не найден: {element_selector}")
                return
            
            box = await element.bounding_box()
            if not box:
                print(f"❌ Не удалось получить координаты элемента")
                return
            
            # Кликаем в случайную точку внутри элемента
            target_x = box['x'] + random.uniform(box['width'] * 0.2, box['width'] * 0.8)
            target_y = box['y'] + random.uniform(box['height'] * 0.2, box['height'] * 0.8)
        else:
            target_x, target_y = x, y
        
        # Наведение курсора перед кликом
        if random.random() < self.CONFIG["click"]["hover_before"]:
            await self.move_mouse_human(page, target_x, target_y)
            hover_duration = random.uniform(*self.CONFIG["click"]["hover_duration"])
            await asyncio.sleep(hover_duration)
            
            # Двойная проверка (навести курсор снова)
            if random.random() < self.CONFIG["click"]["double_check"]:
                await page.mouse.move(target_x - 5, target_y - 5)
                await asyncio.sleep(0.1)
                await page.mouse.move(target_x, target_y)
        else:
            await self.move_mouse_human(page, target_x, target_y)
        
        # Промах с коррекцией
        if random.random() < self.CONFIG["click"]["miss_rate"]:
            miss_x = target_x + random.uniform(-15, 15)
            miss_y = target_y + random.uniform(-15, 15)
            await page.mouse.move(miss_x, miss_y)
            correction_delay = random.uniform(*self.CONFIG["click"]["miss_correction"])
            await asyncio.sleep(correction_delay)
            await page.mouse.move(target_x, target_y)
        
        # Клик с задержкой между нажатием и отпусканием
        await page.mouse.down()
        await asyncio.sleep(random.uniform(0.05, 0.15))
        await page.mouse.up()
        
        # Логирование
        self.action_history.append({
            "action": "click",
            "element": element_selector,
            "coordinates": (target_x, target_y),
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"🖱️ Клик: {element_selector or f'({target_x}, {target_y})'}")
    
    # ============================================
    # ПРОКРУТКА
    # ============================================
    
    async def scroll_human(self, page, distance: int, direction: str = "down"):
        """
        Прокрутка с эмуляцией человека
        
        Args:
            page: Объект страницы браузера
            distance: Расстояние прокрутки (пиксели)
            direction: Направление ("down" или "up")
        """
        scroll_multiplier = -1 if direction == "down" else 1
        
        # Разбиваем прокрутку на части
        chunks = []
        remaining = abs(distance)
        
        while remaining > 0:
            chunk_size = min(random.randint(50, 200), remaining)
            chunks.append(chunk_size * scroll_multiplier)
            remaining -= chunk_size
            
            # Возможная пауза для "чтения"
            if random.random() < self.CONFIG["scroll"]["pause_chance"]:
                pause = random.uniform(*self.CONFIG["scroll"]["pause_duration"])
                chunks.append(("pause", pause))
        
        # Возможная прокрутка назад
        if random.random() < self.CONFIG["scroll"]["back_scroll_chance"]:
            back_distance = random.randint(50, 150) * -scroll_multiplier
            chunks.append(back_distance)
        
        # Выполняем прокрутку
        for chunk in chunks:
            if isinstance(chunk, tuple) and chunk[0] == "pause":
                await asyncio.sleep(chunk[1])
            else:
                await page.evaluate(f"window.scrollBy(0, {chunk})")
                
                # Инерция - замедление к концу
                speed = random.uniform(*self.CONFIG["scroll"]["speed_range"])
                delay = abs(chunk) / speed * self.CONFIG["scroll"]["momentum"]
                await asyncio.sleep(delay)
        
        # Логирование
        self.action_history.append({
            "action": "scroll",
            "distance": distance,
            "direction": direction,
            "chunks": len([c for c in chunks if not isinstance(c, tuple)]),
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"📜 Прокрутка: {distance}px {direction}")
    
    # ============================================
    # ВВОД ТЕКСТА
    # ============================================
    
    async def type_human(self, page, selector: str, text: str):
        """
        Ввод текста с эмуляцией человека
        
        Args:
            page: Объект страницы браузера
            selector: CSS селектор поля ввода
            text: Текст для ввода
        """
        # Фокус на элементе
        await page.focus(selector)
        await asyncio.sleep(random.uniform(0.2, 0.5))
        
        # Вычисляем скорость печати (символов в секунду)
        wpm = random.uniform(*self.CONFIG["typing"]["wpm_range"])
        chars_per_second = (wpm * 5) / 60  # Среднее слово = 5 символов
        
        typed_text = ""
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # Опечатка
            if random.random() < self.CONFIG["typing"]["typo_rate"]:
                # Вводим неправильный символ
                wrong_char = random.choice("qwertyuiopasdfghjklzxcvbnm")
                await page.keyboard.press(wrong_char)
                typed_text += wrong_char
                
                # Задержка перед исправлением
                correction_delay = random.uniform(*self.CONFIG["typing"]["typo_correction_delay"])
                await asyncio.sleep(correction_delay)
                
                # Исправляем (Backspace)
                await page.keyboard.press("Backspace")
                typed_text = typed_text[:-1]
                await asyncio.sleep(0.1)
            
            # Вводим правильный символ
            await page.keyboard.press(char)
            typed_text += char
            
            # Пауза на знаках препинания
            if self.CONFIG["typing"]["pause_on_punctuation"] and char in ".,!?;:":
                pause = random.uniform(*self.CONFIG["typing"]["punctuation_pause"])
                await asyncio.sleep(pause)
            
            # Задержка между символами
            delay = 1 / chars_per_second
            variance = random.uniform(0.5, 1.5)
            await asyncio.sleep(delay * variance)
            
            i += 1
        
        # Логирование
        self.action_history.append({
            "action": "type",
            "selector": selector,
            "text_length": len(text),
            "wpm": wpm,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"⌨️ Введён текст: {len(text)} символов ({wpm:.0f} WPM)")
    
    # ============================================
    # СТАТИСТИКА И ЛОГИ
    # ============================================
    
    def get_session_stats(self) -> Dict:
        """
        Статистика текущей сессии
        
        Returns:
            Словарь со статистикой действий
        """
        action_counts = {}
        for action in self.action_history:
            action_type = action["action"]
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "session_start": self.session_start.isoformat(),
            "duration_seconds": session_duration,
            "total_actions": len(self.action_history),
            "action_counts": action_counts,
            "actions_per_minute": len(self.action_history) / (session_duration / 60) if session_duration > 0 else 0
        }
    
    def export_activity_log(self, filepath: str):
        """
        Экспорт лога активности в JSON
        
        Args:
            filepath: Путь к файлу для сохранения
        """
        data = {
            "session_stats": self.get_session_stats(),
            "action_history": self.action_history,
            "config": self.CONFIG
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Лог активности сохранён: {filepath}")


# ============================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================

async def demo_human_simulation():
    """Демонстрация симуляции человеческого поведения"""
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 ДЕМОНСТРАЦИЯ СИМУЛЯТОРА ЧЕЛОВЕЧЕСКОГО ПОВЕДЕНИЯ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    simulator = HumanBehaviorSimulator()
    
    # Примеры задержек
    print("\n1️⃣ Временные задержки:")
    for i in range(3):
        delay = simulator.human_delay()
        print(f"   Задержка {i+1}: {delay:.2f} сек")
    
    # Пример траектории мыши
    print("\n2️⃣ Генерация траектории мыши:")
    path = simulator.generate_mouse_path(0, 0, 500, 300)
    print(f"   От (0, 0) до (500, 300)")
    print(f"   Точек траектории: {len(path)}")
    print(f"   Первые 3 точки: {path[:3]}")
    print(f"   Последние 3 точки: {path[-3:]}")
    
    # Пример задержки чтения
    print("\n3️⃣ Задержка для чтения:")
    text = "Это пример текста для демонстрации времени чтения"
    reading_time = simulator.reading_delay(text)
    print(f"   Текст: '{text}'")
    print(f"   Слов: {len(text.split())}")
    print(f"   Время чтения: {reading_time:.2f} сек")
    
    # Статистика сессии
    print("\n4️⃣ Статистика сессии:")
    stats = simulator.get_session_stats()
    print(f"   Длительность: {stats['duration_seconds']:.2f} сек")
    print(f"   Всего действий: {stats['total_actions']}")
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Демонстрация завершена!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    # Запуск демонстрации
    asyncio.run(demo_human_simulation())
