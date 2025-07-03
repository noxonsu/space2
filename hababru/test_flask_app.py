#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/space2/hababru')

def test_app_startup():
    # Устанавливаем переменные окружения для тестирования
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
    os.environ['TELEGRAM_CHANNEL'] = '@aideaxondemos'
    os.environ['DEEPSEEK_API_KEY'] = 'test_key'
    
    try:
        # Импортируем Flask приложение
        from src.backend.main import app
        
        with app.test_client() as client:
            # Тестируем главную страницу
            response = client.get('/')
            print(f"Главная страница: статус {response.status_code}")
            
            # Тестируем llms.txt
            response = client.get('/llms.txt')
            print(f"llms.txt: статус {response.status_code}")
            if response.status_code == 200:
                print(f"Длина llms.txt: {len(response.data)} байт")
                
            # Тестируем продуктовые страницы
            response = client.get('/analiz-dogovorov')
            print(f"Анализ договоров: статус {response.status_code}")
            
            response = client.get('/analiz-novostej')
            print(f"Анализ новостей: статус {response.status_code}")
            
        print("✅ Flask приложение успешно запускается!")
        
    except Exception as e:
        print(f"❌ Ошибка запуска Flask приложения: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_app_startup()
