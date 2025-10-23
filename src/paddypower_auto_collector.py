"""
🎰 PADDYPOWER АВТОМАТИЧЕСКИЙ КОЛЛЕКТОР С АНТИ-ДЕТЕКТОМ
========================================================

Полная автоматизация:
- Продвинутый анти-детект (fingerprints, User-Agent, canvas/WebGL spoofing)
- Автоматический вход в аккаунт (логин/пароль из .env)
- Обработка cookies и сохранение сессий
- Обход уведомлений и попапов
- Навигация по рулеткам (автопоиск игры)
- Интеллектуальный сбор данных

Автор: RULETTT Team
Версия: 3.0 (Enhanced Anti-Detect)
"""

import asyncio
import json
import random
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

try:
    from pyppeteer import launch
    from pyppeteer.page import Page
    from pyppeteer.browser import Browser
    PYPPETEER_AVAILABLE = True
except ImportError:
    PYPPETEER_AVAILABLE = False
    print("⚠️ pyppeteer не установлен. Установите: pip install pyppeteer")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv не установлен. Используем переменные окружения")

try:
    from bot_simulator import HumanBehaviorSimulator
    SIMULATOR_AVAILABLE = True
except ImportError:
    SIMULATOR_AVAILABLE = False
    print("⚠️ bot_simulator не найден. Симуляция человека отключена")


class AntiDetectBrowser:
    """Продвинутый анти-детект для браузера"""
    
    # Реалистичные User-Agents (обновлённые 2025)
    USER_AGENTS = [
        # Chrome Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        
        # Chrome Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        
        # Firefox Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    ]
    
    # Реалистичные разрешения экрана
    SCREEN_RESOLUTIONS = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
        {'width': 1440, 'height': 900},
        {'width': 2560, 'height': 1440},
    ]
    
    # Реалистичные языки
    LANGUAGES = [
        'en-US,en;q=0.9',
        'en-GB,en;q=0.9',
        'en-US,en;q=0.9,ru;q=0.8',
    ]
    
    # Реалистичные платформы
    PLATFORMS = ['Win32', 'MacIntel', 'Linux x86_64']
    
    @staticmethod
    def get_random_fingerprint() -> Dict:
        """Генерация случайного реалистичного fingerprint"""
        resolution = random.choice(AntiDetectBrowser.SCREEN_RESOLUTIONS)
        
        return {
            'userAgent': random.choice(AntiDetectBrowser.USER_AGENTS),
            'viewport': resolution,
            'language': random.choice(AntiDetectBrowser.LANGUAGES),
            'platform': random.choice(AntiDetectBrowser.PLATFORMS),
            'timezone': 'Europe/London',  # Paddypower - UK
            'webgl_vendor': 'Google Inc. (NVIDIA)',
            'webgl_renderer': 'ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)',
        }
    
    @staticmethod
    async def apply_stealth(page: Page, fingerprint: Dict):
        """Применение анти-детект скриптов к странице"""
        
        print("🛡️ Применяю анти-детект защиту...")
        
        # 1. Удаление флагов автоматизации
        await page.evaluateOnNewDocument('''() => {
            // Удаляем webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
            
            // Маскируем permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Маскируем плагины
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Маскируем языки
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        }''')
        
        # 2. Установка User-Agent и Platform
        await page.evaluateOnNewDocument(f'''() => {{
            Object.defineProperty(navigator, 'userAgent', {{
                get: () => '{fingerprint["userAgent"]}'
            }});
            
            Object.defineProperty(navigator, 'platform', {{
                get: () => '{fingerprint["platform"]}'
            }});
            
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {random.randint(4, 16)}
            }});
            
            Object.defineProperty(navigator, 'deviceMemory', {{
                get: () => {random.choice([4, 8, 16])}
            }});
        }}''')
        
        # 3. Canvas fingerprint spoofing (легкие шумы)
        await page.evaluateOnNewDocument('''() => {
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {
                const context = this.getContext('2d');
                const imageData = context.getImageData(0, 0, this.width, this.height);
                
                // Добавляем микро-шум (невидимый глазу, но меняет fingerprint)
                for (let i = 0; i < imageData.data.length; i += 4) {
                    if (Math.random() < 0.001) {
                        imageData.data[i] = Math.min(255, imageData.data[i] + Math.random() * 2);
                    }
                }
                
                context.putImageData(imageData, 0, 0);
                return originalToDataURL.apply(this, arguments);
            };
        }''')
        
        # 4. WebGL spoofing
        await page.evaluateOnNewDocument(f'''() => {{
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return '{fingerprint["webgl_vendor"]}';
                }}
                if (parameter === 37446) {{
                    return '{fingerprint["webgl_renderer"]}';
                }}
                return getParameter.apply(this, arguments);
            }};
        }}''')
        
        # 5. Chrome runtime injection
        await page.evaluateOnNewDocument('''() => {
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
        }''')
        
        # 6. Battery API spoofing
        await page.evaluateOnNewDocument('''() => {
            Object.defineProperty(navigator, 'getBattery', {
                value: () => Promise.resolve({
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: 1,
                    addEventListener: () => {},
                    removeEventListener: () => {}
                })
            });
        }''')
        
        # 7. MediaDevices spoofing
        await page.evaluateOnNewDocument('''() => {
            navigator.mediaDevices.enumerateDevices = () => Promise.resolve([
                { kind: 'audioinput', deviceId: 'default', label: '', groupId: '' },
                { kind: 'videoinput', deviceId: 'default', label: '', groupId: '' },
                { kind: 'audiooutput', deviceId: 'default', label: '', groupId: '' }
            ]);
        }''')
        
        print("✅ Анти-детект активирован")


