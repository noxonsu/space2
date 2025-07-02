#!/usr/bin/env python3
"""
CLI для создания SEO-страниц с поддержкой продуктов
"""

import os
import sys
import argparse
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.backend.services.seo_service import SeoService
from src.backend.services.llm_service import LLMService
from src.backend.services.parsing_service import ParsingService
from src.backend.services.cache_service import CacheService
from src.backend.services.products import product_registry
from src.backend.services.products.contract_analysis import ContractAnalysisProduct
from src.backend.services.products.news_analysis import NewsAnalysisProduct

def initialize_services():
    """Инициализация всех сервисов"""
    # Инициализируем сервисы
    llm_service = LLMService(
        deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    parsing_service = ParsingService(llm_service=llm_service)
    cache_service = CacheService()
    
    # Регистрируем продукты
    contract_product = ContractAnalysisProduct(llm_service, parsing_service, cache_service)
    news_product = NewsAnalysisProduct(llm_service)
    
    product_registry.register_product(contract_product)
    product_registry.register_product(news_product)
    
    # Создаем SEO-сервис
    content_base_path = os.path.join(os.getcwd(), 'content', 'seo_pages')
    seo_service = SeoService(
        llm_service=llm_service,
        parsing_service=parsing_service,
        content_base_path=content_base_path
    )
    
    return seo_service

def create_page_with_product(seo_service, slug, title, keywords, product_id, meta_description=""):
    """Создает SEO-страницу для указанного продукта"""
    try:
        success = seo_service.create_seo_page_with_product(
            slug=slug,
            title=title,
            keywords=keywords,
            product_id=product_id,
            meta_description=meta_description
        )
        
        if success:
            print(f"✅ SEO-страница '{slug}' успешно создана для продукта '{product_id}'")
            print(f"   Заголовок: {title}")
            print(f"   Ключевые слова: {', '.join(keywords)}")
            print(f"   URL: /{slug}")
            return True
        else:
            print(f"❌ Не удалось создать SEO-страницу '{slug}'")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании страницы: {e}")
        return False

def list_products():
    """Выводит список доступных продуктов"""
    products = product_registry.get_all_products()
    
    print("📦 Доступные продукты:")
    print("-" * 50)
    
    for product_id, product in products.items():
        product_info = product.get_product_info()
        print(f"ID: {product_id}")
        print(f"Название: {product.name}")
        print(f"Описание: {product.description}")
        print(f"Демо доступно: {'Да' if product_info.get('demo_available') else 'Нет'}")
        print("-" * 50)

def generate_slug(title):
    """Генерирует slug из заголовка"""
    import re
    import unicodedata
    
    # Приводим к нижнему регистру
    slug = title.lower()
    
    # Убираем лишние символы, оставляем только буквы, цифры и пробелы
    slug = re.sub(r'[^\w\s-]', '', slug, flags=re.UNICODE)
    
    # Заменяем пробелы и множественные дефисы на одиночные дефисы
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Убираем дефисы в начале и конце
    slug = slug.strip('-')
    
    return slug

def main():
    parser = argparse.ArgumentParser(description="Создание SEO-страниц с поддержкой продуктов")
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда для создания страницы
    create_parser = subparsers.add_parser('create', help='Создать SEO-страницу')
    create_parser.add_argument('--title', required=True, help='Заголовок страницы')
    create_parser.add_argument('--keywords', required=True, help='Ключевые слова (через запятую)')
    create_parser.add_argument('--product', required=True, help='ID продукта')
    create_parser.add_argument('--slug', help='Slug страницы (генерируется автоматически, если не указан)')
    create_parser.add_argument('--description', help='Meta description')
    
    # Команда для вывода списка продуктов
    list_parser = subparsers.add_parser('products', help='Показать список продуктов')
    
    # Команда для массового создания
    bulk_parser = subparsers.add_parser('bulk', help='Массовое создание страниц')
    bulk_parser.add_argument('--file', required=True, help='Файл с данными для создания (CSV)')
    bulk_parser.add_argument('--product', required=True, help='ID продукта для всех страниц')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Инициализируем сервисы
    print("🔧 Инициализация сервисов...")
    seo_service = initialize_services()
    
    if args.command == 'products':
        list_products()
        
    elif args.command == 'create':
        # Проверяем, что продукт существует
        product = product_registry.get_product(args.product)
        if not product:
            print(f"❌ Продукт '{args.product}' не найден")
            print("Доступные продукты:")
            list_products()
            return
        
        # Генерируем slug если не указан
        slug = args.slug or generate_slug(args.title)
        
        # Парсим ключевые слова
        keywords = [kw.strip() for kw in args.keywords.split(',')]
        
        print(f"🚀 Создание SEO-страницы...")
        print(f"   Slug: {slug}")
        print(f"   Заголовок: {args.title}")
        print(f"   Продукт: {args.product}")
        print(f"   Ключевые слова: {', '.join(keywords)}")
        
        success = create_page_with_product(
            seo_service=seo_service,
            slug=slug,
            title=args.title,
            keywords=keywords,
            product_id=args.product,
            meta_description=args.description or ""
        )
        
        if success:
            print(f"\n🎉 Страница готова! Проверьте: http://localhost/{slug}")
        
    elif args.command == 'bulk':
        print(f"📄 Массовое создание из файла: {args.file}")
        
        # Проверяем, что продукт существует
        product = product_registry.get_product(args.product)
        if not product:
            print(f"❌ Продукт '{args.product}' не найден")
            return
        
        try:
            import csv
            with open(args.file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                created_count = 0
                failed_count = 0
                
                for row in reader:
                    title = row.get('title', '').strip()
                    keywords_str = row.get('keywords', '').strip()
                    slug = row.get('slug', '').strip() or generate_slug(title)
                    description = row.get('description', '').strip()
                    
                    if not title or not keywords_str:
                        print(f"⚠️  Пропускаем строку: отсутствует title или keywords")
                        failed_count += 1
                        continue
                    
                    keywords = [kw.strip() for kw in keywords_str.split(',')]
                    
                    success = create_page_with_product(
                        seo_service=seo_service,
                        slug=slug,
                        title=title,  
                        keywords=keywords,
                        product_id=args.product,
                        meta_description=description
                    )
                    
                    if success:
                        created_count += 1
                    else:
                        failed_count += 1
                
                print(f"\n📊 Результат:")
                print(f"   Создано: {created_count}")
                print(f"   Ошибок: {failed_count}")
                
        except FileNotFoundError:
            print(f"❌ Файл {args.file} не найден")
        except Exception as e:
            print(f"❌ Ошибка при обработке файла: {e}")

if __name__ == "__main__":
    main()
