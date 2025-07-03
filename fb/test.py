#!/usr/bin/env python3
"""
Тестовый скрипт для отправки сообщения WhatsApp через Facebook Graph API
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

def get_phone_numbers():
    """Получение всех номеров телефонов из WhatsApp Business Account"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    if not access_token or not waba_id:
        print("Ошибка: ACCESS_TOKEN или WHATSAPP_BUSINESS_ACCOUNT_ID не найден")
        return []
    
    url = f"https://graph.facebook.com/v23.0/{waba_id}/phone_numbers"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"🔍 Запрос к API для получения номеров телефонов...")
    print(f"URL: {url}")
    print(f"WABA ID: {waba_id}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("data"):
                print(f"\n✅ Найдено {len(data['data'])} номеров телефонов:")
                for i, phone in enumerate(data['data'], 1):
                    print(f"  {i}. ID: {phone.get('id')}")
                    print(f"     Номер: {phone.get('display_phone_number')}")
                    print(f"     Статус: {phone.get('status')}")
                    print(f"     Качество: {phone.get('quality_rating')}")
                    print(f"     Проверен: {phone.get('code_verification_status')}")
                    print(f"     Имя: {phone.get('verified_name')}")
                    print()
                return data['data']
            else:
                print("❌ Не найдены номера телефонов в ответе")
                return []
        else:
            print(f"❌ Ошибка HTTP {response.status_code}: {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return []

def send_whatsapp_message():
    """
    Отправляет сообщение WhatsApp через Facebook Graph API
    """
    # Получаем токен доступа из переменной окружения
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("Ошибка: ACCESS_TOKEN не найден в переменных окружения")
        return False
    
    # Получаем список номеров телефонов
    phone_numbers = get_phone_numbers()
    if not phone_numbers:
        print("❌ Не найдены номера телефонов")
        return False
    
    # Используем первый доступный номер
    phone_number_id = phone_numbers[0]['id']
    print(f"📞 Используем номер телефона ID: {phone_number_id}")
    
    # URL для отправки сообщения
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    
    # Заголовки запроса
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные сообщения (простое текстовое сообщение)
    data = {
        "messaging_product": "whatsapp",
        "to": "48575019924",
        "type": "text",
        "text": {
            "body": "Привет! Это тестовое сообщение от WhatsApp Business API 🚀"
        }
    }
    
    try:
        # Отправляем POST запрос
        print("Отправляем сообщение...")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=data)
        
        # Выводим результат
        print(f"\nСтатус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            print("✅ Сообщение успешно отправлено!")
            return True
        else:
            print(f"❌ Ошибка при отправке сообщения: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Запуск тестовой отправки сообщения WhatsApp")
    success = send_whatsapp_message()
    
    if success:
        print("\n✅ Тест завершен успешно!")
    else:
        print("\n❌ Тест завершен с ошибкой!")
