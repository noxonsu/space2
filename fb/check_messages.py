#!/usr/bin/env python3
"""
Просмотр отправленных сообщений WhatsApp Business API
"""

import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def get_messages_history(phone_number_id, limit=10):
    """Получение истории сообщений для номера телефона"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return None
    
    # Эндпоинт для получения сообщений
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Параметры запроса
    params = {
        'limit': limit,
        'fields': 'id,status,timestamp,type,text,recipient_id,message_status'
    }
    
    print(f"📋 Получение истории сообщений для номера ID: {phone_number_id}")
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ История сообщений получена")
            return data
        else:
            print(f"❌ Ошибка при получении истории: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return None

def get_conversation_analytics(phone_number_id):
    """Получение аналитики разговоров"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return None
    
    # Эндпоинт для аналитики
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/conversation_analytics"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Параметры для последних 7 дней
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    params = {
        'start': int(start_time.timestamp()),
        'end': int(end_time.timestamp()),
        'granularity': 'DAILY',
        'metric_types': 'COST,CONVERSATION'
    }
    
    print(f"\n📊 Получение аналитики разговоров...")
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Аналитика получена")
            return data
        else:
            print(f"❌ Ошибка при получении аналитики: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return None

def get_message_status(message_id):
    """Получение статуса конкретного сообщения"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return None
    
    # Эндпоинт для статуса сообщения
    url = f"https://graph.facebook.com/v23.0/{message_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔍 Получение статуса сообщения ID: {message_id}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Статус сообщения получен")
            return data
        else:
            print(f"❌ Ошибка при получении статуса: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return None

def get_waba_analytics(waba_id):
    """Получение аналитики WABA"""
    access_token = os.getenv('ACCESS_TOKEN')
    
    if not access_token:
        print("❌ ACCESS_TOKEN не найден")
        return None
    
    # Эндпоинт для аналитики WABA
    url = f"https://graph.facebook.com/v23.0/{waba_id}/message_analytics"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Параметры для последних 7 дней
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    params = {
        'start': int(start_time.timestamp()),
        'end': int(end_time.timestamp()),
        'granularity': 'DAILY'
    }
    
    print(f"\n📈 Получение аналитики WABA...")
    print(f"URL: {url}")
    print(f"Параметры: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Аналитика WABA получена")
            return data
        else:
            print(f"❌ Ошибка при получении аналитики WABA: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")
        return None

def main():
    print("🚀 Просмотр отправленных сообщений WhatsApp Business API")
    print("=" * 60)
    
    # ID из предыдущих тестов
    phone_number_id = "689775597552915"
    waba_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    # ID последнего отправленного сообщения
    last_message_id = "wamid.HBgLNDg1NzUwMTk5MjQVAgARGBJGM0VFOUJDNUZGMkRFQjkwQTcA"
    
    print(f"📞 Phone Number ID: {phone_number_id}")
    print(f"🏢 WABA ID: {waba_id}")
    print(f"💬 Message ID: {last_message_id}")
    
    # 1. Пытаемся получить историю сообщений
    print("\n" + "="*60)
    messages_data = get_messages_history(phone_number_id)
    
    # 2. Получаем аналитику разговоров
    print("\n" + "="*60)
    conversation_data = get_conversation_analytics(phone_number_id)
    
    # 3. Получаем статус конкретного сообщения
    print("\n" + "="*60)
    message_status = get_message_status(last_message_id)
    
    # 4. Получаем аналитику WABA
    print("\n" + "="*60)
    waba_analytics = get_waba_analytics(waba_id)
    
    print("\n" + "="*60)
    print("✅ Проверка завершена")
    
    # Выводим результаты
    print(f"\n📋 РЕЗУЛЬТАТЫ:")
    print(f"• История сообщений: {'✅' if messages_data else '❌'}")
    print(f"• Аналитика разговоров: {'✅' if conversation_data else '❌'}")
    print(f"• Статус сообщения: {'✅' if message_status else '❌'}")
    print(f"• Аналитика WABA: {'✅' if waba_analytics else '❌'}")

if __name__ == "__main__":
    main()
