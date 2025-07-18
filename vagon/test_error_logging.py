#!/usr/bin/env python3
"""
Тест системы логирования ошибок SQL.
"""
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sql_error_logger import sql_error_logger

def test_error_logging():
    """Тестирует систему логирования ошибок."""
    print("=== ТЕСТ СИСТЕМЫ ЛОГИРОВАНИЯ ОШИБОК ===")
    
    # Тестируем логирование ошибки SQL
    print("1. Записываем тестовую ошибку SQL...")
    sql_error_logger.log_sql_error(
        user_query="Какое количество вагонов компании Еврохим было выгружено за последний месяц",
        generated_sql="SELECT COUNT(*) AS [Количество вагонов] FROM [GRNG/GRMU].[dbo].[VagonUnloading] WHERE [Грузовладелец] = 'Еврохим'",
        error_message="('22018', '[22018] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Operand type clash: date is incompatible with int (206) (SQLExecDirectW)')",
        error_type="SQL_EXECUTION_ERROR",
        additional_info={
            "database": "GRNG/GRMU", 
            "table": "VagonUnloading"
        }
    )
    
    # Тестируем логирование ошибки LLM
    print("2. Записываем тестовую ошибку LLM...")
    sql_error_logger.log_llm_generation_error(
        user_query="Покажи мне все данные",
        error_message="HuggingFace API Error: Rate limit exceeded"
    )
    
    # Проверяем результаты
    print("3. Проверяем результаты...")
    errors = sql_error_logger.get_recent_errors(limit=5)
    print(f"   Найдено ошибок: {len(errors)}")
    
    for i, error in enumerate(errors):
        print(f"   Ошибка {i+1}:")
        print(f"     Тип: {error.get('error_type')}")
        print(f"     Запрос: {error.get('user_query')[:50]}...")
        print(f"     Время: {error.get('timestamp')}")
    
    # Получаем статистику
    print("4. Статистика ошибок:")
    stats = sql_error_logger.get_error_statistics()
    print(f"   Всего ошибок: {stats.get('total_errors', 0)}")
    print(f"   По типам: {stats.get('error_types', {})}")
    
    print("=== ТЕСТ ЗАВЕРШЕН ===")

if __name__ == "__main__":
    test_error_logging()
