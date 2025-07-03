"""
Утилита для загрузки данных продуктов из YAML-файлов
"""

import os
import yaml
from typing import Dict, Any, List
from pathlib import Path

class ProductDataLoader:
    """Загрузчик данных продуктов из файлов"""
    
    def __init__(self, products_dir: str = None):
        if products_dir is None:
            # Определяем путь к директории content/products относительно этого файла
            current_dir = Path(__file__).parent
            self.products_dir = current_dir.parent.parent.parent / "content" / "products"
        else:
            self.products_dir = Path(products_dir)
    
    def load_product_data(self, product_id: str) -> Dict[str, Any]:
        """Загружает данные продукта из YAML-файла"""
        file_path = self.products_dir / f"{product_id}.yaml"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Файл данных продукта не найден: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                return data
        except yaml.YAMLError as e:
            raise ValueError(f"Ошибка парсинга YAML-файла {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки файла {file_path}: {e}")
    
    def get_available_products(self) -> List[str]:
        """Возвращает список доступных продуктов"""
        if not self.products_dir.exists():
            return []
        
        products = []
        for file_path in self.products_dir.glob("*.yaml"):
            product_id = file_path.stem
            products.append(product_id)
        
        return sorted(products)
    
    def load_all_products(self) -> Dict[str, Dict[str, Any]]:
        """Загружает данные всех доступных продуктов"""
        products = {}
        for product_id in self.get_available_products():
            try:
                products[product_id] = self.load_product_data(product_id)
            except Exception as e:
                print(f"Ошибка загрузки продукта {product_id}: {e}")
        
        return products
    
    def validate_product_data(self, data: Dict[str, Any]) -> bool:
        """Проверяет корректность структуры данных продукта"""
        required_fields = ['product_id', 'name', 'description']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Обязательное поле '{field}' отсутствует в данных продукта")
        
        return True
