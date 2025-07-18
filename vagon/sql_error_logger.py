"""
Модуль для логирования ошибок SQL запросов для последующего анализа и отладки.
"""
import os
import json
import datetime
from typing import Dict, Any, Optional


class SQLErrorLogger:
    """Класс для логирования ошибок SQL запросов."""
    
    def __init__(self, log_file_path: str = "sql_errors.log"):
        """
        Инициализация логгера.
        
        Args:
            log_file_path: Путь к файлу логов
        """
        self.log_file_path = log_file_path
        self._ensure_log_file_exists()
    
    def _ensure_log_file_exists(self):
        """Создает файл логов, если он не существует."""
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                f.write("# SQL Errors Log\n")
                f.write("# Format: JSON per line\n\n")
    
    def log_sql_error(self, 
                     user_query: str, 
                     generated_sql: str, 
                     error_message: str, 
                     error_type: str = "SQL_EXECUTION_ERROR",
                     additional_info: Optional[Dict[str, Any]] = None):
        """
        Логирует ошибку выполнения SQL запроса.
        
        Args:
            user_query: Оригинальный запрос пользователя
            generated_sql: Сгенерированный SQL запрос
            error_message: Сообщение об ошибке
            error_type: Тип ошибки
            additional_info: Дополнительная информация
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "error_type": error_type,
            "user_query": user_query,
            "generated_sql": generated_sql,
            "error_message": error_message,
            "additional_info": additional_info or {}
        }
        
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Ошибка при записи в лог: {e}")
    
    def log_llm_generation_error(self, 
                                user_query: str, 
                                error_message: str, 
                                llm_response: Optional[str] = None):
        """
        Логирует ошибку генерации SQL запроса LLM.
        
        Args:
            user_query: Оригинальный запрос пользователя
            error_message: Сообщение об ошибке
            llm_response: Ответ от LLM (если есть)
        """
        self.log_sql_error(
            user_query=user_query,
            generated_sql=llm_response or "NO_SQL_GENERATED",
            error_message=error_message,
            error_type="LLM_GENERATION_ERROR"
        )
    
    def get_recent_errors(self, limit: int = 10) -> list:
        """
        Возвращает последние ошибки из лога.
        
        Args:
            limit: Максимальное количество ошибок для возврата
            
        Returns:
            Список последних ошибок
        """
        try:
            errors = []
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Читаем с конца файла
            for line in reversed(lines):
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        error_entry = json.loads(line)
                        errors.append(error_entry)
                        if len(errors) >= limit:
                            break
                    except json.JSONDecodeError:
                        continue
                        
            return errors
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении лога: {e}")
            return []
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """
        Возвращает статистику по ошибкам.
        
        Returns:
            Словарь со статистикой
        """
        try:
            error_types = {}
            total_errors = 0
            
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            error_entry = json.loads(line)
                            error_type = error_entry.get('error_type', 'UNKNOWN')
                            error_types[error_type] = error_types.get(error_type, 0) + 1
                            total_errors += 1
                        except json.JSONDecodeError:
                            continue
                            
            return {
                "total_errors": total_errors,
                "error_types": error_types,
                "log_file": self.log_file_path
            }
        except FileNotFoundError:
            return {"total_errors": 0, "error_types": {}, "log_file": self.log_file_path}
        except Exception as e:
            return {"error": f"Ошибка при получении статистики: {e}"}


# Создаем глобальный экземпляр логгера
sql_error_logger = SQLErrorLogger()
