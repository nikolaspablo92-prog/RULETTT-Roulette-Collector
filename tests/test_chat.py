"""
🧪 Тест функциональности чата RULETTT
"""

import requests
import json
from datetime import datetime

def test_chat_api():
    """Тестирование API чата"""
    base_url = "http://localhost:5000"
    
    print("🧪 Тестирование API чата RULETTT...")
    print("=" * 50)
    
    # Тест 1: Проверка health
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ API сервер работает")
            print(f"   Статус: {response.json()['status']}")
        else:
            print("❌ API сервер недоступен")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return False
    
    # Тест 2: Получение сообщений чата (пустой список)
    try:
        response = requests.get(f"{base_url}/api/chat")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Получение сообщений: {data['count']} сообщений")
        else:
            print(f"❌ Ошибка получения сообщений: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка тестирования получения сообщений: {e}")
    
    # Тест 3: Отправка тестового сообщения
    try:
        test_message = {
            "username": "TestUser",
            "message": "Привет! Это тестовое сообщение от " + datetime.now().strftime("%H:%M:%S"),
            "session_id": "test_session"
        }
        
        response = requests.post(
            f"{base_url}/api/chat",
            json=test_message,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сообщение отправлено: ID {data['message_id']}")
        else:
            print(f"❌ Ошибка отправки сообщения: {response.status_code}")
            print(f"   Ответ: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка тестирования отправки сообщения: {e}")
    
    # Тест 4: Повторное получение сообщений (должно быть 1)
    try:
        response = requests.get(f"{base_url}/api/chat?session_id=test_session")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ После отправки: {data['count']} сообщений")
            if data['count'] > 0:
                last_msg = data['messages'][-1]
                print(f"   Последнее: {last_msg['username']}: {last_msg['message']}")
        else:
            print(f"❌ Ошибка повторного получения: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка повторного тестирования: {e}")
    
    # Тест 5: Получение списка пользователей
    try:
        response = requests.get(f"{base_url}/api/chat/users?session_id=test_session")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Активные пользователи: {data['count']}")
            for user in data['users']:
                print(f"   - {user['username']} (последний раз: {user['last_seen']})")
        else:
            print(f"❌ Ошибка получения пользователей: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка тестирования пользователей: {e}")
    
    print("\n🎉 Тестирование завершено!")
    print("📱 Откройте http://localhost:8080/communication.html для тестирования интерфейса")

if __name__ == "__main__":
    test_chat_api()