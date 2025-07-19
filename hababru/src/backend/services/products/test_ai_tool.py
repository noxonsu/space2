import os
import json
from typing import Dict, Any, Optional
from ..products import BaseProduct
from ..llm_service import LLMService
from ..parsing_service import ParsingService
from ..cache_service import CacheService
from ..product_data_loader import ProductDataLoader

class TestAiToolProduct(BaseProduct):
    def __init__(self, llm_service: LLMService):
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("test_ai_tool")
        
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
            # Логика демо-выполнения для Тестового AI Инструмента
            
            input_text = demo_params.get("input_text", "Пример текста для обработки.")
            
            # Имитация работы LLM для генерации демо-результата
            prompt = f"Сгенерируйте демо-результат для тестового AI инструмента на основе текста: '{input_text}'. Опишите, как инструмент обрабатывает текст."
            llm_response = self.llm_service.generate_text(prompt)
            
            return {
                "status": "success",
                "result": f"Демо-результат Тестового AI Инструмента: {llm_response}",
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
            # Основная логика обработки для Тестового AI Инструмента
            
            input_text = form_data.get('input_text')
            
            if not input_text:
                raise ValueError("Необходимо предоставить входной текст.")
            
            log_messages = []
            log_messages.append(f"Начат процесс обработки текста: {input_text}")
            
            log_messages.append("Имитация обработки текста AI инструментом.")
            
            result_message = "Текст успешно обработан AI инструментом."
            
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
            "тестовый ИИ инструмент",
            "демо AI",
            "автоматизация процессов",
            "ИИ решения",
            "AI для бизнеса"
        ])
