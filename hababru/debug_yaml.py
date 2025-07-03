#!/usr/bin/env python3

import yaml

yaml_text = '''---
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
'''

print("Testing YAML parsing...")
try:
    data = yaml.safe_load(yaml_text)
    print(f"SUCCESS: Loaded data keys: {list(data.keys())}")
    if 'product_info' in data:
        print(f"product_info keys: {list(data['product_info'].keys())}")
    else:
        print("No product_info found")
        
    print("Full parsed data:")
    print(data)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
