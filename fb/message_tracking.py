#!/usr/bin/env python3
"""
Альтернативные способы отслеживания сообщений WhatsApp Business API
"""

import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_webhooks_info():
    """Проверка настроек webhooks"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    url = f"https://graph.facebook.com/v23.0/{waba_id}/subscribed_apps"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print("📡 Проверка настроек webhooks...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def get_analytics_data():
    """Получение доступной аналитики"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    # Пробуем разные варианты аналитики
    endpoints = [
        f"https://graph.facebook.com/v23.0/{waba_id}/analytics",
        f"https://graph.facebook.com/v23.0/{waba_id}/insights",
        f"https://graph.facebook.com/v23.0/{waba_id}?fields=analytics"
    ]
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    for url in endpoints:
        print(f"\n📊 Проверка аналитики: {url}")
        try:
            response = requests.get(url, headers=headers)
            print(f"Статус: {response.status_code}")
            print(f"Ответ: {response.text[:300]}...")
        except Exception as e:
            print(f"Ошибка: {e}")

def get_account_info():
    """Получение подробной информации об аккаунте"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    url = f"https://graph.facebook.com/v23.0/{waba_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Пробуем получить различные поля
    params = {
        'fields': 'id,name,account_review_status,analytics,currency,message_template_namespace,on_behalf_of_business_info,primary_business_location,timezone_id'
    }
    
    print(f"\n🏢 Информация об аккаунте...")
    print(f"URL: {url}")
    print(f"Поля: {params['fields']}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def check_message_templates():
    """Проверка доступных шаблонов сообщений"""
    access_token = os.getenv('ACCESS_TOKEN')
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    url = f"https://graph.facebook.com/v23.0/{waba_id}/message_templates"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n📝 Шаблоны сообщений...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                print(f"✅ Найдено {len(data['data'])} шаблонов")
                for template in data['data']:
                    print(f"  • {template.get('name')} ({template.get('status')})")
            return data
        else:
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def main():
    print("🚀 Альтернативные способы отслеживания сообщений")
    print("=" * 60)
    
    print("\n📌 ВАЖНО: WhatsApp Business API не предоставляет прямой доступ к истории сообщений!")
    print("Для отслеживания сообщений рекомендуется:")
    print("1. Использовать webhooks для получения статусов доставки")
    print("2. Вести собственную базу данных отправленных сообщений") 
    print("3. Использовать аналитику для общей статистики")
    
    # Проверяем доступную информацию
    get_webhooks_info()
    get_analytics_data()
    get_account_info()
    check_message_templates()
    
    print("\n" + "=" * 60)
    print("✅ Проверка завершена")
    
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("• Настройте webhook для получения статусов сообщений")
    print("• Сохраняйте информацию о сообщениях в собственной БД")
    print("• Используйте Message ID для отслеживания конкретных сообщений")
    print("• Последнее отправленное сообщение ID: wamid.HBgLNDg1NzUwMTk5MjQVAgARGBJGM0VFOUJDNUZGMkRFQjkwQTcA")

if __name__ == "__main__":
    main()
