#!/usr/bin/env python3
"""
Поиск WhatsApp Business Account ID
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def find_whatsapp_business_accounts():
    """Поиск WhatsApp Business Account ID"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return []
    
    # Используем user ID из предыдущего запроса
    user_id = "24079729264973121"
    
    # Проверяем WhatsApp Business Account через пользователя
    url = f"https://graph.facebook.com/v23.0/{user_id}/accounts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Поиск аккаунтов пользователя...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                print("Найденные аккаунты:")
                for account in data['data']:
                    print(f"  • ID: {account.get('id')}")
                    print(f"    Название: {account.get('name')}")
                    print(f"    Категория: {account.get('category')}")
                    print()
            else:
                print("❌ Аккаунты не найдены")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при поиске аккаунтов: {e}")

def check_direct_waba_access():
    """Проверка прямого доступа к указанному WABA ID"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    if not access_token or not waba_id:
        print("❌ ACCESS_TOKEN или WHATSAPP_BUSINESS_ACCOUNT_ID не найден")
        return
    
    # Проверяем прямой доступ к WABA
    url = f"https://graph.facebook.com/v23.0/{waba_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔍 Проверка прямого доступа к WABA ID: {waba_id}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ WABA найден!")
            print(f"ID: {data.get('id')}")
            print(f"Название: {data.get('name')}")
            print(f"Статус: {data.get('account_review_status')}")
            print(f"Валюта: {data.get('currency')}")
        else:
            print(f"❌ Не удалось получить доступ к WABA: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке WABA: {e}")

def list_accessible_waba():
    """Список доступных WABA через Debug Token"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return
    
    # Используем debug token для получения информации о доступных ресурсах
    url = f"https://graph.facebook.com/v23.0/debug_token?input_token={access_token}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔍 Анализ токена для поиска доступных ресурсов...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Информация о токене получена")
            
            token_data = data.get('data', {})
            print(f"App ID: {token_data.get('app_id')}")
            print(f"User ID: {token_data.get('user_id')}")
            print(f"Действует до: {token_data.get('expires_at')}")
            
            # Проверяем scopes
            scopes = token_data.get('scopes', [])
            print(f"Разрешения: {', '.join(scopes)}")
            
        else:
            print(f"❌ Не удалось получить информацию о токене: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при анализе токена: {e}")

def main():
    print("🚀 Поиск WhatsApp Business Account ID")
    print("=" * 60)
    
    find_whatsapp_business_accounts()
    check_direct_waba_access()
    list_accessible_waba()
    
    print("\n" + "=" * 60)
    print("✅ Поиск завершен")

if __name__ == "__main__":
    main()
