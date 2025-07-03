#!/usr/bin/env python3
"""
Быстрая регистрация номера телефона с PIN
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def register_phone_with_pin(phone_number_id, pin):
    """Регистрация номера телефона для Cloud API с PIN"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return False
    
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/register"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные для регистрации
    data = {
        "messaging_product": "whatsapp",
        "pin": pin
    }
    
    print(f"🔐 Регистрация номера для Cloud API...")
    print(f"URL: {url}")
    print(f"Phone Number ID: {phone_number_id}")
    print(f"PIN: {pin}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"\nСтатус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Номер успешно зарегистрирован!")
            print(f"Результат: {result}")
            return True
        else:
            print(f"❌ Ошибка при регистрации: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return False

def main():
    print("🚀 Быстрая регистрация номера телефона с PIN")
    print("=" * 50)
    
    # Используем первый номер из предыдущих результатов
    phone_number_id = "689775597552915"  # ID первого номера +7 985 595-49-87
    
    # Запрашиваем PIN у пользователя
    pin = input("Введите PIN (6-значный код для двухфакторной аутентификации WhatsApp): ").strip()
    
    if not pin:
        print("❌ PIN не может быть пустым")
        return
    
    if len(pin) != 6 or not pin.isdigit():
        print("❌ PIN должен быть 6-значным числом")
        return
    
    print(f"\n📞 Регистрируем номер ID: {phone_number_id}")
    print(f"🔐 PIN: {pin}")
    
    success = register_phone_with_pin(phone_number_id, pin)
    
    if success:
        print("\n✅ Номер зарегистрирован! Теперь можно отправлять сообщения.")
    else:
        print("\n❌ Не удалось зарегистрировать номер.")

if __name__ == "__main__":
    main()
