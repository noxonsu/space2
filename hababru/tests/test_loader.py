#!/usr/bin/env python3

from src.backend.services.product_data_loader import ProductDataLoader

def test_loader():
    loader = ProductDataLoader()
    products = loader.get_available_products()
    print('Доступные продукты:', products)
    
    for product_id in products:
        try:
            data = loader.load_product_data(product_id)
            print(f'{product_id}: {data["name"]} - {data["description"]}')
        except Exception as e:
            print(f'Ошибка загрузки {product_id}: {e}')

if __name__ == "__main__":
    test_loader()
