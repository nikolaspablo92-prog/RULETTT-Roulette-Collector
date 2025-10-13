"""
Проверка доступных routes в API
"""
import requests

print("🔍 Проверка API endpoints...")
print()

# Проверка базовых endpoints
endpoints = [
    '/api/health',
    '/api/spins',
    '/api/statistics',
    '/api/logs',
    '/api/logs/stats',
    '/api/errors/unresolved',
    '/api/events'
]

for endpoint in endpoints:
    url = f'http://localhost:5000{endpoint}'
    try:
        response = requests.get(url, timeout=2)
        print(f"✅ {endpoint:30} - {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint:30} - Connection Error")
    except Exception as e:
        print(f"⚠️  {endpoint:30} - {e}")

print()
print("💡 Если видите 404 на новых endpoints, перезапустите API сервер")
