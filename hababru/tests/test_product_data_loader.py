"""
Тесты для загрузчика данных продуктов
"""

import pytest
import tempfile
import os
import yaml
from pathlib import Path
from src.backend.services.product_data_loader import ProductDataLoader

class TestProductDataLoader:
    
    def setup_method(self):
        """Настройка для каждого теста"""
        # Создаем временную директорию для тестовых данных
        self.temp_dir = tempfile.mkdtemp()
        self.loader = ProductDataLoader(self.temp_dir)
        
        # Создаем тестовый файл продукта
        self.test_product_data = {
            "product_id": "test_product",
            "name": "Тестовый продукт",
            "description": "Описание тестового продукта",
            "demo_data": {
                "test_field": "test_value"
            },
            "product_info": {
                "key_benefits": ["Польза 1", "Польза 2"]
            }
        }
        
        test_file_path = Path(self.temp_dir) / "test_product.yaml"
        with open(test_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.test_product_data, f, allow_unicode=True)
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_product_data_success(self):
        """Тест успешной загрузки данных продукта"""
        data = self.loader.load_product_data("test_product")
        
        assert data["product_id"] == "test_product"
        assert data["name"] == "Тестовый продукт"
        assert data["description"] == "Описание тестового продукта"
        assert data["demo_data"]["test_field"] == "test_value"
    
    def test_load_product_data_file_not_found(self):
        """Тест обработки ошибки при отсутствии файла"""
        with pytest.raises(FileNotFoundError):
            self.loader.load_product_data("nonexistent_product")
    
    def test_get_available_products(self):
        """Тест получения списка доступных продуктов"""
        products = self.loader.get_available_products()
        
        assert "test_product" in products
        assert len(products) == 1
    
    def test_load_all_products(self):
        """Тест загрузки всех продуктов"""
        all_products = self.loader.load_all_products()
        
        assert "test_product" in all_products
        assert all_products["test_product"]["name"] == "Тестовый продукт"
    
    def test_validate_product_data_success(self):
        """Тест успешной валидации данных продукта"""
        is_valid = self.loader.validate_product_data(self.test_product_data)
        assert is_valid is True
    
    def test_validate_product_data_missing_field(self):
        """Тест валидации с отсутствующим обязательным полем"""
        invalid_data = {"name": "Продукт", "description": "Описание"}
        # Отсутствует product_id
        
        with pytest.raises(ValueError) as exc_info:
            self.loader.validate_product_data(invalid_data)
        
        assert "product_id" in str(exc_info.value)

class TestNewsAnalysisIntegration:
    """Тесты интеграции с NewsAnalysisProduct"""
    
    def test_news_analysis_loads_from_yaml(self):
        """Тест что NewsAnalysisProduct корректно загружает данные из YAML"""
        from src.backend.services.llm_service import LLMService
        from src.backend.services.products.news_analysis import NewsAnalysisProduct
        
        # Создаем mock LLM service
        class MockLLMService:
            def generate_text(self, prompt):
                return "Тестовый анализ"
        
        llm_service = MockLLMService()
        product = NewsAnalysisProduct(llm_service)
        
        # Проверяем что данные загрузились из файла
        assert product.product_id == "news_analysis"
        assert product.name == "Мониторинг и анализ новостей"
        
        # Проверяем что методы возвращают данные из YAML
        product_info = product.get_product_info()
        assert "key_benefits" in product_info
        assert len(product_info["key_benefits"]) > 0
        
        seo_keywords = product.get_seo_keywords()
        assert len(seo_keywords) > 0
        
        demo_content = product.get_demo_content()
        assert "demo_queries" in demo_content
