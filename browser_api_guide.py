"""
ПОШАГОВЫЙ ГАЙД: ПОИСК API ЧЕРЕЗ КОНСОЛЬ БРАУЗЕРА
===============================================

Этот скрипт поможет найти API казино через анализ сетевого трафика
и автоматически настроить систему.
"""

import json
import os
from datetime import datetime
from pathlib import Path

class BrowserAPIGuide:
    """Гайд по поиску API через браузер"""
    
    def __init__(self):
        self.found_apis = []
        self.casino_config = {}
    
    def run_guide(self):
        """Запуск пошагового гайда"""
        print("🕵️ ПОИСК API ЧЕРЕЗ КОНСОЛЬ БРАУЗЕРА")
        print("=" * 45)
        print("Следуйте инструкциям для поиска API вашего казино\n")
        
        self.step_1_preparation()
        self.step_2_browser_setup()
        self.step_3_traffic_analysis()
        self.step_4_api_identification()
        self.step_5_configuration()
        self.step_6_testing()
    
    def step_1_preparation(self):
        """Шаг 1: Подготовка"""
        print("📋 ШАГ 1: ПОДГОТОВКА")
        print("-" * 25)
        print("""
1. Выберите казино с live-рулеткой
2. Убедитесь что у вас есть аккаунт (или можете играть в демо)
3. Подготовьте браузер (Chrome/Firefox/Edge)

ЛУЧШИЕ КАНДИДАТЫ:
• Криптовалютные казино (Stake, BC.Game, Roobet)
• Казино с Evolution Gaming
• Казино с демо-режимом
        """)
        
        casino_url = input("Введите URL казино с live-рулеткой: ").strip()
        if casino_url:
            self.casino_config['casino_url'] = casino_url
            print(f"✅ Установлено казино: {casino_url}")
        
        input("\nНажмите Enter когда будете готовы к следующему шагу...")
    
    def step_2_browser_setup(self):
        """Шаг 2: Настройка браузера"""
        print("\n🌐 ШАГ 2: НАСТРОЙКА БРАУЗЕРА")
        print("-" * 30)
        print("""
ИНСТРУКЦИИ:

1. Откройте браузер (желательно Chrome)
2. Перейдите на страницу live-рулетки
3. Нажмите F12 (или Ctrl+Shift+I)
4. В Developer Tools перейдите на вкладку "Network" (Сеть)
5. ВАЖНО: Поставьте фильтр "XHR" или "Fetch"

СКРИНШОТ КОНСОЛИ:
┌─────────────────────────────────────┐
│ Elements Console Sources Network    │ <- Вкладки
├─────────────────────────────────────┤
│ ○ All JS CSS XHR Fetch WS Other     │ <- Фильтры (выберите XHR)
├─────────────────────────────────────┤
│ Name         Status  Type    Size   │
│ ...                                 │
└─────────────────────────────────────┘

НАСТРОЙКИ ФИЛЬТРА:
• Включите "XHR" - это AJAX запросы
• Включите "Fetch" - современные запросы  
• Отключите остальное для чистоты
        """)
        
        ready = input("Готово? Консоль открыта, фильтр XHR включен? (y/n): ").lower()
        if ready == 'y':
            print("✅ Браузер настроен")
        else:
            print("⚠️ Вернитесь к настройке браузера перед продолжением")
        
        input("\nНажмите Enter для продолжения...")
    
    def step_3_traffic_analysis(self):
        """Шаг 3: Анализ трафика"""
        print("\n📊 ШАГ 3: АНАЛИЗ СЕТЕВОГО ТРАФИКА")
        print("-" * 35)
        print("""
ДЕЙСТВИЯ В БРАУЗЕРЕ:

1. ▶️ ЗАПУСТИТЕ МОНИТОРИНГ:
   • В Network tab нажмите кнопку записи (красный кружок)
   • Или просто начните взаимодействие с сайтом

2. 🎰 ВЗАИМОДЕЙСТВУЙТЕ С РУЛЕТКОЙ:
   • Зайдите в live-рулетку
   • Подождите несколько спинов
   • Если можете - сделайте ставку
   • Наблюдайте за результатами

3. 🔍 НАБЛЮДАЙТЕ ЗА ЗАПРОСАМИ:
   В консоли должны появляться запросы.
   ИЩИТЕ запросы с названиями содержащими:
   • "roulette", "live", "game", "result"
   • "history", "spin", "wheel", "bet"
   • числовые ID или коды игр

ПРИМЕР того что вы можете увидеть:
┌─────────────────────────────────────┐
│ live_game_data    200  xhr  1.2kb   │ ← ХОРОШО!
│ roulette_results  200  xhr  856b    │ ← ОТЛИЧНО!
│ api/games/12345   200  xhr  2.1kb   │ ← ВОЗМОЖНО
│ websocket         101  ws   -       │ ← WebSocket
└─────────────────────────────────────┘
        """)
        
        input("Понаблюдайте за трафиком 2-3 минуты, затем нажмите Enter...")
        
        # Собираем информацию от пользователя
        print("\n🎯 ЧТО ВЫ НАШЛИ?")
        print("Перечислите интересные запросы (по одному на строку, Enter для завершения):")
        
        found_requests = []
        while True:
            request = input("Запрос (или Enter для завершения): ").strip()
            if not request:
                break
            found_requests.append(request)
        
        if found_requests:
            self.found_apis = found_requests
            print(f"✅ Записано {len(found_requests)} потенциальных API запросов")
        else:
            print("⚠️ Запросы не найдены. Попробуйте еще раз или проверьте фильтры")
    
    def step_4_api_identification(self):
        """Шаг 4: Идентификация API"""
        print("\n🔍 ШАГ 4: АНАЛИЗ НАЙДЕННЫХ ЗАПРОСОВ")
        print("-" * 38)
        
        if not self.found_apis:
            print("❌ Нет запросов для анализа")
            return
        
        print("Для каждого запроса нужно получить детальную информацию:")
        print("""
ИНСТРУКЦИИ:
1. Кликните на запрос в Network tab
2. Справа откроется панель с деталями
3. Скопируйте информацию:
   • Request URL (полный URL)
   • Method (GET/POST)
   • Response (ответ сервера)

ПРИМЕР анализа:
┌─────────────────┐
│ Request URL:    │
│ https://...     │ ← СКОПИРУЙТЕ ЭТО
├─────────────────┤  
│ Request Method: │
│ GET             │ ← И ЭТО
├─────────────────┤
│ Response:       │
│ {"numbers":...} │ ← И ЭТО (если JSON)
└─────────────────┘
        """)
        
        api_details = []
        
        for i, request in enumerate(self.found_apis, 1):
            print(f"\n📋 ЗАПРОС {i}: {request}")
            
            url = input("  Полный URL: ").strip()
            method = input("  Method (GET/POST/...): ").strip().upper() or "GET"
            
            print("  Ответ сервера (первые 200 символов):")
            response = input("  Response: ").strip()
            
            has_roulette_data = input("  Содержит данные рулетки? (y/n): ").lower() == 'y'
            
            api_details.append({
                'name': request,
                'url': url,
                'method': method,
                'response_preview': response[:200],
                'has_roulette_data': has_roulette_data
            })
        
        # Фильтруем подходящие API
        good_apis = [api for api in api_details if api['has_roulette_data']]
        
        if good_apis:
            print(f"\n🎯 НАЙДЕНО {len(good_apis)} ПОДХОДЯЩИХ API:")
            for api in good_apis:
                print(f"  ✅ {api['name']}: {api['url']}")
            self.casino_config['apis'] = good_apis
        else:
            print("😞 Подходящие API не найдены")
    
    def step_5_configuration(self):
        """Шаг 5: Создание конфигурации"""
        print("\n⚙️ ШАГ 5: СОЗДАНИЕ КОНФИГУРАЦИИ")
        print("-" * 32)
        
        if not self.casino_config.get('apis'):
            print("❌ Нет API для настройки")
            self.manual_config_fallback()
            return
        
        # Создаем конфигурацию
        config = {
            'casino_name': input("Название казино: ").strip() or "Unknown Casino",
            'connection_method': 'api',
            'api': {
                'base_url': self.extract_base_url(self.casino_config['apis'][0]['url']),
                'endpoints': {},
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
            },
            'betting': {
                'base_bet': 100,
                'max_bet': 10000,
                'bankroll': 100000
            },
            'safety': {
                'enabled': True,
                'max_daily_loss': 50000
            }
        }
        
        # Добавляем найденные endpoints
        for api in self.casino_config['apis']:
            endpoint_name = input(f"Название для {api['name']} (live_results/history/...): ").strip()
            if endpoint_name:
                config['api']['endpoints'][endpoint_name] = self.extract_endpoint(api['url'])
        
        # Сохраняем конфигурацию
        self.save_config(config)
        print("✅ Конфигурация создана и сохранена")
    
    def manual_config_fallback(self):
        """Резервная ручная настройка"""
        print("\n🛠️ РЕЗЕРВНАЯ НАСТРОЙКА")
        print("-" * 20)
        print("Создаем базовую конфигурацию для ручного ввода данных")
        
        config = {
            'casino_name': input("Название казино: ").strip() or "Manual Casino",
            'connection_method': 'manual',
            'betting': {
                'base_bet': 100,
                'max_bet': 10000, 
                'bankroll': 100000
            }
        }
        
        self.save_config(config)
        print("✅ Базовая конфигурация создана")
    
    def step_6_testing(self):
        """Шаг 6: Тестирование"""
        print("\n🧪 ШАГ 6: ТЕСТИРОВАНИЕ НАСТРОЙКИ")
        print("-" * 30)
        
        print("Теперь протестируем настроенное подключение:")
        
        test_choice = input("Запустить тест подключения? (y/n): ").lower()
        if test_choice == 'y':
            self.run_connection_test()
        
        print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
        print("1. python test_connection.py - детальная проверка")
        print("2. python src/main.py - запуск основной системы")
        print("3. Выберите 'Получить реальные данные' в меню")
        
        print("\n🎉 Настройка завершена!")
    
    def extract_base_url(self, url):
        """Извлечь базовый URL"""
        if '://' in url:
            protocol_and_domain = url.split('/')[:3]
            return '/'.join(protocol_and_domain)
        return url
    
    def extract_endpoint(self, url):
        """Извлечь endpoint из URL"""
        if '://' in url:
            parts = url.split('/')
            if len(parts) > 3:
                return '/' + '/'.join(parts[3:])
        return url
    
    def save_config(self, config):
        """Сохранить конфигурацию"""
        try:
            config_path = Path(__file__).parent / "casino_setup.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"💾 Конфигурация сохранена в {config_path}")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def run_connection_test(self):
        """Быстрый тест подключения"""
        print("\n🔗 Тестирование подключения...")
        
        try:
            # Пытаемся загрузить и протестировать конфигурацию
            config_path = Path(__file__).parent / "casino_setup.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                print(f"✅ Конфигурация загружена")
                print(f"   Казино: {config.get('casino_name')}")
                print(f"   Метод: {config.get('connection_method')}")
                
                if config.get('connection_method') == 'api':
                    endpoints = config.get('api', {}).get('endpoints', {})
                    print(f"   API endpoints: {len(endpoints)}")
                    for name, endpoint in endpoints.items():
                        print(f"     • {name}: {endpoint}")
                
                print("✅ Базовая проверка пройдена")
            else:
                print("❌ Конфигурация не найдена")
                
        except Exception as e:
            print(f"❌ Ошибка тестирования: {e}")


def main():
    """Главная функция"""
    try:
        guide = BrowserAPIGuide()
        guide.run_guide()
        
    except KeyboardInterrupt:
        print("\n\n👋 Настройка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()