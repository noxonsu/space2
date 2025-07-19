#!/usr/bin/env python3
"""
Скрипт для полного анализа доступной информации о продукте анализа новостей
"""

import sys
import os
import pprint

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hababru'))

from hababru.src.backend.services.products.news_analysis import NewsAnalysisProduct
from hababru.src.backend.services.llm_service import LLMService


def main():
    print("=== АНАЛИЗ ДОСТУПНОЙ ИНФОРМАЦИИ О ПРОДУКТЕ 'АНАЛИЗ НОВОСТЕЙ' ===\n")
    
    # Создаем мок LLM сервис
    mock_llm_service = type('MockLLMService', (), {
        'generate_text': lambda self, prompt: 'Мок ответ от LLM'
    })()
    
    # Создаем продукт
    try:
        news_product = NewsAnalysisProduct(mock_llm_service)
        print("✅ Продукт успешно инициализирован\n")
    except Exception as e:
        print(f"❌ Ошибка инициализации продукта: {e}")
        return
    
    # 1. Базовая информация о продукте
    print("1. БАЗОВАЯ ИНФОРМАЦИЯ:")
    print(f"   - Product ID: {news_product.product_id}")
    print(f"   - Название: {news_product.name}")
    print(f"   - Описание: {news_product.description}")
    print()
    
    # 2. Подробная информация о продукте
    print("2. ПОДРОБНАЯ ИНФОРМАЦИЯ О ПРОДУКТЕ:")
    product_info = news_product.get_product_info()
    for key, value in product_info.items():
        if isinstance(value, list):
            print(f"   - {key}:")
            for item in value:
                print(f"     • {item}")
        else:
            print(f"   - {key}: {value}")
    print()
    
    # 3. SEO ключевые слова
    print("3. SEO КЛЮЧЕВЫЕ СЛОВА:")
    keywords = news_product.get_seo_keywords()
    print(f"   Всего: {len(keywords)} ключевых слов")
    for i, keyword in enumerate(keywords, 1):
        print(f"   {i:2d}. {keyword}")
    print()
    
    # 4. Демо-контент
    print("4. ДЕМО-КОНТЕНТ:")
    demo_content = news_product.get_demo_content()
    for key, value in demo_content.items():
        if isinstance(value, dict):
            print(f"   - {key}:")
            for subkey, subvalue in value.items():
                if isinstance(subvalue, list):
                    print(f"     • {subkey}:")
                    for item in subvalue:
                        print(f"       - {item}")
                else:
                    print(f"     • {subkey}: {subvalue}")
        elif isinstance(value, list):
            print(f"   - {key}:")
            for item in value:
                print(f"     • {item}")
        else:
            print(f"   - {key}: {value}")
    print()
    
    # 5. Интерфейсы ввода/вывода
    print("5. ИНТЕРФЕЙСЫ ВВОДА/ВЫВОДА:")
    
    print("   ВХОДНЫЕ ДАННЫЕ:")
    input_interface = news_product.get_input_interface_description()
    pprint.pprint(input_interface, width=80, indent=6)
    print()
    
    print("   ВЫХОДНЫЕ ДАННЫЕ:")
    output_interface = news_product.get_output_interface_description()
    pprint.pprint(output_interface, width=80, indent=6)
    print()
    
    # 6. Доступ к внутренним данным продукта
    print("6. ВНУТРЕННИЕ ДАННЫЕ КОНФИГУРАЦИИ:")
    print(f"   - Количество отслеживаемых секторов: {len(news_product.product_data.get('demo_data', {}).get('monitored_sectors', []))}")
    print(f"   - Источники новостей: {len(news_product.product_data.get('demo_data', {}).get('news_sources', []))}")
    print(f"   - Функции анализа: {len(news_product.product_data.get('demo_data', {}).get('analysis_features', []))}")
    print()
    
    # 7. Связанные SEO страницы
    print("7. СВЯЗАННЫЕ SEO СТРАНИЦЫ:")
    seo_pages = news_product.product_data.get('seo_pages', [])
    for page in seo_pages:
        print(f"   - {page.get('path', '')}: {page.get('title', '')} ({page.get('category', '')})")
    print()
    
    # 8. Пример выполнения демо
    print("8. ПРИМЕР ВЫПОЛНЕНИЯ ДЕМО:")
    try:
        demo_result = news_product.execute_demo({'query': 'внешнеэкономическая деятельность'})
        if 'error' in demo_result:
            print(f"   ❌ Ошибка выполнения: {demo_result['error']}")
        else:
            print(f"   ✅ Демо выполнено успешно:")
            print(f"   - Запрос: {demo_result.get('query', 'N/A')}")
            print(f"   - Найдено новостей: {demo_result.get('total_news', 0)}")
            print(f"   - Количество трендов: {len(demo_result.get('trends', []))}")
            if demo_result.get('news_items'):
                print(f"   - Первая новость: {demo_result['news_items'][0].get('title', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Ошибка выполнения демо: {e}")
    print()
    
    # 9. Статистика конфигурации
    print("9. СТАТИСТИКА КОНФИГУРАЦИИ:")
    config_stats = {
        'Всего ключей в конфигурации': len(news_product.product_data.keys()),
        'Количество SEO ключевых слов': len(news_product.get_seo_keywords()),
        'Количество целевых аудиторий': len(product_info.get('target_audience', [])),
        'Количество преимуществ': len(product_info.get('key_benefits', [])),
        'Количество случаев использования': len(product_info.get('use_cases', [])),
    }
    
    for key, value in config_stats.items():
        print(f"   - {key}: {value}")
    print()
    
    print("=== АНАЛИЗ ЗАВЕРШЕН ===")
    print(f"💡 Продукт имеет обширную конфигурацию с {sum(config_stats.values())} различными элементами данных")


if __name__ == "__main__":
    main()
