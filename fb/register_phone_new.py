#!/usr/bin/env python3
"""
Регистрация номера телефона для WhatsApp Cloud API
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def request_code(phone_number_id):
    """Запрос кода подтверждения для регистрации номера"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return False
    
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/request_code"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные для запроса кода
    data = {
        "code_method": "SMS"  # Можно также использовать "VOICE"
    }
    
    print(f"📱 Запрос кода подтверждения для номера ID: {phone_number_id}")
    print(f"URL: {url}")
    print(f"Метод: SMS")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Код подтверждения отправлен!")
            print(f"Результат: {result}")
            return True
        else:
            print(f"❌ Ошибка при запросе кода: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return False

def verify_code(phone_number_id, code):
    """Подтверждение кода для регистрации номера"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return False
    
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/verify_code"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные для подтверждения кода
    data = {
        "code": code
    }
    
    print(f"✅ Подтверждение кода для номера ID: {phone_number_id}")
    print(f"URL: {url}")
    print(f"Код: {code}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Код подтвержден!")
            print(f"Результат: {result}")
            return True
        else:
            print(f"❌ Ошибка при подтверждении кода: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return False

def register_phone(phone_number_id, pin):
    """Регистрация номера телефона для Cloud API"""
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
    print(f"PIN: {pin}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Статус ответа: {response.status_code}")
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
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("data"):
                print(f"✅ Найдено {len(data['data'])} номеров телефонов:")
                for i, phone in enumerate(data['data'], 1):
                    print(f"  {i}. ID: {phone.get('id')}")
                    print(f"     Номер: {phone.get('display_phone_number')}")
                    print(f"     Статус: {phone.get('status')}")
                    print(f"     Платформа: {phone.get('platform_type')}")
                    print(f"     Проверен: {phone.get('code_verification_status')}")
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

def main():
    print("🚀 Регистрация номера телефона для WhatsApp Cloud API")
    print("=" * 60)
    
    # Получаем список номеров
    phone_numbers = get_phone_numbers()
    if not phone_numbers:
        print("❌ Не найдены номера телефонов")
        return
    
    # Выбираем первый номер
    phone_number_id = phone_numbers[0]['id']
    phone_number = phone_numbers[0]['display_phone_number']
    
    print(f"\n📞 Будем регистрировать номер: {phone_number} (ID: {phone_number_id})")
    
    # Меню действий
    print("\n🔧 Доступные действия:")
    print("1. Запросить код подтверждения (SMS)")
    print("2. Подтвердить код")
    print("3. Зарегистрировать номер с PIN")
    print("4. Выйти")
    
    while True:
        choice = input("\nВыберите действие (1-4): ").strip()
        
        if choice == "1":
            print("\n1️⃣ Запрос кода подтверждения...")
            request_code(phone_number_id)
            
        elif choice == "2":
            code = input("Введите полученный код: ").strip()
            if code:
                print(f"\n2️⃣ Подтверждение кода: {code}")
                verify_code(phone_number_id, code)
            else:
                print("❌ Код не может быть пустым")
                
        elif choice == "3":
            pin = input("Введите PIN (6-значный): ").strip()
            if pin and len(pin) == 6 and pin.isdigit():
                print(f"\n3️⃣ Регистрация с PIN: {pin}")
                register_phone(phone_number_id, pin)
            else:
                print("❌ PIN должен быть 6-значным числом")
                
        elif choice == "4":
            print("👋 Выход")
            break
            
        else:
            print("❌ Неверный выбор. Используйте 1-4")

if __name__ == "__main__":
    main()
