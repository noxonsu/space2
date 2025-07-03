#!/usr/bin/env python3
"""
Простая проверка эндпоинтов для просмотра сообщений
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def check_endpoint(url, description):
    """Проверка эндпоинта"""
    access_token = os.getenv('ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔍 {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text[:500]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def main():
    print("🚀 Проверка эндпоинтов для просмотра сообщений")
    
    phone_id = "689775597552915"
    waba_id = "718496087231012"
    message_id = "wamid.HBgLNDg1NzUwMTk5MjQVAgARGBJGM0VFOUJDNUZGMkRFQjkwQTcA"
    
    # Проверяем различные эндпоинты
    endpoints = [
        (f"https://graph.facebook.com/v23.0/{phone_id}/messages", "История сообщений телефона"),
        (f"https://graph.facebook.com/v23.0/{waba_id}/messages", "История сообщений WABA"),
        (f"https://graph.facebook.com/v23.0/{message_id}", "Информация о сообщении"),
        (f"https://graph.facebook.com/v23.0/{phone_id}/conversation_analytics", "Аналитика разговоров"),
        (f"https://graph.facebook.com/v23.0/{waba_id}/message_analytics", "Аналитика сообщений"),
    ]
    
    for url, desc in endpoints:
        check_endpoint(url, desc)
    
    print("\n✅ Проверка завершена")

if __name__ == "__main__":
    main()
