#!/usr/bin/env python3

import sys
import os
import tempfile
import yaml
sys.path.append('/workspaces/space2/hababru')

from src.backend.services.telegram_product_generator import TelegramProductGenerator, TelegramMessage
from unittest.mock import Mock

def test_semantic_debug():
    """Отладочный тест для семантической проверки"""
    
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    
    # Mock LLM service
    mock_llm_service = Mock()
    
    # Создаем генератор
    generator = TelegramProductGenerator(
        llm_service=mock_llm_service,
        products_dir=temp_dir
    )
    
    # Создаем YAML продукта contract_analysis
    real_contract_yaml = """---
product_id: "contract_analysis"
name: "Анализ договоров с ИИ"
description: "Автоматизированный анализ юридических договоров с выявлением рисков и рекомендациями"
version: "1.0"
category: "legal"
status: "active"

demo_data:
  key_features:
    - "Анализ рисков договора"
    - "Проверка соответствия законодательству"
    - "Рекомендации по улучшению"
  
  supported_formats:
    - "PDF"
    - "DOC"
    - "TXT"
  
  processing_time: "2-5 минут"
  accuracy: "95%"

product_info:
  key_benefits:
    - "Экономия времени юристов до 70%"
    - "Снижение правовых рисков"
    - "Автоматизация рутинных проверок"
  
  target_audience:
    - "Юридические фирмы"
    - "Корпоративные юристы"
    - "Малый и средний бизнес"

seo:
  keywords:
    - "анализ договора"
    - "проверка договора"
    - "экспертиза договора"
    - "анализ договора ИИ"
    - "проверка контракта"
    - "юридический анализ"
"""
    
    # Сохраняем файл
    existing_product_path = os.path.join(temp_dir, "contract_analysis.yaml")
    with open(existing_product_path, 'w', encoding='utf-8') as f:
        f.write(real_contract_yaml)
    
    # Telegram сообщение
    telegram_text = "🔍 Новый сервис для проверки договоров с помощью искусственного интеллекта! Анализируем юридические документы и находим риски."
    
    print("=== ОТЛАДКА СЕМАНТИЧЕСКОЙ ПРОВЕРКИ ===")
    print(f"Telegram текст: {telegram_text}")
    
    # Нормализуем текст сообщения
    message_normalized = generator._normalize_text(telegram_text)
    print(f"Нормализованный текст сообщения: {message_normalized}")
    
    # Получаем существующие продукты
    existing_products = generator._get_existing_products_with_data()
    print(f"Найдено продуктов: {list(existing_products.keys())}")
    
    if "contract_analysis" in existing_products:
        product_data = existing_products["contract_analysis"]
        
        # Извлекаем полный текст продукта
        product_full_text = generator._extract_all_text_from_product(product_data)
        print(f"Полный текст продукта: {product_full_text[:200]}...")
        
        # Нормализуем текст продукта
        product_normalized = generator._normalize_text(product_full_text)
        print(f"Нормализованный текст продукта: {product_normalized[:200]}...")
        
        # Рассчитываем сходство
        similarity = generator._calculate_text_similarity(message_normalized, product_normalized)
        print(f"Коэффициент сходства: {similarity:.3f}")
        
        # Показываем пересечение слов
        words1 = set(message_normalized.split())
        words2 = set(product_normalized.split())
        
        stop_words = {
            "и", "в", "на", "с", "для", "от", "по", "до", "из", "к", "о", "об", "при", "про", 
            "через", "над", "под", "между", "а", "но", "или", "что", "как", "это", "то", "если",
            "так", "уже", "еще", "очень", "где", "когда", "потом", "здесь", "там", "все", "весь"
        }
        
        words1_filtered = {word for word in words1 if len(word) > 2 and word not in stop_words}
        words2_filtered = {word for word in words2 if len(word) > 2 and word not in stop_words}
        
        intersection = words1_filtered.intersection(words2_filtered)
        
        print(f"Слова из сообщения: {words1_filtered}")
        print(f"Слова из продукта (первые 20): {list(words2_filtered)[:20]}")
        print(f"Общие слова: {intersection}")
        print(f"Количество общих слов: {len(intersection)}")
        print(f"Общее количество уникальных слов: {len(words1_filtered.union(words2_filtered))}")
    
    # Проверяем семантический дубль
    duplicate_id = generator._check_semantic_duplicate(TelegramMessage(
        message_id=999,
        text=telegram_text,
        date="2025-07-03T16:00:00Z"
    ))
    
    print(f"Результат проверки дубля: {duplicate_id}")
    
    # Очистка
    import shutil
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    test_semantic_debug()
