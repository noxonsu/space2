#!/usr/bin/env python3
"""
Отправка шаблона сообщения dashonoutrog_login
"""

import os
import requests
import json
import random
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def send_template_message(phone_number_id, to_number, verification_code):
    """Отправка шаблона dashonoutrog_login с кодом верификации"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return False
    
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные для отправки шаблона
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": "dashonoutrog_login",
            "language": {
                "code": "en"  # Язык шаблона
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": verification_code
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": verification_code
                        }
                    ]
                }
            ]
        }
    }
    
    print(f"📤 Отправка шаблона аутентификации...")
    print(f"URL: {url}")
    print(f"Получатель: {to_number}")
    print(f"Код верификации: {verification_code}")
    print(f"Данные: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"\nСтатус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')
            contact_wa_id = result.get('contacts', [{}])[0].get('wa_id')
            
            print("✅ Шаблон успешно отправлен!")
            print(f"Message ID: {message_id}")
            print(f"WhatsApp ID получателя: {contact_wa_id}")
            return True
        else:
            print(f"❌ Ошибка при отправке шаблона: {response.status_code}")
            
            # Дополнительная информация об ошибке
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                error_details = error_data.get('error', {}).get('error_data', {}).get('details', 'No details')
                print(f"Детали ошибки: {error_message}")
                print(f"Подробности: {error_details}")
            except:
                pass
            
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return False

def get_phone_numbers():
    """Получение номеров телефонов"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    url = f"https://graph.facebook.com/v23.0/{waba_id}/phone_numbers"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    except:
        return []

def main():
    print("🚀 Отправка шаблона аутентификации dashonoutrog_login")
    print("=" * 60)
    
    # Получаем номера телефонов
    phone_numbers = get_phone_numbers()
    if not phone_numbers:
        print("❌ Не найдены номера телефонов")
        return
    
    # Используем первый зарегистрированный номер
    phone_number_id = None
    for phone in phone_numbers:
        if phone.get('platform_type') == 'CLOUD_API':
            phone_number_id = phone['id']
            sender_number = phone['display_phone_number']
            print(f"📞 Отправитель: {sender_number} (ID: {phone_number_id})")
            break
    
    if not phone_number_id:
        print("❌ Не найден зарегистрированный номер для Cloud API")
        return
    
    # Параметры отправки
    recipient_number = "48575019924"  # Номер получателя
    verification_code = str(random.randint(100000, 999999))  # Генерируем 6-значный код
    
    print(f"📨 Получатель: {recipient_number}")
    print(f"🔐 Код верификации: {verification_code}")
    
    # Отправляем шаблон
    success = send_template_message(phone_number_id, recipient_number, verification_code)
    
    if success:
        print("\n✅ Шаблон отправлен успешно!")
        print("\n💡 Информация о шаблоне:")
        print("• Название: dashonoutrog_login")
        print("• Категория: AUTHENTICATION")
        print("• Язык: en")
        print("• Текст: *{код}* is your verification code. For your security, do not share this code.")
        print("• Кнопка: Copy code (с автоматической вставкой кода)")
    else:
        print("\n❌ Не удалось отправить шаблон")

if __name__ == "__main__":
    main()
