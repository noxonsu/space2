#!/usr/bin/env python3
"""
Проверка найденных WhatsApp Business Account ID
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def check_waba_and_phones(waba_id):
    """Проверка WABA и получение номеров телефонов"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return False
    
    print(f"\n🔍 Проверка WABA ID: {waba_id}")
    print("-" * 50)
    
    # Сначала проверим сам WABA
    url = f"https://graph.facebook.com/v23.0/{waba_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа для WABA: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ WABA найден!")
            print(f"ID: {data.get('id')}")
            print(f"Название: {data.get('name')}")
            print(f"Статус: {data.get('account_review_status')}")
            
            # Теперь получим номера телефонов
            phones_url = f"https://graph.facebook.com/v23.0/{waba_id}/phone_numbers"
            
            print(f"\n📱 Получение номеров телефонов...")
            phones_response = requests.get(phones_url, headers=headers)
            print(f"Статус ответа для телефонов: {phones_response.status_code}")
            print(f"Тело ответа: {phones_response.text}")
            
            if phones_response.status_code == 200:
                phones_data = phones_response.json()
                
                if phones_data.get("data"):
                    print(f"\n✅ Найдено {len(phones_data['data'])} номеров телефонов:")
                    for i, phone in enumerate(phones_data['data'], 1):
                        print(f"  {i}. ID: {phone.get('id')}")
                        print(f"     Номер: {phone.get('display_phone_number')}")
                        print(f"     Статус: {phone.get('status')}")
                        print(f"     Качество: {phone.get('quality_rating')}")
                        print(f"     Проверен: {phone.get('code_verification_status')}")
                        print(f"     Имя: {phone.get('verified_name')}")
                        print()
                    return True
                else:
                    print("❌ Номера телефонов не найдены")
                    return False
            else:
                print(f"❌ Ошибка при получении номеров: {phones_response.status_code}")
                return False
                
        else:
            print(f"❌ WABA не найден: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке WABA: {e}")
        return False

def main():
    print("🚀 Проверка найденных WhatsApp Business Account ID")
    print("=" * 60)
    
    # ID найденные в granular_scopes
    waba_ids = ["1003776954875391", "718496087231012"]
    
    found_waba = False
    
    for waba_id in waba_ids:
        if check_waba_and_phones(waba_id):
            print(f"\n✅ Рабочий WABA ID найден: {waba_id}")
            found_waba = True
            break
    
    if not found_waba:
        print("\n❌ Ни один из WABA ID не работает")
    
    print("\n" + "=" * 60)
    print("✅ Проверка завершена")

if __name__ == "__main__":
    main()
