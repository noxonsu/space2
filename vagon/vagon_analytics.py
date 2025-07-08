import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class VagonAnalytics:
    def __init__(self):
        self.connection_string = self._build_connection_string()
        self.connection = None
        
    def _build_connection_string(self):
        """Строим строку подключения к базе данных"""
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        # Используем одну из баз данных, например, GRNG/GRMU
        database = os.getenv('DB_NAME_GRNG', 'GRNG') 
        driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
        
        return f"DRIVER={{{driver}}};SERVER={host},{port};DATABASE={database};UID={user};PWD={password};"
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            print("Успешное подключение к базе данных!")
            return True
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return False
    
    def disconnect(self):
        """Отключение от базы данных"""
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")
    
    def execute_query(self, query, params=None):
        """
        Выполнение SQL запроса.
        Эта функция принимает SQL-запрос, сгенерированный LLM, и выполняет его.
        """
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            print(f"Выполнение запроса: {query}")
            if params:
                print(f"С параметрами: {params}")
                
            df = pd.read_sql(query, self.connection, params=params)
            return df
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Ошибка SQL: {sqlstate} - {ex}")
            return f"Ошибка при выполнении SQL запроса: {ex}"
        except Exception as e:
            print(f"Неизвестная ошибка выполнения запроса: {e}")
            return f"Неизвестная ошибка: {e}"
