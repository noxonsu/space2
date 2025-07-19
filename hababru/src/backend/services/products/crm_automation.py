import os
import json
from typing import Dict, Any, Optional
from ..products import BaseProduct
from ..llm_service import LLMService
from ..parsing_service import ParsingService
from ..cache_service import CacheService
from ..product_data_loader import ProductDataLoader

class CrmAutomationProduct(BaseProduct):
    def __init__(self, llm_service: LLMService):
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("crm_automation")
        
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
            # Логика демо-выполнения для CRM Автоматизации
            
            demo_input = demo_params.get("input", "Пример клиентского запроса: 'Хочу узнать статус заказа.'")
            
            # Имитация работы LLM для генерации демо-результата
            prompt = f"Сгенерируйте демо-результат для CRM Автоматизации на основе запроса: '{demo_input}'. Опишите, как ИИ обрабатывает запрос."
            llm_response = self.llm_service.generate_text(prompt)
            
            return {
                "status": "success",
                "result": f"Демо-результат CRM Автоматизации: {llm_response}",
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
            # Основная логика обработки для CRM Автоматизации
            
            customer_data = form_data.get('customer_data')
            
            if not customer_data:
                raise ValueError("Необходимо предоставить данные клиента.")
            
            log_messages = []
            log_messages.append(f"Начат процесс обработки данных клиента: {customer_data}")
            
            log_messages.append("Имитация автоматического заполнения карточки клиента.")
            log_messages.append("Имитация предиктивной аналитики продаж.")
            
            result_message = "Данные клиента обработаны, карточка обновлена, прогноз продаж сгенерирован."
            
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
            "CRM автоматизация",
            "автоматизация продаж",
            "ИИ для CRM",
            "умный помощник CRM",
            "автоматизация бизнес-процессов"
        ])
