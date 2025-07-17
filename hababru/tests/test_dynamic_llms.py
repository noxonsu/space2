#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/space2/hababru')

from src.backend.services.telegram_product_generator import TelegramProductGenerator, TelegramMessage
from src.backend.services.llm_service import LLMService
from src.backend.services.llms_txt_service import LlmsTxtService

# Мок LLM сервиса для создания продукта
class MockLLMService:
    def generate_text(self, prompt):
        return """---
product_id: "crm_automation"
name: "CRM Автоматизация"
description: "Умный помощник для автоматизации CRM-процессов с ИИ"
version: "1.0"
category: "automation"
status: "active"

demo_data:
  key_features:
    - "Автоматическое заполнение карточек клиентов"
    - "Предиктивная аналитика продаж"
    - "Интеграция с мессенджерами"
  
  supported_formats:
    - "CSV"
    - "XLSX"
    - "API"
  
  processing_time: "мгновенно"
  accuracy: "95%"

product_info:
  key_benefits:
    - "Экономия времени до 80%"
    - "Повышение конверсии на 25%"
    - "Автоматизация рутинных задач"
  
  target_audience:
    - "Отделы продаж"
    - "Малый и средний бизнес"
    - "E-commerce компании"
  
  use_cases:
    - "Лидогенерация"
    - "Сегментация клиентов"
    - "Прогнозирование продаж"

seo:
  keywords:
    - "CRM автоматизация"
    - "автоматизация продаж"
    - "CRM с ИИ"
    - "управление клиентами"
    - "автоматизация бизнеса"
"""

# Создаем новый продукт
print("=== СОЗДАНИЕ НОВОГО ПРОДУКТА ===")
generator = TelegramProductGenerator(MockLLMService())

message = TelegramMessage(
    message_id=999,
    text="🚀 Новый CRM помощник с ИИ! Автоматизирует продажи, анализирует клиентов и прогнозирует сделки. Интеграция со всеми популярными системами.",
    date="2025-07-03T15:00:00Z",
    media_files=["crm_demo.png"]
)

result = generator.generate_product_from_message(message)
print("Результат создания:", result)

print("\n=== ПРОВЕРКА LLMS.TXT ПОСЛЕ ДОБАВЛЕНИЯ ===")
llms_service = LlmsTxtService('https://hababru.com')

print("Доступные продукты:")
products = llms_service.product_loader.get_available_products()
for product_id in products:
    try:
        data = llms_service.product_loader.load_product_data(product_id)
        print(f"- {product_id}: {data.get('name', 'No name')}")
    except Exception as e:
        print(f"- {product_id}: ERROR - {e}")

print("\n=== СЕКЦИЯ ПРОДУКТОВ ИЗ LLMS.TXT ===")
content = llms_service.generate_llms_txt()
lines = content.split('\n')

# Ищем секцию "Продукты"
in_products_section = False
for line in lines:
    if line.strip() == "## Продукты":
        in_products_section = True
        print(line)
        continue
    elif line.startswith("## ") and in_products_section:
        break
    elif in_products_section:
        print(line)
