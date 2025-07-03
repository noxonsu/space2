#!/usr/bin/env python3

from src.backend.services.telegram_product_generator import TelegramProductGenerator, TelegramMessage
from unittest.mock import Mock

def test_telegram_generator():
    # Создаем мок LLM сервиса
    mock_llm = Mock()
    mock_llm.generate_text.return_value = """---
product_id: "test_ai_tool"
name: "Тестовый AI Инструмент"
description: "Демонстрационный AI инструмент для автоматизации"
version: "1.0"
category: "ai"
status: "active"

demo_data:
  key_features:
    - "Обработка текста"
    - "Автоматизация процессов"
    - "Интеграция с API"

product_info:
  key_benefits:
    - "Экономия времени до 40%"
    - "Повышение точности"
    - "Масштабируемость"
  
  target_audience:
    - "IT компании"
    - "Стартапы"

seo:
  keywords:
    - "AI инструмент"
    - "автоматизация"
    - "машинное обучение"
"""

    # Создаем генератор
    generator = TelegramProductGenerator(mock_llm)
    
    # Тестовое сообщение
    message = TelegramMessage(
        message_id=999,
        text="Новый AI инструмент для автоматизации бизнес-процессов",
        date="2025-07-03T15:00:00Z"
    )
    
    # Генерируем продукт
    result = generator.generate_product_from_message(message)
    
    print("=== РЕЗУЛЬТАТ ГЕНЕРАЦИИ ===")
    print(f"Успех: {result['success']}")
    if result['success']:
        print(f"Product ID: {result['product_id']}")
        print(f"Название: {result['product_name']}")
        print(f"Файл: {result['file_path']}")
    else:
        print(f"Ошибка: {result['error']}")

if __name__ == "__main__":
    test_telegram_generator()
