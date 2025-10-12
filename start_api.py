"""
Простой запуск API сервера без debug режима
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_server import app

if __name__ == '__main__':
    print("🎲 Запуск RULETTT API сервера (продакшн режим)...")
    print("📡 API доступен на: http://localhost:5000")
    print("💬 Чат API готов к работе!")
    
    app.run(debug=False, host='0.0.0.0', port=5000)