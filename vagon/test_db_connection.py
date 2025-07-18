#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения к базе данных SQL Server
"""
import os
import pyodbc
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_connection():
    """Тестирует подключение к базе данных."""
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    print(f"Тестирование подключения к SQL Server:")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Driver: {driver}")
    print("-" * 50)
    
    # Тестируем подключение к разным базам данных
    databases = ['GRNG/GRMU', 'OperativeReport', 'ShipmentsToThePort']
    
    for db_name in databases:
        print(f"\nТестирование подключения к базе: {db_name}")
        connection_string = f"DRIVER={{{driver}}};SERVER={host},{port};DATABASE={db_name};UID={user};PWD={password};TrustServerCertificate=yes;"
        
        try:
            connection = pyodbc.connect(connection_string, timeout=10)
            cursor = connection.cursor()
            
            # Простой тест запрос
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()
            print(f"✅ Подключение к {db_name} успешно!")
            print(f"   Версия SQL Server: {version[0][:50]}...")
            
            cursor.close()
            connection.close()
            
        except pyodbc.Error as e:
            print(f"❌ Ошибка подключения к {db_name}: {e}")
        except Exception as e:
            print(f"❌ Неожиданная ошибка для {db_name}: {e}")

if __name__ == "__main__":
    test_connection()
