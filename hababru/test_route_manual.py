#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

from src.backend.main import create_app

def test_llms_txt_route():
    print("Создаем Flask приложение...")
    app = create_app()
    
    print("Тестируем маршрут /llms.txt...")
    with app.test_client() as client:
        response = client.get('/llms.txt')
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Content-Type: {response.content_type}")
        
        if response.status_code == 200:
            content = response.get_data(as_text=True)
            print(f"Длина контента: {len(content)} символов")
            print("=" * 60)
            print(content[:800])  # Первые 800 символов
            print("..." if len(content) > 800 else "")
            print("=" * 60)
            
            # Проверяем основные элементы
            if content.startswith('# HababRu'):
                print("✓ Заголовок корректный")
            else:
                print("✗ Проблема с заголовком")
                
            if '> B2B-сервис' in content:
                print("✓ Описание найдено")
            else:
                print("✗ Описание не найдено")
                
            if '## Документация' in content:
                print("✓ Секция документации найдена")
            else:
                print("✗ Секция документации не найдена")
                
            if '## Продукты' in content:
                print("✓ Секция продуктов найдена")
            else:
                print("✗ Секция продуктов не найдена")
        else:
            print(f"Ошибка: получен статус {response.status_code}")
            error_content = response.get_data(as_text=True)
            print(f"Содержимое ошибки: {error_content[:200]}")
    
    print("\nТест маршрута завершен!")

if __name__ == "__main__":
    test_llms_txt_route()
