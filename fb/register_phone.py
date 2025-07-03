#!/usr/bin/env python3
"""
Скрипт для регистрации номера телефона для Cloud API
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def check_phone_registration_status(phone_id):
    """Проверка статуса регистрации номера"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return None
    
    url = f"https://graph.facebook.com/v23.0/{phone_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"🔍 Проверка статуса регистрации номера {phone_id}...")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Информация о номере получена:")
            print(f"ID: {data.get('id')}")
            print(f"Номер: {data.get('display_phone_number')}")
            print(f"Статус: {data.get('status')}")
            print(f"Платформа: {data.get('platform_type')}")
            print(f"Проверен: {data.get('code_verification_status')}")
            print(f"Качество: {data.get('quality_rating')}")
            print(f"Имя: {data.get('verified_name')}")
            
            # Проверяем, зарегистрирован ли номер для Cloud API
            if data.get('platform_type') == 'CLOUD_API':
                print("✅ Номер зарегистрирован для Cloud API")
                return True
            else:
                print(f"❌ Номер НЕ зарегистрирован для Cloud API (platform_type: {data.get('platform_type')})")
                return False
        else:
            print(f"❌ Ошибка при получении информации о номере: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке номера: {e}")
        return False

def register_phone_for_cloud_api(phone_id):
    """Попытка регистрации номера для Cloud API"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return False
    
    url = f"https://graph.facebook.com/v23.0/{phone_id}/register"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Данные для регистрации
    data = {
        "messaging_product": "whatsapp"
    }
    
    print(f"🔄 Попытка регистрации номера {phone_id} для Cloud API...")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Статус ответа: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            print("✅ Номер успешно зарегистрирован для Cloud API!")
            return True
        else:
            print(f"❌ Ошибка при регистрации номера: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при регистрации номера: {e}")
        return False

def main():
    print("🚀 Проверка и регистрация номеров для Cloud API")
    print("=" * 60)
    
    # ID номеров из предыдущего запроса
    phone_ids = ["689775597552915", "720664694455158"]
    
    for phone_id in phone_ids:
        print(f"\n{'='*60}")
        
        # Проверяем статус регистрации
        is_registered = check_phone_registration_status(phone_id)
        
        if is_registered is False:
            print(f"\n🔄 Номер не зарегистрирован. Попытка регистрации...")
            register_phone_for_cloud_api(phone_id)
            
            # Проверяем статус после регистрации
            print(f"\n🔍 Повторная проверка статуса...")
            check_phone_registration_status(phone_id)
        elif is_registered is True:
            print(f"✅ Номер уже зарегистрирован для Cloud API")
    
    print("\n" + "=" * 60)
    print("✅ Проверка завершена")

if __name__ == "__main__":
    main()
