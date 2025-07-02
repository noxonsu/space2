#!/usr/bin/env python3
"""
Массовый генератор SEO-страниц
Позволяет создавать множество SEO-страниц из списка ключевых слов
"""

import argparse
import os
import sys
import json
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Загрузка переменных окружения
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from src.backend.services.content_generation_service import ContentGenerationService
from src.backend.services.llm_service import LLMService
from src.backend.cli.generate_seo_page import slugify

class BulkSeoGenerator:
    def __init__(self):
        self.llm_service = LLMService(
            deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        self.content_generator = ContentGenerationService(self.llm_service)
        
        # Базовые пути
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
        self.seo_pages_base_dir = os.path.join(self.project_root, 'content', 'seo_pages')
        
    def load_keywords_from_file(self, file_path: str) -> List[str]:
        """Загружает ключевые слова из файла (по одному на строку)"""
        keywords = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    keyword = line.strip()
                    if keyword and not keyword.startswith('#'):  # Игнорируем комментарии
                        keywords.append(keyword)
            print(f"Загружено {len(keywords)} ключевых слов из файла: {file_path}")
            return keywords
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден: {file_path}")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            return []
    
    def generate_semantic_cluster(self, main_keyword: str, cluster_size: int = 5) -> List[str]:
        """Генерирует семантический кластер на основе главного ключевого слова"""
        prompt = f"""
        Создай семантический кластер из {cluster_size} ключевых слов для B2B-услуг, связанных с темой "{main_keyword}".
        
        Ключевые слова должны быть:
        1. Коммерчески ориентированными (услуги, консультации, анализ)
        2. Подходящими для B2B-сегмента
        3. Различными по интенту (информационные, коммерческие, навигационные)
        4. Реалистичными для продвижения
        
        Верни только список ключевых слов, по одному на строку, без нумерации.
        """
        
        try:
            response = self.llm_service.generate_text(prompt)
            keywords = [k.strip() for k in response.split('\n') if k.strip()]
            return keywords[:cluster_size]  # Ограничиваем размер кластера
        except Exception as e:
            print(f"Ошибка при генерации семантического кластера для '{main_keyword}': {e}")
            return []
    
    def generate_pages_batch(self, keywords: List[str], delay: float = 2.0, skip_existing: bool = True) -> Dict[str, Any]:
        """Генерирует SEO-страницы пачкой с задержкой между запросами"""
        results = {
            'success': [],
            'failed': [],
            'skipped': [],
            'total': len(keywords)
        }
        
        print(f"Начинаем генерацию {len(keywords)} SEO-страниц...")
        print(f"Задержка между запросами: {delay}с")
        print(f"Пропускать существующие: {skip_existing}")
        print("-" * 50)
        
        for i, keyword in enumerate(keywords, 1):
            slug = slugify(keyword)
            seo_page_dir = os.path.join(self.seo_pages_base_dir, slug)
            
            print(f"[{i}/{len(keywords)}] Обрабатываем: '{keyword}' -> '{slug}'")
            
            # Проверяем существование
            if skip_existing and os.path.exists(seo_page_dir):
                print(f"  ⏭️  Пропускаем - страница уже существует")
                results['skipped'].append({'keyword': keyword, 'slug': slug})
                continue
            
            try:
                # Создаем директорию
                if not os.path.exists(seo_page_dir):
                    os.makedirs(seo_page_dir)
                
                # Генерируем контент
                self.content_generator.generate_all_for_keyword(keyword, slug, seo_page_dir)
                
                print(f"  ✅ Успешно создана страница: /{slug}")
                results['success'].append({'keyword': keyword, 'slug': slug})
                
            except Exception as e:
                print(f"  ❌ Ошибка при создании страницы: {e}")
                results['failed'].append({'keyword': keyword, 'slug': slug, 'error': str(e)})
            
            # Задержка между запросами (чтобы не перегружать API)
            if i < len(keywords):  # Не делаем задержку после последнего элемента
                time.sleep(delay)
        
        return results
    
    def save_generation_report(self, results: Dict[str, Any], output_file: str = None):
        """Сохраняет отчет о генерации в JSON-файл"""
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.project_root, f'seo_generation_report_{timestamp}.json')
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Отчет сохранен: {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении отчета: {e}")

def main():
    parser = argparse.ArgumentParser(description="Массовая генерация SEO-страниц")
    parser.add_argument("--keywords-file", help="Путь к файлу с ключевыми словами (по одному на строку)")
    parser.add_argument("--keywords", nargs='+', help="Список ключевых слов через пробел")
    parser.add_argument("--cluster", help="Генерировать семантический кластер на основе этого ключевого слова")
    parser.add_argument("--cluster-size", type=int, default=5, help="Размер семантического кластера (по умолчанию: 5)")
    parser.add_argument("--delay", type=float, default=2.0, help="Задержка между запросами в секундах (по умолчанию: 2.0)")
    parser.add_argument("--no-skip", action="store_true", help="Не пропускать существующие страницы")
    parser.add_argument("--report", help="Путь для сохранения отчета (по умолчанию: автоматический)")
    
    args = parser.parse_args()
    
    generator = BulkSeoGenerator()
    keywords = []
    
    # Определяем источник ключевых слов
    if args.keywords_file:
        keywords = generator.load_keywords_from_file(args.keywords_file)
    elif args.keywords:
        keywords = args.keywords
    elif args.cluster:
        print(f"Генерируем семантический кластер для: '{args.cluster}'")
        keywords = generator.generate_semantic_cluster(args.cluster, args.cluster_size)
        print(f"Сгенерированные ключевые слова: {keywords}")
    else:
        print("Ошибка: Необходимо указать источник ключевых слов")
        print("Используйте --keywords-file, --keywords или --cluster")
        sys.exit(1)
    
    if not keywords:
        print("Ошибка: Не найдено ключевых слов для обработки")
        sys.exit(1)
    
    # Генерируем страницы
    results = generator.generate_pages_batch(
        keywords=keywords,
        delay=args.delay,
        skip_existing=not args.no_skip
    )
    
    # Выводим итоговый отчет
    print("\n" + "="*50)
    print("ИТОГОВЫЙ ОТЧЕТ")
    print("="*50)
    print(f"Всего обработано: {results['total']}")
    print(f"Успешно создано: {len(results['success'])}")
    print(f"Пропущено: {len(results['skipped'])}")
    print(f"Ошибки: {len(results['failed'])}")
    
    if results['failed']:
        print("\nОшибки:")
        for failed in results['failed']:
            print(f"  - {failed['keyword']}: {failed['error']}")
    
    # Сохраняем отчет
    generator.save_generation_report(results, args.report)
    
    print(f"\nГенерация завершена!")

if __name__ == "__main__":
    main()
