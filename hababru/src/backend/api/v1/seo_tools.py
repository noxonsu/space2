from flask import Blueprint, jsonify, request, render_template
import os
import yaml
import markdown
from flask import current_app
import logging
from datetime import datetime # Добавляем импорт datetime
from ...services.llm_service import LLMService # Импортируем LLMService
from ...services.products import product_registry
from ...services.telegram_connector import TelegramConnector
from ...services.telegram_product_generator import TelegramProductGenerator, TelegramMessage

def create_seo_tools_blueprint(seo_service, seo_prompt_service) -> Blueprint:
    """Создает Blueprint для SEO и Telegram инструментов"""
    
    blueprint = Blueprint('seo_tools', __name__)
    
    # Инициализируем Telegram сервисы
    telegram_connector = None
    # product_generator теперь будет инициализироваться внутри функций,
    # чтобы иметь доступ к current_app.config.get('LLM_SERVICE')
    
    def get_llm_service_instance():
        """Вспомогательная функция для получения LLMService из current_app.config"""
        llm_service_instance = current_app.config.get('LLM_SERVICE')
        if not llm_service_instance:
            current_app.logger.error("LLMService не инициализирован в app.config.")
            raise RuntimeError("LLMService не инициализирован")
        return llm_service_instance

    def get_product_generator_instance():
        """Вспомогательная функция для получения TelegramProductGenerator"""
        llm_service_instance = get_llm_service_instance()
        return TelegramProductGenerator(llm_service=llm_service_instance)

    def get_telegram_connector():
        """Ленивая инициализация Telegram коннектора"""
        nonlocal telegram_connector
        if telegram_connector is None:
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if bot_token:
                telegram_connector = TelegramConnector(
                    bot_token=bot_token,
                    channel_username='aideaxondemos'
                )
        return telegram_connector
    
    # Путь к директории с SEO-страницами
    # Используем current_app.root_path, который указывает на корень проекта hababru
    CONTENT_BASE_PATH = None # Будет инициализирован в функции, чтобы получить доступ к current_app

    @blueprint.route('/seo_pages_list', methods=['GET'])
    def get_seo_pages_list():
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        pages_data = []
        
        # Инициализируем CONTENT_BASE_PATH здесь, чтобы иметь доступ к current_app
        nonlocal CONTENT_BASE_PATH # Используем nonlocal для изменения переменной из внешней области видимости
        if CONTENT_BASE_PATH is None:
            CONTENT_BASE_PATH = os.path.join(current_app.root_path, 'content', 'seo_pages')

        app_logger.info(f"Попытка получить список SEO-страниц из: {CONTENT_BASE_PATH}")

        # Проверяем, существует ли директория
        if not os.path.exists(CONTENT_BASE_PATH):
            app_logger.error(f"Директория SEO-контента не найдена: {CONTENT_BASE_PATH}")
            return jsonify({"error": "SEO content directory not found"}), 500

        for slug in os.listdir(CONTENT_BASE_PATH):
            page_dir = os.path.join(CONTENT_BASE_PATH, slug)
            source_md_path = os.path.join(page_dir, 'source.md')

            if os.path.isdir(page_dir) and os.path.exists(source_md_path):
                try:
                    with open(source_md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    parts = content.split('---', 2)
                    if len(parts) < 3:
                        app_logger.warning(f"Некорректный формат source.md для {slug}: отсутствует YAML Front Matter.")
                        continue # Пропускаем некорректные файлы

                    front_matter = yaml.safe_load(parts[1])
                    
                    # Получаем информацию о связанном продукте
                    product_id = front_matter.get('product_id')
                    product_info = {}
                    if product_id:
                        product = product_registry.get_product(product_id)
                        if product:
                            product_info = {
                                'product_id': product_id,
                                'product_name': product.name,
                                'product_description': product.description
                            }
                    
                    pages_data.append({
                        "slug": slug,
                        "title": front_matter.get("title", slug),
                        "meta_keywords": front_matter.get("meta_keywords", []),
                        "meta_description": front_matter.get("meta_description", ""),
                        "main_keyword": front_matter.get("main_keyword", slug),
                        "contract_file": front_matter.get("contract_file", "generated_contract.txt"),
                        "product_info": product_info
                    })
                    app_logger.info(f"Успешно загружена SEO-страница: {slug}")
                except Exception as e:
                    app_logger.error(f"Ошибка при чтении SEO-страницы {slug} ({source_md_path}): {e}", exc_info=True)
                    continue
        app_logger.info(f"Загружено {len(pages_data)} SEO-страниц.")
        return jsonify(pages_data)

    @blueprint.route('/run_openai_prompt', methods=['POST'])
    def run_openai_prompt():
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на /api/v1/run_openai_prompt")

        data = request.get_json()
        slug = data.get('slug')
        prompt_template = data.get('prompt')
        output_filename_prefix = data.get('output_filename_prefix')
        page_data = data.get('page_data')
        force_new_run = data.get('force_new_run', False) # Новый параметр
        selected_model = data.get('selected_model') # Новый параметр: выбранная модель LLM

        llm_service_instance = get_llm_service_instance() # Получаем LLMService здесь

        # Устанавливаем выбранную модель в LLMService перед выполнением промпта
        if selected_model:
            try:
                llm_service_instance.set_current_model(selected_model)
                app_logger.info(f"LLMService: Установлена модель для выполнения промпта: {selected_model}")
            except ValueError as e:
                app_logger.error(f"Ошибка установки модели LLM: {e}")
                return jsonify({"error": str(e)}), 400

        if not all([slug, prompt_template, output_filename_prefix, page_data]):
            app_logger.error(f"Отсутствуют необходимые параметры для run_openai_prompt. Получено: slug={slug}, prompt_template={prompt_template[:50] if prompt_template else 'None'}, output_filename_prefix={output_filename_prefix}, page_data_keys={page_data.keys() if page_data else 'None'}")
            return jsonify({"error": "Отсутствуют необходимые параметры"}), 400

        seo_prompt_service = current_app.config.get('SEO_PROMPT_SERVICE')
        cache_service = current_app.config.get('CACHE_SERVICE') # Получаем сервис кэширования

        if not seo_prompt_service:
            app_logger.error("SeoPromptService не инициализирован в app.config.")
            return jsonify({"error": "SeoPromptService не инициализирован"}), 500
        if not cache_service:
            app_logger.error("CacheService не инициализирован в app.config.")
            return jsonify({"error": "CacheService не инициализирован"}), 500

        try:
            if force_new_run:
                app_logger.info(f"Запрос на сброс кэша для {slug} с префиксом {output_filename_prefix}")
                cache_service.delete_prompt_result(slug, output_filename_prefix)
                app_logger.info(f"Кэш для {slug} с префиксом {output_filename_prefix} сброшен.")

            app_logger.info(f"Вызов seo_prompt_service.run_openai_prompt_for_page для слага: {slug}")
            result = seo_prompt_service.run_openai_prompt_for_page(slug, prompt_template, output_filename_prefix, page_data)
            app_logger.info(f"Промпт для {slug} успешно выполнен. Результат сохранен в: {result.get('output_file_path')}")
            return jsonify(result), 200
        except Exception as e:
            app_logger.error(f"Ошибка при выполнении промпта OpenAI для {slug}: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/get_prompt_result', methods=['GET'])
    def get_prompt_result():
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        slug = request.args.get('slug')
        output_filename_prefix = request.args.get('output_filename_prefix')

        if not all([slug, output_filename_prefix]):
            app_logger.error(f"Отсутствуют необходимые параметры для get_prompt_result. Получено: slug={slug}, output_filename_prefix={output_filename_prefix}")
            return jsonify({"error": "Отсутствуют необходимые параметры"}), 400

        nonlocal CONTENT_BASE_PATH # Используем nonlocal для изменения переменной из внешней области видимости
        if CONTENT_BASE_PATH is None:
            CONTENT_BASE_PATH = os.path.join(current_app.root_path, 'content', 'seo_pages')

        page_dir = os.path.join(CONTENT_BASE_PATH, slug)
        
        found_file = None
        for filename in os.listdir(page_dir):
            if filename.startswith(output_filename_prefix) and filename.endswith('.txt'):
                found_file = filename
                break

        if found_file:
            file_path = os.path.join(page_dir, found_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                app_logger.info(f"Найден и возвращен существующий результат промпта для {slug} с префиксом {output_filename_prefix}")
                return jsonify({"status": "ok", "llm_output": content, "output_file_path": file_path}), 200
            except Exception as e:
                app_logger.error(f"Ошибка при чтении существующего файла результата {file_path}: {e}", exc_info=True)
                return jsonify({"error": f"Ошибка при чтении существующего файла результата: {str(e)}"}), 500
        else:
            app_logger.info(f"Существующий результат промпта для {slug} с префиксом {output_filename_prefix} не найден.")
            return jsonify({"status": "not_found", "message": "Результат не найден"}), 404

    @blueprint.route('/get_page_prompt_results', methods=['GET'])
    def get_page_prompt_results():
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        slug = request.args.get('slug')

        if not slug:
            app_logger.error("Отсутствует параметр 'slug' для get_page_prompt_results.")
            return jsonify({"error": "Отсутствует параметр 'slug'"}), 400

        cache_service = current_app.config.get('CACHE_SERVICE')
        if not cache_service:
            app_logger.error("CacheService не инициализирован в app.config.")
            return jsonify({"error": "CacheService не инициализирован"}), 500

        try:
            results = cache_service.get_all_prompt_results_for_page(slug)
            app_logger.info(f"Возвращено {len(results)} результатов промптов для страницы {slug}.")
            return jsonify({"status": "ok", "results": results}), 200
        except Exception as e:
            app_logger.error(f"Ошибка при получении всех результатов промптов для страницы {slug}: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500
    
    @blueprint.route('/get_llm_models', methods=['GET'])
    def get_llm_models():
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        try:
            llm_service_instance = get_llm_service_instance() # Получаем LLMService здесь
            available_models = llm_service_instance.get_available_models()
            app_logger.info(f"Возвращен список доступных LLM моделей: {available_models}")
            return jsonify(available_models), 200
        except Exception as e:
            app_logger.error(f"Ошибка при получении списка LLM моделей: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/generate_page', methods=['POST'])
    def generate_page():
        """API для создания одной SEO-страницы"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на /api/v1/generate_page")

        data = request.get_json()
        keyword = data.get('keyword')
        model = data.get('model', 'deepseek')
        skip_existing = data.get('skipExisting', True)

        if not keyword:
            app_logger.error("Отсутствует параметр keyword")
            return jsonify({"error": "Ключевое слово обязательно"}), 400

        try:
            # Используем CLI скрипт через subprocess для генерации
            import subprocess
            import os
            
            # Формируем команду
            script_path = os.path.join(current_app.root_path, 'src', 'backend', 'cli', 'generate_seo_page.py')
            cmd = ['python', script_path, '--keyword', keyword]
            
            app_logger.info(f"Запуск генерации страницы: {cmd}")
            
            # Запускаем скрипт
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_app.root_path)
            
            if result.returncode != 0:
                app_logger.error(f"Ошибка генерации страницы: {result.stderr}")
                return jsonify({"error": f"Ошибка генерации: {result.stderr}"}), 500
            
            # Извлекаем слаг из вывода скрипта
            import re
            slug_match = re.search(r"Страница будет доступна по URL: /([^\\s]+)", result.stdout)
            slug = slug_match.group(1) if slug_match else None
            
            app_logger.info(f"Страница успешно создана: {slug}")
            return jsonify({
                "success": True,
                "message": "Страница успешно создана",
                "slug": slug,
                "output": result.stdout
            })
            
        except Exception as e:
            app_logger.error(f"Ошибка при создании страницы: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/delete_page/<slug>', methods=['DELETE'])
    def delete_page(slug):
        """API для удаления SEO-страницы"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info(f"Получен запрос на удаление страницы: {slug}")

        try:
            import shutil
            
            # Путь к директории страницы
            page_dir = os.path.join(current_app.root_path, 'content', 'seo_pages', slug)
            
            if not os.path.exists(page_dir):
                app_logger.error(f"Страница не найдена: {slug}")
                return jsonify({"error": "Страница не найдена"}), 404
            
            # Удаляем директорию страницы
            shutil.rmtree(page_dir)
            
            app_logger.info(f"Страница успешно удалена: {slug}")
            return jsonify({
                "success": True,
                "message": f"Страница {slug} успешно удалена"
            })
            
        except Exception as e:
            app_logger.error(f"Ошибка при удалении страницы {slug}: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/bulk_generate_pages', methods=['POST'])
    def bulk_generate_pages():
        """API для массовой генерации SEO-страниц"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на /api/v1/bulk_generate_pages")

        data = request.get_json()
        keywords = data.get('keywords', [])
        delay = data.get('delay', 2)
        skip_existing = data.get('skipExisting', True)

        if not keywords:
            app_logger.error("Отсутствует список ключевых слов")
            return jsonify({"error": "Список ключевых слов обязателен"}), 400

        try:
            import subprocess
            import os
            import tempfile
            
            # Создаем временный файл с ключевыми словами
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
                for keyword in keywords:
                    f.write(f"{keyword}\\n")
                temp_file = f.name
            
            try:
                # Формируем команду для bulk_seo_generator
                script_path = os.path.join(current_app.root_path, 'src', 'backend', 'cli', 'bulk_seo_generator.py')
                cmd = [
                    'python', script_path, 
                    '--keywords-file', temp_file,
                    '--delay', str(delay)
                ]
                
                if skip_existing:
                    # По умолчанию bulk_seo_generator пропускает существующие
                    pass
                else:
                    cmd.append('--no-skip')
                
                app_logger.info(f"Запуск массовой генерации: {cmd}")
                
                # Запускаем скрипт
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_app.root_path)
                
                if result.returncode != 0:
                    app_logger.error(f"Ошибка массовой генерации: {result.stderr}")
                    return jsonify({"error": f"Ошибка генерации: {result.stderr}"}), 500
                
                # Парсим результат
                import re
                success_match = re.search(r"Успешно создано: (\\d+)", result.stdout)
                failed_match = re.search(r"Ошибки: (\\d+)", result.stdout)
                
                success_count = int(success_match.group(1)) if success_match else 0
                failed_count = int(failed_match.group(1)) if failed_match else 0
                
                app_logger.info(f"Массовая генерация завершена. Успешно: {success_count}, Ошибок: {failed_count}")
                return jsonify({
                    "success": True,
                    "message": f"Массовая генерация завершена",
                    "success": success_count,
                    "failed": failed_count,
                    "output": result.stdout
                })
                
            finally:
                # Удаляем временный файл
                os.unlink(temp_file)
            
        except Exception as e:
            app_logger.error(f"Ошибка при массовой генерации: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/generate_cluster', methods=['POST'])
    def generate_cluster():
        """API для генерации семантического кластера"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на /api/v1/generate_cluster")

        data = request.get_json()
        keyword = data.get('keyword')
        size = data.get('size', 5)

        if not keyword:
            app_logger.error("Отсутствует параметр keyword")
            return jsonify({"error": "Ключевое слово обязательно"}), 400

        try:
            import subprocess
            import os
            
            # Формируем команду для bulk_seo_generator с генерацией кластера
            script_path = os.path.join(current_app.root_path, 'src', 'backend', 'cli', 'bulk_seo_generator.py')
            cmd = [
                'python', script_path, 
                '--cluster', keyword,
                '--cluster-size', str(size)
            ]
            
            app_logger.info(f"Запуск генерации кластера: {cmd}")
            
            # Запускаем скрипт
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_app.root_path)
            
            if result.returncode != 0:
                app_logger.error(f"Ошибка генерации кластера: {result.stderr}")
                return jsonify({"error": f"Ошибка генерации кластера: {result.stderr}"}), 500
            
            app_logger.info(f"Кластер успешно создан для ключевого слова: {keyword}")
            return jsonify({
                "success": True,
                "message": f"Кластер для '{keyword}' успешно создан",
                "output": result.stdout
            })
            
        except Exception as e:
            app_logger.error(f"Ошибка при генерации кластера: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/products', methods=['GET'])
    def get_products():
        """API для получения списка всех продуктов"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на /api/v1/products")

        try:
            from src.backend.services.products import product_registry
            
            products = []
            for product_id, product in product_registry.get_all_products().items():
                product_info = product.get_product_info()
                seo_pages = product_registry.get_seo_pages_for_product(product_id)
                
                products.append({
                    "product_id": product_id,
                    "name": product_info.get('name', ''),
                    "description": product_info.get('description', ''),
                    "seo_pages_count": len(seo_pages),
                    "target_audience": product_info.get('target_audience', []),
                    "key_benefits": product_info.get('key_benefits', [])
                })
            
            return jsonify(products)
            
        except Exception as e:
            app_logger.error(f"Ошибка получения списка продуктов: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/products/stats', methods=['GET'])
    def get_products_stats():
        """API для получения статистики по продуктам"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на /api/v1/products/stats")

        try:
            from src.backend.services.products import product_registry
            import os
            import yaml
            
            stats = {}
            
            # Сканируем папку с SEO-страницами напрямую
            content_base_path = os.path.join(current_app.root_path, 'content', 'seo_pages')
            app_logger.info(f"Сканируем директорию: {content_base_path}")
            
            for product_id, product in product_registry.get_all_products().items():
                stats[product_id] = {
                    "seo_pages_count": 0,
                    "active": True
                }
            
            # Подсчитываем SEO-страницы по product_id в файлах
            if os.path.exists(content_base_path):
                for folder_name in os.listdir(content_base_path):
                    folder_path = os.path.join(content_base_path, folder_name)
                    if os.path.isdir(folder_path):
                        source_file = os.path.join(folder_path, 'source.md')
                        if os.path.exists(source_file):
                            try:
                                with open(source_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    
                                # Извлекаем YAML front matter
                                if content.startswith('---'):
                                    yaml_end = content.find('\n---\n', 4)
                                    if yaml_end > 0:
                                        yaml_content = content[4:yaml_end]
                                        front_matter = yaml.safe_load(yaml_content)
                                        product_id = front_matter.get('product_id')
                                        
                                        if product_id and product_id in stats:
                                            stats[product_id]["seo_pages_count"] += 1
                                            app_logger.info(f"Найдена страница для продукта {product_id}: {folder_name}")
                                            
                            except Exception as e:
                                app_logger.warning(f"Ошибка обработки файла {source_file}: {e}")
            
            app_logger.info(f"Итоговая статистика: {stats}")
            return jsonify(stats)
            
        except Exception as e:
            app_logger.error(f"Ошибка получения статистики продуктов: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/products', methods=['POST'])
    def create_product():
        """API для создания нового продукта"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на создание продукта /api/v1/products")

        data = request.get_json()
        product_id = data.get('product_id')
        name = data.get('name')
        description = data.get('description')
        target_audience = data.get('target_audience', [])
        key_benefits = data.get('key_benefits', [])

        if not all([product_id, name, description]):
            return jsonify({"error": "Обязательные поля: product_id, name, description"}), 400

        try:
            # Здесь будет логика создания нового продукта
            # Пока что возвращаем заглушку
            app_logger.info(f"Создание продукта: {product_id} - {name}")
            
            return jsonify({
                "success": True,
                "message": f"Продукт '{name}' будет создан в следующей версии",
                "product_id": product_id
            })
            
        except Exception as e:
            app_logger.error(f"Ошибка создания продукта: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/products/<product_id>/seo_pages', methods=['POST'])
    def create_seo_pages_for_product():
        """API для создания SEO-страниц для конкретного продукта"""
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        app_logger.info("Получен запрос на создание SEO-страниц для продукта")

        data = request.get_json()
        product_id = data.get('product_id')
        keywords = data.get('keywords', [])
        theme = data.get('theme', '')

        try:
            from src.backend.services.products import product_registry
            
            product = product_registry.get_product(product_id)
            if not product:
                return jsonify({"error": f"Продукт {product_id} не найден"}), 404

            # Здесь будет логика создания SEO-страниц для продукта
            seo_service = current_app.config.get('SEO_SERVICE')
            if not seo_service:
                return jsonify({"error": "SEO Service не инициализирован"}), 500

            created_pages = []
            for keyword in keywords:
                slug = keyword.lower().replace(' ', '-').replace(',', '')
                try:
                    success = seo_service.create_seo_page_with_product(
                        slug=slug,
                        title=f"{keyword} - {product.name}",
                        keywords=[keyword],
                        product_id=product_id,
                        meta_description=f"{keyword} с помощью {product.name}"
                    )
                    if success:
                        created_pages.append({
                            "slug": slug,
                            "title": f"{keyword} - {product.name}",
                            "keyword": keyword
                        })
                except Exception as e:
                    app_logger.warning(f"Не удалось создать страницу для {keyword}: {e}")

            return jsonify({
                "success": True,
                "product_name": product.name,
                "pages_created": len(created_pages),
                "created_pages": created_pages
            })
            
        except Exception as e:
            app_logger.error(f"Ошибка создания SEO-страниц для продукта: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @blueprint.route('/admin/seo')
    def seo_admin():
        """Страница администрирования SEO и Telegram"""
        return render_template('seo_admin_template.html', 
                             seo_pages=seo_service.get_all_seo_pages(),
                             telegram_enabled=bool(os.getenv('TELEGRAM_BOT_TOKEN')))
    
    @blueprint.route('/admin/telegram/messages', methods=['GET'])
    def get_telegram_messages():
        """Получение последних сообщений из Telegram канала"""
        try:
            connector = get_telegram_connector()
            if not connector:
                return jsonify({
                    'success': False,
                    'error': 'Telegram не настроен. Добавьте TELEGRAM_BOT_TOKEN в .env'
                }), 400
            
            limit = request.args.get('limit', 10, type=int)
            
            # Получаем сообщения
            messages = connector.fetch_recent_messages(limit=limit)
            
            # Фильтруем подходящие для генерации продуктов
            suitable_messages = []
            for msg in messages:
                is_suitable = product_generator._is_suitable_for_product_generation(msg)
                
                suitable_messages.append({
                    'message_id': msg.message_id,
                    'text': msg.text,
                    'date': msg.date,
                    'media_files': msg.media_files,
                    'is_suitable': is_suitable,
                    'text_preview': msg.text[:200] + '...' if len(msg.text) > 200 else msg.text
                })
            
            return jsonify({
                'success': True,
                'messages': suitable_messages,
                'total_count': len(messages)
            })
            
        except Exception as e:
            current_app.logger.error(f"Ошибка получения Telegram сообщений: {e}")
            return jsonify({
                'success': False,
                'error': f'Ошибка получения сообщений: {str(e)}'
            }), 500
    
    @blueprint.route('/admin/telegram/generate', methods=['POST'])
    def generate_product_from_telegram():
        """Генерация продукта из Telegram сообщения"""
        try:
            data = request.get_json()
            
            if not data or 'message_id' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Не указан message_id'
                }), 400
            
            # Получаем сообщение
            connector = get_telegram_connector()
            if not connector:
                return jsonify({
                    'success': False,
                    'error': 'Telegram не настроен'
                }), 400
            
            messages = connector.fetch_recent_messages(limit=50)
            target_message = None
            
            for msg in messages:
                if msg.message_id == data['message_id']:
                    target_message = msg
                    break
            
            if not target_message:
                return jsonify({
                    'success': False,
                    'error': 'Сообщение не найдено'
                }), 404
            
            product_generator_instance = get_product_generator_instance() # Получаем генератор здесь
            # Генерируем продукт
            result = product_generator_instance.generate_product_from_message(target_message)
            
            return jsonify(result)
            
        except Exception as e:
            current_app.logger.error(f"Ошибка генерации продукта: {e}") # Используем current_app.logger
            return jsonify({
                'success': False,
                'error': f'Ошибка генерации: {str(e)}'
            }), 500
    
    @blueprint.route('/admin/telegram/check-duplicates', methods=['POST'])
    def check_telegram_duplicates():
        """Проверка на дубли перед генерацией"""
        try:
            data = request.get_json()
            
            if not data or 'message_id' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Не указан message_id'
                }), 400
            
            # Получаем сообщение
            connector = get_telegram_connector()
            if not connector:
                return jsonify({
                    'success': False,
                    'error': 'Telegram не настроен'
                }), 400
            
            messages = connector.fetch_recent_messages(limit=50)
            target_message = None
            
            for msg in messages:
                if msg.message_id == data['message_id']:
                    target_message = msg
                    break
            
            if not target_message:
                return jsonify({
                    'success': False,
                    'error': 'Сообщение не найдено'
                }), 404
            
            product_generator_instance = get_product_generator_instance() # Получаем генератор здесь
            # Проверяем на дубли
            duplicate_id = product_generator_instance._check_semantic_duplicate(target_message)
            
            if duplicate_id:
                # Получаем информацию о дубликате
                existing_products = product_generator_instance._get_existing_products_with_data()
                duplicate_product = existing_products.get(duplicate_id, {})
                
                return jsonify({
                    'success': True,
                    'has_duplicate': True,
                    'duplicate_product_id': duplicate_id,
                    'duplicate_product_name': duplicate_product.get('name', 'Неизвестно'),
                    'duplicate_product_description': duplicate_product.get('description', '')
                })
            else:
                return jsonify({
                    'success': True,
                    'has_duplicate': False
                })
                
        except Exception as e:
            current_app.logger.error(f"Ошибка проверки дублей: {e}") # Используем current_app.logger
            return jsonify({
                'success': False,
                'error': f'Ошибка проверки: {str(e)}'
            }), 500
    
    @blueprint.route('/admin/telegram/products', methods=['GET'])
    def get_existing_products():
        """Получение списка существующих продуктов"""
        try:
            product_generator_instance = get_product_generator_instance() # Получаем генератор здесь
            existing_products = product_generator_instance._get_existing_products_with_data()
            
            products_list = []
            for product_id, product_data in existing_products.items():
                products_list.append({
                    'product_id': product_id,
                    'name': product_data.get('name', 'Без названия'),
                    'description': product_data.get('description', ''),
                    'category': product_data.get('category', 'other'),
                    'status': product_data.get('status', 'active')
                })
            
            return jsonify({
                'success': True,
                'products': products_list,
                'total_count': len(products_list)
            })
            
        except Exception as e:
            current_app.logger.error(f"Ошибка получения списка продуктов: {e}") # Используем current_app.logger
            return jsonify({
                'success': False,
                'error': f'Ошибка получения продуктов: {str(e)}'
            }), 500
    
    @blueprint.route('/admin/telegram/regenerate', methods=['POST'])
    def regenerate_product_with_model():
        """Перегенерация продукта из Telegram сообщения с выбором модели"""
        try:
            data = request.get_json()
            
            if not data or 'message_id' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Не указан message_id'
                }), 400
            
            # Получаем параметры
            message_id = data['message_id']
            selected_model = data.get('model', 'deepseek-chat')
            force_regenerate = data.get('force_regenerate', False)
            
            # Получаем сообщение
            connector = get_telegram_connector()
            if not connector:
                return jsonify({
                    'success': False,
                    'error': 'Telegram не настроен'
                }), 400
            
            messages = connector.fetch_recent_messages(limit=50)
            target_message = None
            
            for msg in messages:
                if msg.message_id == message_id:
                    target_message = msg
                    break
            
            if not target_message:
                return jsonify({
                    'success': False,
                    'error': 'Сообщение не найдено'
                }), 404
            
            # Устанавливаем выбранную модель
            if selected_model:
                try:
                    llm_service_instance = get_llm_service_instance() # Получаем LLMService здесь
                    llm_service_instance.set_current_model(selected_model)
                    current_app.logger.info(f"Установлена модель для регенерации: {selected_model}")
                except ValueError as e:
                    current_app.logger.error(f"Ошибка установки модели: {e}")
                    return jsonify({
                        'success': False,
                        'error': f'Некорректная модель: {str(e)}'
                    }), 400
            
            product_generator_instance = get_product_generator_instance() # Получаем генератор здесь
            # Проверяем на дубли только если не принудительная регенерация
            if not force_regenerate:
                duplicate_id = product_generator_instance._check_semantic_duplicate(target_message)
                if duplicate_id:
                    existing_products = product_generator_instance._get_existing_products_with_data()
                    duplicate_product = existing_products.get(duplicate_id, {})
                    
                    return jsonify({
                        'success': False,
                        'error': f'Продукт с похожим смыслом уже существует: {duplicate_id}',
                        'duplicate_product_id': duplicate_id,
                        'duplicate_product_name': duplicate_product.get('name', 'Неизвестно'),
                        'duplicate_product_description': duplicate_product.get('description', '')
                    })
            
            # Генерируем продукт с выбранной моделью
            result = product_generator_instance.generate_product_from_message(target_message)
            
            # Добавляем информацию о модели в результат
            if result.get('success'):
                result['model_used'] = selected_model
                result['regenerated'] = True
            
            return jsonify(result)
            
        except Exception as e:
            current_app.logger.error(f"Ошибка регенерации продукта: {e}")
            return jsonify({
                'success': False,
                'error': f'Ошибка регенерации: {str(e)}'
            }), 500

    @blueprint.route('/admin/telegram/models', methods=['GET'])
    def get_available_models():
        """Получение списка доступных моделей для генерации"""
        try:
            llm_service_instance = get_llm_service_instance() # Получаем LLMService здесь
            models = llm_service_instance.get_available_models()
            current_model = llm_service_instance.current_model_full_id if llm_service_instance.current_model_full_id else "" # Изменено: используем current_model_full_id и проверяем на None
            
            # Добавляем информацию о каждой модели
            models_info = []
            for model in models:
                model_info = llm_service_instance.get_model_info(model)
                models_info.append({
                    'id': model,
                    'name': model,
                    'provider': model_info.get('provider', 'Unknown'),
                    'description': model_info.get('description', ''),
                    'context_length': model_info.get('context_length', 'Unknown')
                })
            
            return jsonify({
                'success': True,
                'models': models,
                'models_info': models_info,
                'current_model': current_model
            })
            
        except Exception as e:
            current_app.logger.error(f"Ошибка получения моделей: {e}")
            return jsonify({
                'success': False,
                'error': f'Ошибка получения моделей: {str(e)}'
            }), 500

    @blueprint.route('/admin/telegram/batch-regenerate', methods=['POST'])
    def batch_regenerate_products():
        """Массовая перегенерация существующих продуктов с новой моделью"""
        try:
            data = request.get_json()
            
            selected_model = data.get('model', 'deepseek:deepseek-chat') # Изменено: дефолтная модель с префиксом
            product_ids = data.get('product_ids', [])
            
            if not product_ids:
                return jsonify({
                    'success': False,
                    'error': 'Не указаны product_ids для перегенерации'
                }), 400
            
            llm_service_instance = get_llm_service_instance() # Получаем LLMService здесь
            # Устанавливаем выбранную модель
            try:
                llm_service_instance.set_current_model(selected_model)
                current_app.logger.info(f"Установлена модель для массовой регенерации: {selected_model}")
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': f'Некорректная модель: {str(e)}'
                }), 400
            
            product_generator_instance = get_product_generator_instance() # Получаем генератор здесь
            # Получаем существующие продукты
            existing_products = product_generator_instance._get_existing_products_with_data()
            
            results = {
                'success': True,
                'model_used': selected_model,
                'total_requested': len(product_ids),
                'regenerated': 0,
                'failed': 0,
                'results': []
            }
            
            for product_id in product_ids:
                try:
                    if product_id not in existing_products:
                        results['results'].append({
                            'product_id': product_id,
                            'success': False,
                            'error': 'Продукт не найден'
                        })
                        results['failed'] += 1
                        continue
                    
                    # Создаем временное сообщение из существующего продукта
                    product_data = existing_products[product_id]
                    temp_message = TelegramMessage(
                        message_id=999999,  # Временный ID
                        text=f"{product_data.get('name', '')} - {product_data.get('description', '')}",
                        date="2025-01-03T00:00:00Z",
                        media_files=[]
                    )
                    
                    # Удаляем старый файл продукта
                    import os
                    old_file_path = product_generator_instance.products_dir / f"{product_id}.yaml" # Изменено
                    if old_file_path.exists():
                        os.remove(old_file_path)
                    
                    # Перегенерируем продукт
                    result = product_generator_instance.generate_product_from_message(temp_message)
                    
                    if result.get('success'):
                        results['regenerated'] += 1
                        results['results'].append({
                            'product_id': product_id,
                            'success': True,
                            'new_product_id': result.get('product_id'),
                            'new_product_name': result.get('product_name')
                        })
                    else:
                        results['failed'] += 1
                        results['results'].append({
                            'product_id': product_id,
                            'success': False,
                            'error': result.get('error', 'Неизвестная ошибка')
                        })
                        
                except Exception as e:
                    current_app.logger.error(f"Ошибка регенерации продукта {product_id}: {e}")
                    results['failed'] += 1
                    results['results'].append({
                        'product_id': product_id,
                        'success': False,
                        'error': str(e)
                    })
            
            return jsonify(results)
            
        except Exception as e:
            current_app.logger.error(f"Ошибка массовой регенерации: {e}")
            return jsonify({
                'success': False,
                'error': f'Ошибка массовой регенерации: {str(e)}'
            }), 500

    return blueprint
