"""
Сервис для генерации llms.txt файла согласно спецификации llmstxt.org
"""

from typing import Dict, List, Any
from .product_data_loader import ProductDataLoader
import os


class LlmsTxtService:
    """Сервис для генерации llms.txt файла"""
    
    def __init__(self, base_url: str = "https://hababru.com"):
        self.base_url = base_url.rstrip('/')
        self.product_loader = ProductDataLoader()
    
    def generate_llms_txt(self) -> str:
        """Генерирует содержимое llms.txt файла"""
        
        # Основная информация
        content = []
        content.append("# HababRu - B2B Платформа для Кастомных Решений")
        content.append("")
        content.append("> B2B-сервис, специализирующийся на разработке кастомных решений для бизнеса с демонстрационными AI-сервисами для анализа документов, мониторинга новостей и других отраслевых задач.")
        content.append("")
        
        # Детальная информация
        content.append("Платформа построена на принципе **SEO-first подхода**, где каждый демонстрационный сервис окружен семантическим ядром целевых страниц для привлечения органического трафика и демонстрации экспертности.")
        content.append("")
        content.append("**Ключевые направления:**")
        content.append("- Анализ юридических документов с AI-анализом")
        content.append("- Мониторинг отраслевых новостей и упоминаний")
        content.append("- Кастомные B2B-решения под конкретные задачи клиентов")
        content.append("")
        content.append("**Технологический стек:** Python (Flask), Vanilla JavaScript, универсальный LLM-коннектор (DeepSeek/OpenAI), автоматическая генерация SEO-контента.")
        content.append("")
        
        # Документация
        content.append("## Документация")
        content.append("")
        content.append("- [Архитектура проекта](https://github.com/noxonsu/hababru/blob/main/README.md): Детальное описание модульной архитектуры платформы")
        content.append("- [API документация](https://github.com/noxonsu/hababru/blob/main/docs/api.md): Описание REST API для интеграции с продуктами")
        content.append("- [Инструкция по развертыванию](https://github.com/noxonsu/hababru/blob/main/docs/deployment.md): Руководство по настройке и запуску в production")
        content.append("")
        
        # Продукты
        content.append("## Продукты")
        content.append("")
        
        # Загружаем доступные продукты
        available_products = self.product_loader.get_available_products()
        for product_id in available_products:
            try:
                product_data = self.product_loader.load_product_data(product_id)
                product_name = product_data.get("name", product_id)
                product_description = product_data.get("description", "")
                
                # Создаем ссылку на демо-страницу продукта
                demo_url = f"{self.base_url}/{product_id}" # Удален /demo/
                content.append(f"- [{product_name}]({demo_url}): {product_description}")
                
            except Exception as e:
                # Если не удалось загрузить данные продукта, пропускаем
                continue
        
        content.append("")
        
        # SEO страницы
        content.append("## SEO Страницы")
        content.append("")
        
        # Динамически получаем SEO страницы из конфигурации продуктов
        seo_pages = self._get_seo_pages_from_products()
        for page in seo_pages:
            page_url = f"{self.base_url}/{page['path']}"
            content.append(f"- [{page['title']}]({page_url}): {page['description']}")
        
        content.append("")
        
        # Примеры и демо
        content.append("## Примеры")
        content.append("")
        
        # Динамически получаем примеры из конфигурации продуктов
        demo_examples = self._get_demo_examples_from_products()
        for example in demo_examples:
            example_url = f"{self.base_url}/{example['path']}"
            content.append(f"- [{example['title']}]({example_url}): {example['description']}")
        
        content.append("")
        
        # Опциональная секция с техническими деталями
        content.append("## Optional")
        content.append("")
        content.append("- [Конфигурация продуктов]({}/content/products/): YAML-файлы с данными о продуктах и их параметрах".format(self.base_url))
        content.append("- [Промпты для LLM]({}/content/seo_prompts/): Шаблоны промптов для генерации SEO-контента".format(self.base_url))
        content.append("- [Кэш анализов]({}/data/cache/): Структура кэширования результатов LLM-анализа".format(self.base_url))
        content.append("- [Статические ресурсы]({}/public/): CSS, JavaScript и другие статические файлы".format(self.base_url))
        
        return "\n".join(content)
    
    def get_product_sections(self) -> Dict[str, List[Dict[str, str]]]:
        """Возвращает структурированную информацию о продуктах для llms.txt"""
        sections = {}
        
        available_products = self.product_loader.get_available_products()
        for product_id in available_products:
            try:
                product_data = self.product_loader.load_product_data(product_id)
                
                sections[product_id] = {
                    "name": product_data.get("name", product_id),
                    "description": product_data.get("description", ""),
                    "demo_url": f"{self.base_url}/{product_id}", # Удален /demo/
                    "seo_keywords": product_data.get("seo", {}).get("keywords", [])[:5]  # Первые 5 ключевых слов
                }
            except Exception:
                continue
        
        return sections
    
    def validate_llms_txt_format(self, content: str) -> bool:
        """Проверяет соответствие содержимого спецификации llms.txt"""
        lines = content.split('\n')
        
        # Проверяем что файл начинается с H1
        if not lines[0].startswith('# '):
            return False
        
        # Проверяем наличие blockquote с описанием
        blockquote_found = False
        for line in lines[:10]:  # Ищем в первых 10 строках
            if line.startswith('> '):
                blockquote_found = True
                break
        
        if not blockquote_found:
            return False
        
        # Проверяем наличие хотя бы одной секции H2
        h2_found = False
        for line in lines:
            if line.startswith('## '):
                h2_found = True
                break
        
        return h2_found
    
    def _get_seo_pages_from_products(self) -> list:
        """Получает список SEO страниц из конфигурации всех продуктов"""
        seo_pages = []
        
        available_products = self.product_loader.get_available_products()
        for product_id in available_products:
            try:
                product_data = self.product_loader.load_product_data(product_id)
                
                # Проверяем что продукт активен
                if product_data.get("status") != "active":
                    continue
                
                # Получаем SEO страницы из конфигурации продукта
                product_seo_pages = product_data.get("seo_pages", [])
                seo_pages.extend(product_seo_pages)
                
            except Exception:
                continue
        
        return seo_pages
    
    def _get_demo_examples_from_products(self) -> list:
        """Получает список демо примеров из конфигурации всех продуктов"""
        demo_examples = []
        
        available_products = self.product_loader.get_available_products()
        for product_id in available_products:
            try:
                product_data = self.product_loader.load_product_data(product_id)
                
                # Проверяем что продукт активен
                if product_data.get("status") != "active":
                    continue
                
                # Получаем демо примеры из конфигурации продукта
                product_demo_examples = product_data.get("demo_examples", [])
                
                # Обрабатываем разные форматы demo_examples
                if isinstance(product_demo_examples, list):
                    # Фильтруем только словари (игнорируем строки типа "sample_data")
                    for example in product_demo_examples:
                        if isinstance(example, dict) and "path" in example:
                            demo_examples.append(example)
                elif isinstance(product_demo_examples, dict):
                    # Старый формат с sample_data - игнорируем
                    continue
                
            except Exception:
                continue
        
        return demo_examples
