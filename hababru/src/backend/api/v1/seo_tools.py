from flask import Blueprint, jsonify, request
import os
import yaml
import markdown
from flask import current_app
import logging
from src.backend.services.llm_service import LLMService # Импортируем LLMService

def create_seo_tools_blueprint(llm_service: LLMService):
    seo_tools_bp = Blueprint('seo_tools', __name__)

    # Путь к директории с SEO-страницами
    # Используем current_app.root_path, который указывает на корень проекта hababru
    CONTENT_BASE_PATH = None # Будет инициализирован в функции, чтобы получить доступ к current_app

    @seo_tools_bp.route('/seo_pages_list', methods=['GET'])
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
                    
                    pages_data.append({
                        "slug": slug,
                        "title": front_matter.get("title", slug),
                        "meta_keywords": front_matter.get("meta_keywords", []),
                        "meta_description": front_matter.get("meta_description", ""),
                        "main_keyword": front_matter.get("main_keyword", slug),
                        "contract_file": front_matter.get("contract_file", "generated_contract.txt")
                    })
                    app_logger.info(f"Успешно загружена SEO-страница: {slug}")
                except Exception as e:
                    app_logger.error(f"Ошибка при чтении SEO-страницы {slug} ({source_md_path}): {e}", exc_info=True)
                    continue
        app_logger.info(f"Загружено {len(pages_data)} SEO-страниц.")
        return jsonify(pages_data)

    @seo_tools_bp.route('/run_openai_prompt', methods=['POST'])
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

        # Устанавливаем выбранную модель в LLMService перед выполнением промпта
        if selected_model:
            try:
                llm_service.set_current_model(selected_model)
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

    @seo_tools_bp.route('/get_prompt_result', methods=['GET'])
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

    @seo_tools_bp.route('/get_page_prompt_results', methods=['GET'])
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
    
    @seo_tools_bp.route('/get_llm_models', methods=['GET'])
    def get_llm_models():
        app_logger = current_app.logger if current_app else logging.getLogger(__name__)
        # Используем llm_service, переданный в create_seo_tools_blueprint
        if not llm_service:
            app_logger.error("LLMService не инициализирован в Blueprint.")
            return jsonify({"error": "LLMService не инициализирован"}), 500
        
        try:
            available_models = llm_service.get_available_models()
            app_logger.info(f"Возвращен список доступных LLM моделей: {available_models}")
            return jsonify(available_models), 200
        except Exception as e:
            app_logger.error(f"Ошибка при получении списка LLM моделей: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    return seo_tools_bp
