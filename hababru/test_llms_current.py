#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/space2/hababru')

from src.backend.services.llms_txt_service import LlmsTxtService

service = LlmsTxtService('https://hababru.com')
content = service.generate_llms_txt()
print("=== LLMS.TXT CONTENT ===")
print(content)
print("=== END CONTENT ===")

# Проверим список продуктов
print("\n=== AVAILABLE PRODUCTS ===")
products = service.product_loader.get_available_products()
print("Products found:", products)

for product_id in products:
    try:
        data = service.product_loader.load_product_data(product_id)
        print(f"- {product_id}: {data.get('name', 'No name')} - {data.get('description', 'No description')}")
    except Exception as e:
        print(f"- {product_id}: ERROR - {e}")