class PaddypowerAutoCollector:
    """Полностью автоматический коллектор для Paddypower с авто-входом"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Инициализация коллектора"""
        self.config = self.load_config(config_path)
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.simulator = HumanBehaviorSimulator() if SIMULATOR_AVAILABLE else None
        self.fingerprint = AntiDetectBrowser.get_random_fingerprint()
        self.cookies_file = Path('data/paddypower_cookies.json')
        self.session_active = False
        
        print("🎰 Paddypower Автоматический Коллектор v3.0")
        print(f"🛡️ Анти-детект: ✅")
        print(f"🤖 Симуляция человека: {'✅' if self.simulator else '❌'}")
        
    def load_config(self, config_path: Optional[str] = None) -> Dict:
        """Загрузка конфигурации"""
        config = {
            # Paddypower аккаунт (из .env или аргументов)
            'username': os.getenv('PADDYPOWER_USERNAME', ''),
            'password': os.getenv('PADDYPOWER_PASSWORD', ''),
            
            # URL-ы
            'login_url': 'https://www.paddypower.com/login',
            'roulette_url': 'https://games.paddypower.com/roulette',
            'base_url': 'https://www.paddypower.com',
            
            # Настройки бота
            'headless': os.getenv('BOT_HEADLESS', 'false').lower() == 'true',
            'duration_minutes': int(os.getenv('COLLECTION_DURATION', '30')),
            'check_interval': 30,  # секунды между проверками
            
            # XPath из paddypower_collector_v2.js
            'roulette_xpath': '/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/div[7]/div/div[3]/div',
            
            # Селекторы для навигации
            'selectors': {
                'login_button': 'button[data-testid="login-button"]',
                'username_input': 'input[name="username"], input[type="email"], input[data-testid="username"]',
                'password_input': 'input[name="password"], input[type="password"], input[data-testid="password"]',
                'submit_login': 'button[type="submit"]',
                'accept_cookies': 'button[data-testid="accept-cookies"], button:has-text("Accept")',
                'close_popup': 'button[aria-label="Close"], button.close, .modal-close',
                'roulette_game': 'a[href*="roulette"], div[data-game*="roulette"]',
                'game_iframe': 'iframe[src*="game"], iframe[name="game"]',
            },
            
            # Выходной файл
            'output_file': 'roulette_console_data.json',
        }
        
        # Проверка обязательных полей
        if not config['username'] or not config['password']:
            print("⚠️ ВНИМАНИЕ: Логин/пароль не заданы!")
            print("   Установите переменные окружения:")
            print("   PADDYPOWER_USERNAME=ваш_логин")
            print("   PADDYPOWER_PASSWORD=ваш_пароль")
            print("   Или используйте аргументы командной строки")
        
        return config
    
    async def init_browser(self):
        """Инициализация браузера с анти-детектом"""
        print("\n🌐 Запускаю браузер...")
        
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            f'--window-size={self.fingerprint["viewport"]["width"]},{self.fingerprint["viewport"]["height"]}',
            f'--user-agent={self.fingerprint["userAgent"]}',
            '--lang=en-GB',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-popup-blocking',
        ]
        
        self.browser = await launch(
            headless=self.config['headless'],
            args=browser_args,
            ignoreHTTPSErrors=True,
            slowMo=10,  # Легкая задержка для естественности
        )
        
        self.page = await self.browser.newPage()
        
        # Применяем анти-детект
        await AntiDetectBrowser.apply_stealth(self.page, self.fingerprint)
        
        # Устанавливаем viewport
        await self.page.setViewport(self.fingerprint['viewport'])
        
        # Устанавливаем timezone и geolocation (UK для Paddypower)
        await self.page.emulateTimezone('Europe/London')
        await self.page.setGeolocation({'latitude': 51.5074, 'longitude': -0.1278})  # London
        
        # Загружаем сохранённые cookies если есть
        await self.load_cookies()
        
        print("✅ Браузер готов")
        print(f"   User-Agent: {self.fingerprint['userAgent'][:80]}...")
        print(f"   Viewport: {self.fingerprint['viewport']['width']}x{self.fingerprint['viewport']['height']}")
        
    async def load_cookies(self):
        """Загрузка сохранённых cookies"""
        if self.cookies_file.exists():
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    await self.page.setCookie(*cookies)
                print("🍪 Cookies загружены из файла")
                self.session_active = True
            except Exception as e:
                print(f"⚠️ Ошибка загрузки cookies: {e}")
    
    async def save_cookies(self):
        """Сохранение cookies для следующих сессий"""
        try:
            cookies = await self.page.cookies()
            self.cookies_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            print("🍪 Cookies сохранены")
        except Exception as e:
            print(f"⚠️ Ошибка сохранения cookies: {e}")
    
    async def human_wait(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Человекоподобная задержка"""
        if self.simulator:
            await self.simulator.wait_human(min_sec, max_sec)
        else:
            await asyncio.sleep(random.uniform(min_sec, max_sec))
    
    async def handle_popups(self):
        """Закрытие попапов и уведомлений"""
        print("🚫 Проверяю попапы и уведомления...")
        
        popup_selectors = [
            self.config['selectors']['accept_cookies'],
            self.config['selectors']['close_popup'],
            'button:has-text("Accept All")',
            'button:has-text("I Agree")',
            'button:has-text("Continue")',
            'button:has-text("OK")',
            'button[aria-label="Dismiss"]',
            '.cookie-banner button',
            '#onetrust-accept-btn-handler',
            '.gdpr-accept',
        ]
        
        for selector in popup_selectors:
            try:
                elements = await self.page.querySelectorAll(selector)
                if elements:
                    print(f"   ✅ Закрываю: {selector}")
                    await elements[0].click()
                    await self.human_wait(0.5, 1.5)
            except Exception:
                continue
        
        print("✅ Попапы обработаны")
    
    async def auto_login(self):
        """Автоматический вход в аккаунт"""
        if not self.config['username'] or not self.config['password']:
            print("❌ Логин/пароль не заданы. Пропускаю авто-вход")
            return False
        
        print("\n🔐 Автоматический вход в аккаунт...")
        
        try:
            # Переход на страницу логина
            print("   Открываю страницу входа...")
            await self.page.goto(self.config['login_url'], {'waitUntil': 'networkidle2'})
            await self.human_wait(2, 4)
            
            # Закрываем попапы
            await self.handle_popups()
            
            # Ищем поле username
            print("   Ввожу логин...")
            username_input = await self.page.querySelector(self.config['selectors']['username_input'])
            if not username_input:
                print("   ❌ Поле логина не найдено")
                return False
            
            await username_input.click()
            await self.human_wait(0.3, 0.7)
            
            # Вводим username с симуляцией печати
            if self.simulator:
                for char in self.config['username']:
                    await username_input.type(char)
                    await asyncio.sleep(random.uniform(0.05, 0.15))
            else:
                await username_input.type(self.config['username'])
            
            await self.human_wait(0.5, 1.5)
            
            # Ищем поле password
            print("   Ввожу пароль...")
            password_input = await self.page.querySelector(self.config['selectors']['password_input'])
            if not password_input:
                print("   ❌ Поле пароля не найдено")
                return False
            
            await password_input.click()
            await self.human_wait(0.3, 0.7)
            
            # Вводим password
            if self.simulator:
                for char in self.config['password']:
                    await password_input.type(char)
                    await asyncio.sleep(random.uniform(0.05, 0.15))
            else:
                await password_input.type(self.config['password'])
            
            await self.human_wait(1, 2)
            
            # Нажимаем кнопку входа
            print("   Нажимаю кнопку входа...")
            submit_button = await self.page.querySelector(self.config['selectors']['submit_login'])
            if submit_button:
                await submit_button.click()
            else:
                # Пробуем Enter
                await password_input.press('Enter')
            
            # Ждём загрузки
            await self.human_wait(5, 8)
            await self.page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 30000})
            
            # Сохраняем cookies
            await self.save_cookies()
            
            # Проверяем успешность входа
            current_url = self.page.url
            if 'login' not in current_url.lower():
                print("✅ Успешный вход в аккаунт!")
                self.session_active = True
                return True
            else:
                print("❌ Вход не удался (всё ещё на странице логина)")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка авто-входа: {e}")
            return False
    
    async def navigate_to_roulette(self):
        """Навигация к рулетке"""
        print("\n🎰 Навигация к рулетке...")
        
        try:
            # Сначала пробуем прямой URL
            print("   Открываю раздел рулетки...")
            await self.page.goto(self.config['roulette_url'], {'waitUntil': 'networkidle2', 'timeout': 60000})
            await self.human_wait(3, 5)
            
            # Закрываем попапы
            await self.handle_popups()
            
            # Ищем iframe с игрой
            print("   Ищу iframe с игрой...")
            iframe_element = await self.page.querySelector(self.config['selectors']['game_iframe'])
            
            if iframe_element:
                print("✅ Iframe найден!")
                iframe = await iframe_element.contentFrame()
                
                if iframe:
                    print("✅ Игра загружена в iframe")
                    return iframe
            
            # Если iframe не найден, ищем ссылку на игру Spin and Go Roulette
            print("   Ищу ссылку на Spin and Go Roulette...")
            roulette_links = await self.page.querySelectorAll('a[href*="roulette"], button:has-text("Spin and Go")')
            
            if roulette_links:
                print(f"   Найдено {len(roulette_links)} ссылок на рулетку")
                # Кликаем по первой
                await roulette_links[0].click()
                await self.human_wait(5, 8)
                await self.page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 60000})
                
                # Снова ищем iframe
                iframe_element = await self.page.querySelector(self.config['selectors']['game_iframe'])
                if iframe_element:
                    iframe = await iframe_element.contentFrame()
                    if iframe:
                        print("✅ Игра загружена!")
                        return iframe
            
            print("⚠️ Iframe с игрой не найден, использую основную страницу")
            return None
            
        except Exception as e:
            print(f"❌ Ошибка навигации: {e}")
            return None
    
    async def inject_collector_script(self, target_page):
        """Инъекция JavaScript коллектора"""
        print("\n💉 Инжектирую коллектор...")
        
        # Читаем оригинальный скрипт
        script_path = Path(__file__).parent.parent / 'paddypower_collector_v2.js'
        
        if not script_path.exists():
            print(f"❌ Скрипт не найден: {script_path}")
            return False
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                collector_script = f.read()
            
            # Инжектируем в страницу
            await target_page.evaluate(collector_script)
            print("✅ Коллектор внедрён!")
            
            # Даём время на инициализацию
            await self.human_wait(2, 3)
            
            # Проверяем что коллектор работает
            stats = await target_page.evaluate('typeof showPaddypowerStats !== "undefined"')
            if stats:
                print("✅ Коллектор активен и готов к работе")
                return True
            else:
                print("⚠️ Коллектор внедрён, но функции не обнаружены")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка инъекции: {e}")
            return False
    
    async def check_collector_status(self, target_page):
        """Проверка статуса коллектора"""
        try:
            result = await target_page.evaluate('''
                (function() {
                    if (typeof showPaddypowerStats === 'function') {
                        return showPaddypowerStats();
                    }
                    return null;
                })()
            ''')
            
            if result:
                print(f"📊 Собрано спинов: {result.get('total', 0)}")
                print(f"   🔴 Красных: {result.get('red', 0)}")
                print(f"   ⚫ Черных: {result.get('black', 0)}")
                print(f"   🟢 Зеро: {result.get('green', 0)}")
                print(f"   🎯 Последнее: {result.get('lastNumber', '?')} ({result.get('lastColor', '?')})")
            
            return result
        except Exception as e:
            print(f"⚠️ Ошибка проверки статуса: {e}")
            return None
    
    async def export_collected_data(self, target_page) -> Optional[Dict]:
        """Экспорт собранных данных"""
        print("\n📥 Экспортирую данные...")
        
        try:
            data = await target_page.evaluate('''
                (function() {
                    if (typeof exportPaddypowerData === 'function') {
                        return exportPaddypowerData();
                    }
                    return null;
                })()
            ''')
            
            if data and data.get('data'):
                print(f"✅ Экспортировано {len(data['data'])} спинов")
                return data
            else:
                print("⚠️ Нет данных для экспорта")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка экспорта: {e}")
            return None
    
    async def save_to_file(self, data: Dict, filename: str):
        """Сохранение данных в файл"""
        try:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Данные сохранены: {output_path}")
            print(f"   Всего спинов: {len(data.get('data', []))}")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    async def run_collection_session(self):
        """Основной цикл сбора"""
        print("\n🎬 ЗАПУСК СЕССИИ СБОРА")
        print("=" * 60)
        
        # Инициализация браузера
        await self.init_browser()
        
        # Авто-вход (если не залогинены)
        if not self.session_active:
            login_success = await self.auto_login()
            if not login_success:
                print("⚠️ Продолжаю без авто-входа...")
        
        # Навигация к рулетке
        target_frame = await self.navigate_to_roulette()
        target_page = target_frame if target_frame else self.page
        
        # Инъекция коллектора
        collector_ready = await self.inject_collector_script(target_page)
        if not collector_ready:
            print("❌ Не удалось внедрить коллектор. Завершаю.")
            return
        
        # Основной цикл сбора
        print(f"\n⏱️ Начало сбора на {self.config['duration_minutes']} минут")
        print(f"   Проверка каждые {self.config['check_interval']} секунд")
        print("=" * 60)
        
        start_time = datetime.now()
        duration_seconds = self.config['duration_minutes'] * 60
        iteration = 0
        
        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if elapsed >= duration_seconds:
                print(f"\n⏰ Время вышло ({self.config['duration_minutes']} минут)")
                break
            
            iteration += 1
            remaining = duration_seconds - elapsed
            
            print(f"\n🔄 Итерация #{iteration} | Осталось: {remaining/60:.1f} мин")
            
            # Проверяем статус
            await self.check_collector_status(target_page)
            
            # Добавляем случайные действия для естественности
            if iteration % 3 == 0 and self.simulator:
                print("   🎭 Симуляция активности...")
                scroll_amount = random.randint(100, 300)
                if target_frame:
                    await target_page.evaluate(f'window.scrollBy(0, {scroll_amount})')
                else:
                    await self.page.evaluate(f'window.scrollBy(0, {scroll_amount})')
                await self.human_wait(0.5, 1.5)
            
            # Ждём до следующей проверки
            await asyncio.sleep(self.config['check_interval'])
        
        # Финальный экспорт
        print("\n" + "=" * 60)
        print("🏁 ЗАВЕРШЕНИЕ СЕССИИ")
        
        final_data = await self.export_collected_data(target_page)
        
        if final_data:
            await self.save_to_file(final_data, self.config['output_file'])
            print(f"\n✅ УСПЕШНО ЗАВЕРШЕНО!")
            print(f"   Собрано спинов: {len(final_data.get('data', []))}")
            print(f"   Файл: {self.config['output_file']}")
        else:
            print("\n⚠️ Нет данных для сохранения")
        
        print("=" * 60)
    
    async def cleanup(self):
        """Закрытие браузера"""
        if self.browser:
            await self.browser.close()
            print("\n🚪 Браузер закрыт")


async def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='🎰 Paddypower Автоматический Коллектор с Анти-Детектом v3.0'
    )
    
    parser.add_argument('--username', type=str, help='Логин Paddypower')
    parser.add_argument('--password', type=str, help='Пароль Paddypower')
    parser.add_argument('--duration', type=int, default=30, help='Длительность сбора (минуты)')
    parser.add_argument('--headless', action='store_true', help='Скрытый режим браузера')
    parser.add_argument('--output', type=str, default='roulette_console_data.json', help='Выходной файл')
    
    args = parser.parse_args()
    
    # Применяем аргументы к конфигурации
    if args.username:
        os.environ['PADDYPOWER_USERNAME'] = args.username
    if args.password:
        os.environ['PADDYPOWER_PASSWORD'] = args.password
    if args.headless:
        os.environ['BOT_HEADLESS'] = 'true'
    
    # Создаём и запускаем коллектор
    collector = PaddypowerAutoCollector()
    collector.config['duration_minutes'] = args.duration
    collector.config['output_file'] = args.output
    
    try:
        await collector.run_collection_session()
    except KeyboardInterrupt:
        print("\n\n⚠️ Остановлено пользователем (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await collector.cleanup()


if __name__ == '__main__':
    if not PYPPETEER_AVAILABLE:
        print("\n❌ ОШИБКА: pyppeteer не установлен!")
        print("   Установите: pip install pyppeteer playwright")
        print("   Затем: playwright install chromium")
        exit(1)
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🎰 PADDYPOWER АВТОМАТИЧЕСКИЙ КОЛЛЕКТОР v3.0            ║
    ║                                                           ║
    ║  ✅ Продвинутый анти-детект                              ║
    ║  ✅ Автоматический вход в аккаунт                        ║
    ║  ✅ Обработка cookies и уведомлений                      ║
    ║  ✅ Навигация по рулеткам                                ║
    ║  ✅ Интеллектуальный сбор данных                         ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    asyncio.get_event_loop().run_until_complete(main())
