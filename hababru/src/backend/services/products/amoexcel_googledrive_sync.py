import os
import json
from typing import Dict, Any, Optional
from ..products import BaseProduct
from ..llm_service import LLMService
from ..parsing_service import ParsingService
from ..cache_service import CacheService
from ..product_data_loader import ProductDataLoader

class AmoexcelGoogledriveSyncProduct(BaseProduct):
    def __init__(self, llm_service: LLMService):
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("amoexcel_googledrive_sync")
        
        super().__init__(
            product_id=self.product_data["product_id"],
            name=self.product_data["name"],
            description=self.product_data["description"]
        )
        
        self.llm_service = llm_service
    
    def get_demo_content(self) -> Dict[str, Any]:
        """Возвращает демо-контент для отображения на странице"""
        return self.product_data.get("demo_data", {})
    
    def execute_demo(self, demo_params: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполняет демо-версию продукта"""
        try:
            # Логика демо-выполнения для AmoexcelGoogledriveSync
            # В реальном приложении здесь была бы интеграция с AMOCRM, Excel и Google Drive
            
            demo_input = self.product_data.get("demo_data", {}).get("sample_input", "Пример данных для синхронизации.")
            
            # Имитация работы LLM для генерации демо-результата
            prompt = f"Сгенерируйте демо-результат для интеграции AMOCRM, Excel и Google Drive на основе следующих данных: {demo_input}. Опишите шаги и результат."
            llm_response = self.llm_service.generate_text(prompt)
            
            return {
                "status": "success",
                "result": f"Демо-результат интеграции: {llm_response}",
                "demo": True
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "demo": True
            }
    
    def process_upload(self, files: Dict, form_data: Dict) -> Dict[str, Any]:
        """Обрабатывает загруженные файлы и данные формы"""
        try:
            # Основная логика обработки для AmoexcelGoogledriveSync
            # В реальном приложении здесь была бы обработка файлов Excel и взаимодействие с AMOCRM/Google Drive
            
            lead_id = form_data.get('lead_id')
            action = form_data.get('action')
            
            if not lead_id or not action:
                raise ValueError("Необходимо указать ID лида и действие.")
            
            log_messages = []
            log_messages.append(f"Начат процесс для лида ID: {lead_id}, действие: {action}")
            
            if action == "экспорт":
                log_messages.append("Шаг 1: Экспорт лидов из AMOCRM в Excel (имитация).")
                # Здесь была бы реальная логика экспорта
                log_messages.append("Шаг 2: Сохранение Excel файла на Google Drive (имитация).")
                # Здесь была бы реальная логика сохранения
                result_message = "Лиды успешно экспортированы и сохранены."
            elif action == "импорт" or action == "обновление":
                if not files.get('main_file'):
                    raise ValueError("Для импорта/обновления необходим файл Excel.")
                
                log_messages.append("Шаг 1: Загрузка и парсинг Excel файла (имитация).")
                # Здесь была бы реальная логика парсинга
                
                log_messages.append("Шаг 2: Обработка данных на локальном компьютере (имитация).")
                # Здесь была бы реальная логика обработки
                
                log_messages.append("Шаг 3: Обновление карточек лидов в AMOCRM через API (имитация).")
                # Здесь была бы реальная логика обновления
                result_message = "Данные успешно обработаны и обновлены в AMOCRM."
            else:
                raise ValueError("Неизвестное действие.")
            
            log_messages.append("Процесс завершен.")
            
            return {
                "status": "success",
                "result": result_message,
                "log": "\n".join(log_messages),
                "demo": False
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "demo": False
            }
    
    def get_product_info(self) -> Dict[str, Any]:
        """Возвращает информацию о продукте"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "key_benefits": self.product_data.get("product_info", {}).get("key_benefits", []),
            "target_audience": self.product_data.get("product_info", {}).get("target_audience", []),
            "use_cases": self.product_data.get("demo_data", {}).get("use_cases", []),
            "demo_available": True
        }
    
    def get_seo_keywords(self) -> list:
        """Возвращает SEO ключевые слова для продукта"""
        return self.product_data.get("seo_keywords", [
            "AMOCRM интеграция",
            "Excel автоматизация", 
            "Google Drive синхронизация",
            "CRM автоматизация",
            "интеграция систем"
        ])
