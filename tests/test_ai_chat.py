#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 Тестирование AI-ассистента в чате RULETTT
Проверяет работу нового AI endpoint
"""

import requests
import json
import sys
from datetime import datetime

# Конфигурация
API_BASE = 'http://localhost:5000'

def test_ai_responses():
    """Тестирует различные AI-ответы"""
    
    print("🤖 Тестирование AI-ассистента RULETTT")
    print("=" * 50)
    
    # Тестовые запросы
    test_cases = [
        'привет',
        'помощь', 
        'статистика',
        'стратегия',
        'команда',
        'api',
        'код',
        'ошибка',
        'как настроить команду',
        'расскажи про мартингейл',
        'что такое RULETTT'
    ]
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n{i}. Тест: '{message}'")
        
        try:
            response = requests.post(f'{API_BASE}/api/chat/ai', json={
                'message': message,
                'session_id': 'ai_test_session'
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ответ получен (ID: {data['message_id']})")
                print(f"🤖 AI: {data['ai_response'][:100]}...")
            else:
                print(f"❌ Ошибка: {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Ошибка: API сервер не запущен")
            print("   Запустите: python api_server.py")
            return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            
    return True

def test_chat_integration():
    """Проверяет интеграцию AI в обычный чат"""
    
    print("\n" + "=" * 50)
    print("🔄 Тестирование интеграции с чатом")
    
    try:
        # Отправляем AI запрос
        ai_response = requests.post(f'{API_BASE}/api/chat/ai', json={
            'message': 'помощь',
            'session_id': 'integration_test'
        })
        
        if ai_response.status_code != 200:
            print("❌ Ошибка AI запроса")
            return False
            
        # Проверяем что сообщение появилось в чате
        chat_response = requests.get(f'{API_BASE}/api/chat', params={
            'session_id': 'integration_test',
            'limit': 5
        })
        
        if chat_response.status_code == 200:
            messages = chat_response.json()['messages']
            ai_messages = [msg for msg in messages if '🤖' in msg['username']]
            
            if ai_messages:
                print(f"✅ AI сообщения в чате: {len(ai_messages)}")
                print(f"   Последнее: {ai_messages[-1]['message'][:50]}...")
                return True
            else:
                print("⚠️ AI сообщения не найдены в чате")
                return False
        else:
            print("❌ Ошибка загрузки чата")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка интеграции: {e}")
        return False

def test_api_health():
    """Проверяет доступность API"""
    
    try:
        response = requests.get(f'{API_BASE}/api/health')
        if response.status_code == 200:
            print("✅ API сервер работает")
            return True
        else:
            print(f"⚠️ API ответил с кодом: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API сервер недоступен")
        print("   Запустите: python api_server.py")
        return False

def main():
    """Основная функция тестирования"""
    
    print("🎯 RULETTT AI Chat Tester")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Проверяем API
    if not test_api_health():
        return
    
    # Тестируем AI ответы
    if test_ai_responses():
        print("\n✅ Тесты AI-ответов пройдены")
    else:
        print("\n❌ Ошибки в AI-ответах")
        
    # Тестируем интеграцию
    if test_chat_integration():
        print("✅ Интеграция с чатом работает")
    else:
        print("❌ Проблемы с интеграцией")
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование завершено")
    print("\n💡 Для использования:")
    print("   1. Откройте webapp/global_chat.html")
    print("   2. Введите @ai помощь")
    print("   3. Или нажмите кнопку 🤖 AI")

if __name__ == '__main__':
    main()