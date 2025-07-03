#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

from src.backend.services.llms_txt_service import LlmsTxtService

def test_llms_txt():
    print("Создаем сервис LlmsTxtService...")
    service = LlmsTxtService('https://hababru.com')
    
    print("Генерируем контент llms.txt...")
    content = service.generate_llms_txt()
    
    print(f"Контент сгенерирован, длина: {len(content)} символов")
    print("=" * 60)
    print(content)
    print("=" * 60)
    
    print("\nПроверяем валидность формата...")
    is_valid = service.validate_llms_txt_format(content)
    print(f"Формат валиден: {is_valid}")
    
    print("\nТест завершен!")

if __name__ == "__main__":
    test_llms_txt()
