#!/usr/bin/env python3
"""
Финальный тестовый скрипт для отправки сообщения WhatsApp через Facebook Graph API
Эквивалент curl-запроса из исходного запроса
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

def send_whatsapp_message_curl_equivalent():
    """
    Отправляет сообщение WhatsApp через Facebook Graph API
    Эквивалент curl-запроса:
    curl -i -X POST \
        https://graph.facebook.com/v22.0/738116582708328/messages \
        -H 'Authorization: Bearer <access token>' \
        -H 'Content-Type: application/json' \
        -d '{"messaging_product": "whatsapp", "to": "79057448298", "type": "template", "template": {"name": "hello_world", "language": {"code": "en_US"}}}'
    """
    
    # Получаем токен доступа из переменной окружения
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден в переменных окружения")
        return False
    
    # Используем найденный рабочий Phone Number ID
    phone_number_id = "689775597552915"  # Первый номер из найденных
    
    # URL для отправки сообщения (используем v23.0 вместо v22.0)
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    
    # Заголовки запроса
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные сообщения - точная копия из исходного curl-запроса
    data = {
        "messaging_product": "whatsapp",
        "to": "48575019924",  # Обновленный номер получателя
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    
    print("🚀 Отправка сообщения WhatsApp (curl equivalent)")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print("=" * 60)
    
    try:
        # Отправляем POST запрос
        response = requests.post(url, headers=headers, json=data)
        
        # Выводим результат в стиле curl -i
        print(f"HTTP/1.1 {response.status_code} {response.reason}")
        
        # Выводим заголовки ответа
        for header_name, header_value in response.headers.items():
            print(f"{header_name}: {header_value}")
        
        print()  # Пустая строка перед телом ответа
        
        # Выводим тело ответа
        try:
            # Пытаемся отформатировать JSON
            response_json = response.json()
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            # Если не JSON, выводим как есть
            print(response.text)
        
        print("=" * 60)
        
        if response.status_code == 200:
            print("✅ Сообщение успешно отправлено!")
            return True
        else:
            print(f"❌ Ошибка при отправке сообщения: {response.status_code}")
            
            # Дополнительная информация об ошибке
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', 'Unknown error')
                    print(f"Детали ошибки: {error_message}")
                except:
                    pass
            
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return False

def main():
    print("🚀 Тестовая отправка сообщения WhatsApp")
    print("Эквивалент curl-запроса из исходного задания")
    print()
    
    success = send_whatsapp_message_curl_equivalent()
    
    print()
    if success:
        print("✅ Тест завершен успешно!")
    else:
        print("❌ Тест завершен с ошибкой!")
        print()
        print("💡 Возможные причины ошибок:")
        print("• Номер телефона не зарегистрирован для Cloud API")
        print("• Требуется PIN-код для регистрации номера")
        print("• Недостаточно разрешений для токена доступа")
        print("• Номер получателя не существует в WhatsApp")
        print("• Шаблон 'hello_world' не найден")

if __name__ == "__main__":
    main()
