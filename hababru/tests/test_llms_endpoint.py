#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/space2/hababru')

from src.backend.main import create_app
import requests
import time
import subprocess
from threading import Thread

def run_server():
    """Запускает Flask сервер в отдельном потоке"""
    app = create_app()
    app.run(host='127.0.0.1', port=5555, debug=False)

def test_llms_endpoint():
    """Тестирует /llms.txt эндпоинт"""
    
    # Запускаем сервер в фоне
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Ждем запуска сервера
    time.sleep(3)
    
    try:
        response = requests.get('http://127.0.0.1:5555/llms.txt', timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print("\n=== LLMS.TXT RESPONSE ===")
        content = response.text
        
        # Показываем секцию продуктов
        lines = content.split('\n')
        in_products_section = False
        for line in lines:
            if line.strip() == "## Продукты":
                in_products_section = True
                print(line)
                continue
            elif line.startswith("## ") and in_products_section:
                print(line)
                break
            elif in_products_section:
                print(line)
                
        # Проверяем что новый продукт есть
        if "crm_automation" in content:
            print("\n✅ Новый продукт 'crm_automation' найден в llms.txt!")
        else:
            print("\n❌ Новый продукт 'crm_automation' НЕ найден в llms.txt")
            
        return True
        
    except Exception as e:
        print(f"Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    test_llms_endpoint()
