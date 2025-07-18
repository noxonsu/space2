import os
import yaml
from flask import render_template
from .llm_service import LLMService # Изменено на LLMService
from .parsing_service import ParsingService # Для анализа на лету
# Импортируем новые функции кэширования для SEO
from .cache_service import CacheService
from .products import product_registry, BaseProduct
import markdown # Добавляем импорт markdown
import json

class SeoService:
    def __init__(self, llm_service: LLMService, parsing_service: ParsingService, content_base_path: str): # Изменено на llm_service
        self.llm_service = llm_service # Изменено на llm_service
        self.parsing_service = parsing_service
        self.content_base_path = content_base_path
        self.cache_service = CacheService()

    def _get_logger(self):
        from flask import current_app # Импортируем здесь, чтобы избежать циклических зависимостей на уровне модуля
        return current_app.logger if current_app else None

    def render_seo_page(self, slug: str) -> str:
        logger = self._get_logger()
        page_dir = os.path.join(self.content_base_path, slug)
        source_md_path = os.path.join(page_dir, 'source.md')

        if logger:
            logger.info(f"SeoService: Попытка загрузить source.md из: {source_md_path}")

        if not os.path.exists(source_md_path):
            if logger:
                logger.error(f"SeoService: Файл source.md не найден по пути: {source_md_path}")
            raise FileNotFoundError(f"SEO-страница не найдена для слага: {slug} (ожидался файл: {source_md_path})")

        # Чтение source.md
        with open(source_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Разделение YAML Front Matter и основного текста
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError("Некорректный формат source.md: отсутствует YAML Front Matter.")
        
        front_matter = yaml.safe_load(parts[1])
        page_text_content = parts[2].strip()

        # Получаем связанный продукт
        product = self.get_product_for_page(slug)
        product_info = product.get_product_info() if product else {}
        demo_content = product.get_demo_content() if product else {}

        # Подготавливаем данные для демо в зависимости от типа продукта
        demo_data = {}
        analysis_results = {"summary": "Нет данных для анализа", "paragraphs": []}
        
        if product and product.product_id == 'contract_analysis':
            # Для анализа договоров ищем сгенерированный договор
            contract_file_path = os.path.join(page_dir, 'generated_contract.txt')
            generated_contract_text = ""
            
            if os.path.exists(contract_file_path):
                with open(contract_file_path, 'r', encoding='utf-8') as f:
                    generated_contract_text = f.read()
            elif demo_content.get('demo_contract_text'):
                # Используем демо-текст из продукта
                generated_contract_text = demo_content['demo_contract_text']
            
            if generated_contract_text:
                if logger:
                    logger.info("SeoService: Выполняем анализ договора для SEO-страницы")
                analysis_results = self._perform_contract_analysis(generated_contract_text)
                demo_data = {
                    "contract_text": generated_contract_text,
                    "analysis_results": analysis_results
                }
        
        elif product and product.product_id == 'news_analysis':
            # Для анализа новостей используем демо-запросы
            if demo_content.get('demo_queries'):
                sample_query = demo_content['demo_queries'][0]
                
                # Используем кеш для результатов демо-анализа новостей
                cache_key = f"news_analysis_demo_{slug}"
                demo_results = self.cache_service.get_seo_cached_analysis(cache_key)
                
                if not demo_results:
                    if logger:
                        logger.info(f"SeoService: Демо-результаты для '{slug}' не найдены в кеше, выполняем запрос.")
                    demo_results = product.execute_demo({'query': sample_query})
                    # Кешируем результат на 1 час
                    self.cache_service.save_seo_analysis_to_cache(cache_key, demo_results) # timeout is not supported by save_seo_analysis_to_cache
                else:
                    if logger:
                        logger.info(f"SeoService: Демо-результаты для '{slug}' загружены из кеша.")

                demo_data = {
                    "sample_query": sample_query,
                    "demo_results": demo_results
                }

        # Подготовка данных для шаблона
        template_data = {
            "is_seo_page": True,
            "page_title": front_matter.get("title", slug),
            "page_h1": front_matter.get("title", slug),
            "meta_keywords": ", ".join(front_matter.get("meta_keywords", [])),
            "meta_description": front_matter.get("meta_description", ""),
            "related_keywords_meta": front_matter.get("related_keywords", []),
            "related_keywords_list": front_matter.get("related_keywords", []),
            "page_text_content": markdown.markdown(page_text_content),
            "main_keyword": front_matter.get("main_keyword", slug),
            "product_info": product_info,
            "demo_content": demo_content,
            "demo_data": demo_data,
            # Для обратной совместимости
            "contract_text_raw": demo_data.get("contract_text", ""),
            "analysis_results_raw": demo_data.get("analysis_results", analysis_results)
        }
        
        # Convert relevant data to JSON strings here
        template_data_json = {
            "isSeoPage": template_data["is_seo_page"],
            "mainKeyword": template_data["main_keyword"],
            "seoPageContractTextRaw": template_data["contract_text_raw"],
            "analysis_results_raw": template_data["analysis_results_raw"],
            "productInfo": template_data["product_info"],
            "demoContent": template_data["demo_content"],
            "demoData": template_data["demo_data"]
        }

        if logger:
            logger.info(f"SeoService: Данные, передаваемые в шаблон 'index_template.html' для '{slug}':")
            logger.info(f"  is_seo_page: {template_data['is_seo_page']}")
            logger.info(f"  page_title: {template_data['page_title']}")
            logger.info(f"  product_info: {product_info.get('name', 'Не указан') if product_info else 'Нет продукта'}")
            logger.info(f"  template_data_json (dumped, length {len(json.dumps(template_data_json))}): {json.dumps(template_data_json)[:100]}...")

        import html # Import html module for escaping

        # Escape the JSON string for embedding within a JavaScript string literal
        app_config_json_escaped = html.escape(json.dumps(template_data_json))

        # Выбираем шаблон в зависимости от продукта
        template_name = 'index_template.html'  # По умолчанию
        
        if product and product.product_id == 'news_analysis':
            template_name = 'news_analysis_template.html'
        elif product and product.product_id == 'contract_analysis':
            template_name = 'contract_analysis_template.html'
        # Для новых продуктов можно добавить другие шаблоны
        
        if logger:
            logger.info(f"SeoService: Используем шаблон '{template_name}' для продукта '{product.product_id if product else 'default'}'")

        return render_template(template_name, **template_data, app_config_json=app_config_json_escaped)

    def _perform_contract_analysis(self, contract_text: str):
        """Выполняет анализ договора (рефакторинг старого метода)"""
        logger = self._get_logger()
        if not contract_text:
            return {"summary": "Договор пуст, анализ невозможен.", "paragraphs": []}

        # Используем llm_service для сегментации, чтобы она кэшировалась
        paragraphs = self.llm_service.segment_text_into_paragraphs(contract_text)
        
        # Анализ каждого абзаца с LLM, используя analyze_paragraph_in_context
        analyzed_paragraphs = []
        file_hash = self.cache_service._generate_hash(contract_text)

        for i, paragraph in enumerate(paragraphs):
            if logger:
                logger.info(f"SeoService: Подготовка к анализу пункта {i+1}/{len(paragraphs)} для file_hash: {file_hash}")

            analysis_html = self.cache_service.get_cached_paragraph_analysis(file_hash, paragraph)

            if analysis_html:
                if logger:
                    logger.info(f"SeoService: Анализ пункта {i+1} найден в кэше (HTML).")
            else:
                if logger:
                    logger.info(f"SeoService: Анализ пункта {i+1} не найден в кэше, выполняем через LLM.")
                try:
                    # Получаем анализ в Markdown от LLM
                    analysis_markdown = self.llm_service.analyze_paragraph_in_context(paragraph, contract_text)
                    if analysis_markdown:
                        # Конвертируем в HTML
                        analysis_html = markdown.markdown(analysis_markdown)
                        # Сохраняем HTML в кэш абзацев
                        self.cache_service.save_paragraph_analysis_to_cache(file_hash, paragraph, analysis_html)
                        if logger:
                            logger.info(f"SeoService: Анализ пункта {i+1} выполнен и сохранен в кэш.")
                    else:
                        analysis_html = "Не удалось получить анализ для этого пункта."
                        if logger:
                            logger.warning(f"SeoService: Не удалось получить анализ для пункта {i+1}.")
                except Exception as e:
                    if logger:
                        logger.error(f"SeoService: Ошибка при анализе абзаца {i+1}: {e}", exc_info=True)
                    analysis_html = f"Ошибка анализа пункта: {e}"
            
            analyzed_paragraphs.append({
                "original_paragraph": paragraph,
                "analysis": analysis_html
            })
        
        return {
            "summary": "Анализ договора завершен успешно.",
            "paragraphs": analyzed_paragraphs
        }

    def _perform_on_the_fly_analysis(self, contract_text: str):
        logger = self._get_logger()
        if not contract_text:
            return {"summary": "Договор пуст, анализ невозможен.", "paragraphs": []}

        # Используем llm_service для сегментации, чтобы она кэшировалась
        paragraphs = self.llm_service.segment_text_into_paragraphs(contract_text)
        
        # Анализ каждого абзаца с LLM, используя analyze_paragraph_in_context
        analyzed_paragraphs = []
        file_hash = self.cache_service._generate_hash(contract_text)

        for i, paragraph in enumerate(paragraphs):
            if logger:
                logger.info(f"SeoService: Подготовка к анализу пункта {i+1}/{len(paragraphs)} для file_hash: {file_hash}, paragraph_hash: {self.cache_service._generate_hash(paragraph)}")

            analysis_html = self.cache_service.get_cached_paragraph_analysis(file_hash, paragraph)

            if analysis_html:
                if logger:
                    logger.info(f"SeoService: Анализ пункта {i+1} найден в индивидуальном кэше (HTML).")
            else:
                if logger:
                    logger.info(f"SeoService: Анализ пункта {i+1} не найден в кэше, выполняем через LLM.")
                try:
                    # Получаем анализ в Markdown от LLM
                    analysis_markdown = self.llm_service.analyze_paragraph_in_context(paragraph, contract_text)
                    if analysis_markdown:
                        # Конвертируем в HTML
                        analysis_html = markdown.markdown(analysis_markdown)
                        # Сохраняем HTML в индивидуальный кэш абзацев
                        self.cache_service.save_paragraph_analysis_to_cache(file_hash, paragraph, analysis_html)
                        if logger:
                            logger.info(f"SeoService: Анализ пункта {i+1} выполнен, сконвертирован в HTML и сохранен в индивидуальный кэш.")
                    else:
                        analysis_html = "Не удалось получить анализ для этого пункта."
                        if logger:
                            logger.warning(f"SeoService: Не удалось получить анализ (Markdown) для пункта {i+1}. LLM вернул пустой ответ.")
                except Exception as e:
                    if logger:
                        logger.error(f"SeoService: Ошибка при анализе абзаца {i+1} с LLM: {e}", exc_info=True)
                    analysis_html = f"Ошибка анализа пункта: {e}"
            
            analyzed_paragraphs.append({
                "original_paragraph": paragraph,
                "analysis": analysis_html
            })
        
        return {
            "summary": "Это анализ договора, выполненный 'на лету'.",
            "paragraphs": analyzed_paragraphs
        }

    def get_product_for_page(self, slug: str) -> BaseProduct:
        """Получает продукт, связанный с SEO-страницей"""
        # Сначала пытаемся найти в реестре продуктов
        product = product_registry.get_product_for_seo_page(slug)
        
        if product:
            return product
            
        # Если не найден, пытаемся определить по метаданным source.md
        page_dir = os.path.join(self.content_base_path, slug)
        source_md_path = os.path.join(page_dir, 'source.md')
        
        if os.path.exists(source_md_path):
            with open(source_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = yaml.safe_load(parts[1])
                product_id = front_matter.get('product_id')
                
                if product_id:
                    product = product_registry.get_product(product_id)
                    if product:
                        # Регистрируем связь в реестре для следующих запросов
                        product_registry.map_seo_page_to_product(slug, product_id)
                        return product
        
        # По умолчанию возвращаем продукт анализа договоров
        return product_registry.get_product('contract_analysis')

    def get_page_data(self, slug: str) -> dict:
        """Получает полные данные SEO-страницы включая информацию о продукте"""
        page_dir = os.path.join(self.content_base_path, slug)
        source_md_path = os.path.join(page_dir, 'source.md')
        
        if not os.path.exists(source_md_path):
            raise FileNotFoundError(f"SEO-страница не найдена: {slug}")
        
        # Чтение метаданных страницы
        with open(source_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError("Некорректный формат source.md")
        
        front_matter = yaml.safe_load(parts[1])
        page_text_content = parts[2].strip()
        
        # Получаем связанный продукт
        product = self.get_product_for_page(slug)
        product_info = product.get_product_info() if product else {}
        
        # Проверяем наличие демо-данных для продукта
        demo_available = False
        demo_content = {}
        if product:
            demo_content = product.get_demo_content()
            demo_available = bool(demo_content)
        
        return {
            'slug': slug,
            'title': front_matter.get('title', slug),
            'meta_description': front_matter.get('meta_description', ''),
            'meta_keywords': front_matter.get('meta_keywords', []),
            'main_keyword': front_matter.get('main_keyword', slug),
            'related_keywords': front_matter.get('related_keywords', []),
            'content': page_text_content,
            'product_id': front_matter.get('product_id'),
            'product_info': product_info,
            'demo_available': demo_available,
            'demo_content': demo_content,
            'created_at': front_matter.get('created_at'),
            'updated_at': front_matter.get('updated_at')
        }

    def create_seo_page_with_product(self, slug: str, title: str, keywords: list, 
                                   product_id: str, meta_description: str = "") -> bool:
        """Создает новую SEO-страницу, связанную с продуктом"""
        
        # Проверяем, что продукт существует
        product = product_registry.get_product(product_id)
        if not product:
            raise ValueError(f"Продукт {product_id} не найден в реестре")
        
        page_dir = os.path.join(self.content_base_path, slug)
        os.makedirs(page_dir, exist_ok=True)
        
        # Получаем информацию о продукте для генерации контента
        product_info = product.get_product_info()
        demo_content = product.get_demo_content()
        
        # Создаем front matter
        front_matter = {
            'title': title,
            'meta_description': meta_description or f"{title} - {product_info.get('description', '')}",
            'meta_keywords': keywords,
            'main_keyword': keywords[0] if keywords else slug,
            'related_keywords': keywords[1:] if len(keywords) > 1 else [],
            'product_id': product_id,
            'created_at': yaml.safe_load(yaml.dump({'created_at': 'now()'}))['created_at']
        }
        
        # Генерируем контент страницы на основе продукта
        page_content = self._generate_product_page_content(product, title, keywords)
        
        # Создаем source.md
        source_content = f"---\n{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---\n\n{page_content}"
        
        source_md_path = os.path.join(page_dir, 'source.md')
        with open(source_md_path, 'w', encoding='utf-8') as f:
            f.write(source_content)
        
        # Регистрируем связь страницы с продуктом
        product_registry.map_seo_page_to_product(slug, product_id)
        
        # Генерируем демо-данные если это продукт анализа договоров
        if product_id == 'contract_analysis' and demo_content:
            self._generate_demo_contract_for_page(page_dir, demo_content)
        
        return True

    def _generate_product_page_content(self, product: BaseProduct, title: str, keywords: list) -> str:
        """Генерирует контент SEO-страницы на основе информации о продукте"""
        product_info = product.get_product_info()
        demo_content = product.get_demo_content()
        
        content_parts = [
            f"# {title}",
            "",
            f"**{product_info.get('description', '')}**",
            "",
            "## Ключевые преимущества",
            ""
        ]
        
        # Добавляем преимущества
        for benefit in product_info.get('key_benefits', []):
            content_parts.append(f"- {benefit}")
        
        content_parts.extend(["", "## Для кого подходит", ""])
        
        # Добавляем целевую аудиторию
        for audience in product_info.get('target_audience', []):
            content_parts.append(f"- {audience}")
        
        content_parts.extend(["", "## Сценарии использования", ""])
        
        # Добавляем кейсы использования
        for use_case in product_info.get('use_cases', []):
            content_parts.append(f"- {use_case}")
        
        # Добавляем демо-контент если доступен
        if demo_content and product.product_id == 'news_analysis':
            content_parts.extend([
                "", "## Примеры отслеживаемых тем", ""
            ])
            for query in demo_content.get('demo_queries', []):
                content_parts.append(f"- {query}")
        
        # Добавляем призыв к действию
        content_parts.extend([
            "", "## Попробуйте прямо сейчас", "",
            f"Загрузите документ и получите детальный анализ с помощью нашего {product_info.get('name', 'сервиса').lower()}.",
            "",
            "**Быстро • Точно • Конфиденциально**"
        ])
        
        return "\n".join(content_parts)

    def _generate_demo_contract_for_page(self, page_dir: str, demo_content: dict):
        """Генерирует демо-договор для SEO-страницы анализа договоров"""
        demo_text = demo_content.get('demo_contract_text', '')
        if demo_text:
            contract_file_path = os.path.join(page_dir, 'generated_contract.txt')
            with open(contract_file_path, 'w', encoding='utf-8') as f:
                f.write(demo_text)
