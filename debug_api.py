"""
ОТЛАДЧИК API ОДНОГО СТОЛА
========================

Проверяет что именно возвращает API стола.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

def debug_api():
    """Отладка API стола"""
    print("🔍 ОТЛАДКА API СТОЛА")
    print("=" * 20)
    
    # Загружаем конфигурацию
    try:
        with open('casino_setup.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка загрузки конфигурации: {e}")
        return
    
    table_id = config.get('table_info', {}).get('table_id', 'roulettestura541')
    auth = config['api']['auth']
    
    print(f"🎯 Стол: {table_id}")
    print(f"🔑 JSESSIONID: {auth['jsessionid'][:50]}...")
    
    # Тестируем API статистики
    try:
        base_url = "https://games.pragmaticplaylive.net/api/ui/statisticHistory"
        
        params = {
            'tableId': table_id,
            'numberOfGames': 10,
            'JSESSIONID': auth['jsessionid'],
            'ck': str(int(datetime.now().timestamp() * 1000)),
            'game_mode': 'lobby_desktop'
        }
        
        url = f"{base_url}?" + urllib.parse.urlencode(params)
        print(f"🌐 URL: {url[:100]}...")
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        req.add_header('Accept', 'application/json, text/plain, */*')
        req.add_header('Accept-Language', 'ru,en-US;q=0.9,en;q=0.8,lt;q=0.7')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            content_type = response.headers.get('Content-Type', '')
            data = response.read().decode('utf-8')
            
            print(f"📊 Status: {status}")
            print(f"📄 Content-Type: {content_type}")
            print(f"📏 Размер ответа: {len(data)} байт")
            
            if status == 200:
                print("\n🔍 ПЕРВЫЕ 500 СИМВОЛОВ ОТВЕТА:")
                print("-" * 50)
                print(data[:500])
                print("-" * 50)
                
                # Пытаемся парсить JSON
                try:
                    json_data = json.loads(data)
                    print(f"\n✅ JSON валидный")
                    print(f"🔑 Ключи верхнего уровня: {list(json_data.keys())}")
                    
                    if 'history' in json_data:
                        history = json_data['history']
                        print(f"📊 История: {len(history)} записей")
                        
                        if history and len(history) > 0:
                            print(f"🎯 Первая запись:")
                            first_game = history[0]
                            print(f"   Ключи: {list(first_game.keys())}")
                            print(f"   Данные: {json.dumps(first_game, indent=2, ensure_ascii=False)[:300]}...")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Ошибка JSON: {e}")
            else:
                print(f"❌ Неуспешный статус: {status}")
                
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

if __name__ == "__main__":
    debug_api()