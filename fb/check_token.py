#!/usr/bin/env python3
"""
Диагностический скрипт для проверки токена доступа и разрешений
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def check_token_info():
    """Проверка информации о токене доступа"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден в переменных окружения")
        return
    
    # Проверяем информацию о токене
    url = "https://graph.facebook.com/v23.0/me"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Проверка информации о токене доступа...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Токен действителен")
            print(f"ID: {data.get('id')}")
            print(f"Имя: {data.get('name')}")
        else:
            print(f"❌ Проблема с токеном: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке токена: {e}")

def check_token_permissions():
    """Проверка разрешений токена"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return
    
    # Проверяем разрешения токена
    url = "https://graph.facebook.com/v23.0/me/permissions"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 Проверка разрешений токена...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Разрешения получены")
            
            if data.get('data'):
                print("Доступные разрешения:")
                for perm in data['data']:
                    status = perm.get('status', 'unknown')
                    permission = perm.get('permission', 'unknown')
                    print(f"  • {permission}: {status}")
            else:
                print("❌ Нет данных о разрешениях")
        else:
            print(f"❌ Не удалось получить разрешения: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке разрешений: {e}")

def check_business_accounts():
    """Проверка доступных бизнес-аккаунтов"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return
    
    # Проверяем доступные бизнес-аккаунты
    url = "https://graph.facebook.com/v23.0/me/businesses"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 Проверка доступных бизнес-аккаунтов...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Бизнес-аккаунты получены")
            
            if data.get('data'):
                print("Доступные бизнес-аккаунты:")
                for business in data['data']:
                    print(f"  • ID: {business.get('id')}")
                    print(f"    Название: {business.get('name')}")
                    print(f"    Статус: {business.get('verification_status')}")
            else:
                print("❌ Нет доступных бизнес-аккаунтов")
        else:
            print(f"❌ Не удалось получить бизнес-аккаунты: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке бизнес-аккаунтов: {e}")

def main():
    print("🚀 Диагностика токена доступа и разрешений")
    print("=" * 50)
    
    check_token_info()
    check_token_permissions()
    check_business_accounts()
    
    print("\n" + "=" * 50)
    print("✅ Диагностика завершена")

if __name__ == "__main__":
    main()
