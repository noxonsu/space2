#!/usr/bin/env python3

import tempfile
import os
from unittest.mock import Mock
import sys
import os

# Добавляем путь к модулям проекта
sys.path.insert(0, '/workspaces/space2/hababru/src')

from backend.services.telegram_product_generator import TelegramProductGenerator, TelegramMessage

def test_debug():
    temp_dir = tempfile.mkdtemp()
    
    # Создаем mock LLM service
    mock_llm_service = Mock()
    
    # Генератор
    generator = TelegramProductGenerator(
        llm_service=mock_llm_service,
        products_dir=temp_dir
    )

    yaml_response = """---
product_id: "ai_assistant"
name: "AI Помощник для Бизнеса"
description: "Интеллектуальный помощник для автоматизации бизнес-процессов"
version: "1.0"
category: "ai"
status: "active"

demo_data:
  key_features:
    - "Обработка естественного языка"
    - "Автоматизация задач"
    - "Интеграция с CRM"

product_info:
  key_benefits:
    - "Экономия времени до 60%"
    - "Снижение ошибок"
    - "24/7 доступность"
  
  target_audience:
    - "Малый бизнес"
    - "IT компании"
    - "Консалтинг"

seo:
  keywords:
    - "AI помощник"
    - "автоматизация бизнеса"
    - "искусственный интеллект"
"""

    print("Testing YAML parsing from generator...")
    parsed_data = generator._parse_yaml_from_llm_response(yaml_response)
    
    if parsed_data:
        print(f"SUCCESS: Parsed data keys: {list(parsed_data.keys())}")
        print(f"Has product_info: {'product_info' in parsed_data}")
        if 'product_info' in parsed_data:
            print(f"product_info keys: {list(parsed_data['product_info'].keys())}")
    else:
        print("FAILED: Could not parse YAML")
    
    print("\nTesting validation...")
    if parsed_data:
        is_valid = generator._validate_product_data(parsed_data)
        print(f"Validation result: {is_valid}")

if __name__ == "__main__":
    test_debug()
