"""
Базовая структура для продуктов/сервисов платформы
Каждый продукт имеет свой функционал, описание, скриншоты и SEO-страницы
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import os
import json

class BaseProduct(ABC):
    """Базовый класс для всех продуктов платформы"""
    
    def __init__(self, product_id: str, name: str, description: str):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.screenshots = []
        self.demo_data = {}
        
    @abstractmethod
    def get_product_info(self) -> Dict[str, Any]:
        """Возвращает информацию о продукте для SEO-страниц"""
        pass
    
    @abstractmethod
    def execute_demo(self, input_data: Any) -> Dict[str, Any]:
        """Выполняет демо-функционал продукта"""
        pass
    
    @abstractmethod
    def get_seo_keywords(self) -> List[str]:
        """Возвращает список ключевых слов для SEO"""
        pass
    
    @abstractmethod
    def get_demo_content(self) -> Dict[str, Any]:
        """Возвращает демо-контент для показа на SEO-странице"""
        pass
    
    def add_screenshot(self, screenshot_path: str, description: str = ""):
        """Добавляет скриншот продукта"""
        self.screenshots.append({
            "path": screenshot_path,
            "description": description
        })
    
    def get_screenshots(self) -> List[Dict[str, str]]:
        """Возвращает список скриншотов"""
        return self.screenshots
    
    def set_demo_data(self, demo_data: Dict[str, Any]):
        """Устанавливает демо-данные"""
        self.demo_data = demo_data

class ProductRegistry:
    """Реестр всех продуктов платформы"""
    
    def __init__(self):
        self._products = {}
        self._product_seo_mapping = {}  # slug -> product_id
    
    def register_product(self, product: BaseProduct):
        """Регистрирует продукт в системе"""
        self._products[product.product_id] = product
    
    def get_product(self, product_id: str) -> Optional[BaseProduct]:
        """Получает продукт по ID"""
        return self._products.get(product_id)
    
    def get_all_products(self) -> Dict[str, BaseProduct]:
        """Возвращает все зарегистрированные продукты"""
        return self._products.copy()
    
    def map_seo_page_to_product(self, seo_slug: str, product_id: str):
        """Привязывает SEO-страницу к продукту"""
        if product_id not in self._products:
            raise ValueError(f"Продукт {product_id} не зарегистрирован")
        self._product_seo_mapping[seo_slug] = product_id
    
    def get_product_for_seo_page(self, seo_slug: str) -> Optional[BaseProduct]:
        """Получает продукт для SEO-страницы"""
        product_id = self._product_seo_mapping.get(seo_slug)
        if product_id:
            return self._products.get(product_id)
        return None
    
    def get_seo_pages_for_product(self, product_id: str) -> List[str]:
        """Получает список SEO-страниц для продукта"""
        return [slug for slug, pid in self._product_seo_mapping.items() if pid == product_id]

# Глобальный реестр продуктов
product_registry = ProductRegistry()
