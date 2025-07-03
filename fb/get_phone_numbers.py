#!/usr/bin/env python3
"""
Скрипт для получения списка номеров телефонов из WhatsApp Business Account
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

def get_phone_numbers():
    """Получение списка номеров телефонов из WhatsApp Business Account"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    print(f"Access Token: {access_token[:20]}..." if access_token else "Access Token: НЕ НАЙДЕН")
    print(f"WABA ID: {waba_id}")
    
    if not access_token or not waba_id:
        print("❌ Ошибка: ACCESS_TOKEN или WHATSAPP_BUSINESS_ACCOUNT_ID не найден")
        return
    
    url = f"https://graph.facebook.com/v23.0/{waba_id}/phone_numbers"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n📞 Выполняем запрос к: {url}")
    print(f"Headers: {headers}")
    
    try:
        response = requests.get(url, headers=headers)
        
        print(f"\n📊 Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Успешно получен ответ!")
            print(f"Данные: {json.dumps(data, indent=2)}")
            
            if data.get("data"):
                print(f"\n📱 Найденные номера телефонов:")
                for i, phone in enumerate(data["data"], 1):
                    print(f"  {i}. ID: {phone.get('id')}")
                    print(f"     Номер: {phone.get('display_phone_number')}")
                    print(f"     Статус: {phone.get('status')}")
                    print(f"     Verified: {phone.get('verified_name')}")
                    print()
            else:
                print("❌ Не найдены номера телефонов в ответе")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Детали ошибки: {json.dumps(error_data, indent=2)}")
            except:
                print("Не удалось распарсить ответ как JSON")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Получение списка номеров телефонов WhatsApp Business Account")
    get_phone_numbers()
