"""
Фабрика для динамического создания экземпляров продуктов на основе YAML конфигурации
"""

import importlib
from typing import Dict, Any, Optional
from .product_data_loader import ProductDataLoader


class ProductFactory:
    """Фабрика для создания экземпляров продуктов"""
    
    def __init__(self):
        self.data_loader = ProductDataLoader()
        self._dependency_map = {}
    
    def register_dependency(self, name: str, instance: Any) -> None:
        """Регистрирует зависимость, которая может быть внедрена в продукты"""
        self._dependency_map[name] = instance
    
    def create_product(self, product_id: str) -> Optional[Any]:
        """Создает экземпляр продукта на основе его конфигурации в YAML"""
        try:
            # Загружаем данные продукта
            product_data = self.data_loader.load_product_data(product_id)
            
            # Проверяем статус продукта
            if product_data.get("status") != "active":
                return None
            
            # Получаем конфигурацию класса
            product_class_config = product_data.get("product_class", {})
            
            if not product_class_config:
                raise ValueError(f"В продукте {product_id} отсутствует конфигурация product_class")
            
            # Импортируем модуль и класс
            module_name = product_class_config.get("module")
            class_name = product_class_config.get("class_name")
            
            if not module_name or not class_name:
                raise ValueError(f"В продукте {product_id} неполная конфигурация класса")
            
            # Динамически импортируем модуль
            module = importlib.import_module(module_name)
            product_class = getattr(module, class_name)
            
            # Подготавливаем зависимости
            dependencies = product_class_config.get("dependencies", [])
            dependency_instances = []
            
            for dep_name in dependencies:
                if dep_name not in self._dependency_map:
                    raise ValueError(f"Зависимость '{dep_name}' не зарегистрирована для продукта {product_id}")
                dependency_instances.append(self._dependency_map[dep_name])
            
            # Создаем экземпляр продукта
            if dependency_instances:
                product_instance = product_class(*dependency_instances)
            else:
                product_instance = product_class()
            
            return product_instance
            
        except Exception as e:
            raise RuntimeError(f"Ошибка создания продукта {product_id}: {e}")
    
    def create_all_active_products(self) -> Dict[str, Any]:
        """Создает экземпляры всех активных продуктов"""
        products = {}
        available_product_ids = self.data_loader.get_available_products()
        
        for product_id in available_product_ids:
            try:
                product_instance = self.create_product(product_id)
                if product_instance:
                    products[product_id] = product_instance
            except Exception as e:
                print(f"Ошибка создания продукта {product_id}: {e}")
        
        return products
