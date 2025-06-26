import os
from flask import Flask, render_template, send_from_directory, abort, jsonify, request
from dotenv import load_dotenv
import subprocess
import io

# Импорты сервисов
from .api.v1.contract_analyzer import contract_analyzer_bp
from .api.v1.seo_tools import create_seo_tools_blueprint
from .services.llm_service import LLMService
from .services.seo_service import SeoService
from .services.seo_prompt_service import SeoPromptService
from .services.parsing_service import ParsingService
from .services.cache_service import CacheService

# Загрузка переменных окружения из .env файла
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Настройка логирования для отладки
import logging

def create_app(
    llm_service_mock=None,
    parsing_service_mock=None,
    cache_service_mock=None,
    seo_service_mock=None,
    seo_prompt_service_mock=None
):
    app = Flask(__name__, 
                root_path=os.path.join(os.path.dirname(__file__), '..', '..'),
                static_folder='public',
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

    app.logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Инициализация сервисов (используем моки, если они предоставлены)
    llm_service = llm_service_mock if llm_service_mock else LLMService(
        deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    parsing_service = parsing_service_mock if parsing_service_mock else ParsingService(llm_service=llm_service)
    cache_service = cache_service_mock if cache_service_mock else CacheService(cache_dir=os.path.join(app.root_path, 'data', 'cache'))
    seo_service = seo_service_mock if seo_service_mock else SeoService(
        llm_service=llm_service,
        parsing_service=parsing_service,
        content_base_path=os.path.join(app.root_path, 'content', 'seo_pages')
    )
    seo_prompt_service = seo_prompt_service_mock if seo_prompt_service_mock else SeoPromptService(
        llm_service=llm_service,
        content_base_path=os.path.join(app.root_path, 'content', 'seo_pages')
    )

    # Сохраняем экземпляры сервисов в конфигурации приложения, чтобы они были доступны в Blueprint
    app.config['PARSING_SERVICE'] = parsing_service
    app.config['LLM_SERVICE'] = llm_service
    app.config['CACHE_SERVICE'] = cache_service
    app.config['SEO_SERVICE'] = seo_service # Добавляем SEO_SERVICE в app.config
    app.config['SEO_PROMPT_SERVICE'] = seo_prompt_service

    # Регистрация Blueprint для API
    app.register_blueprint(contract_analyzer_bp, url_prefix='/api/v1')
    app.register_blueprint(create_seo_tools_blueprint(llm_service), url_prefix='/api/v1')

    @app.before_request
    def log_request_info():
        app.logger.info(f"Входящий запрос: {request.method} {request.path}")
        if request.is_json:
            app.logger.info(f"JSON данные: {request.json}")
        elif request.form:
            app.logger.info(f"Form данные: {request.form}")

    # Маршрут для главной страницы приложения
    @app.route('/')
    def index():
        return render_template(
            'index_template.html',
            is_seo_page=False,
            main_keyword=None,
            contract_text_raw=None,
            analysis_results_raw=None
        )

    # Новый маршрут для страницы администрирования SEO
    @app.route('/seo_admin')
    def seo_admin():
        app.logger.info("Запрос к странице администрирования SEO.")
        return render_template('seo_admin_template.html')

    # Маршрут для обслуживания статических файлов (CSS, JS, assets)
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/robots.txt')
    def serve_robots_txt():
        return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')

    # Новый маршрут для обслуживания файлов из content/seo_prompts
    @app.route('/content/seo_prompts/<path:filename>')
    def serve_seo_prompts(filename):
        return send_from_directory(os.path.join(app.root_path, 'content', 'seo_prompts'), filename)

    # Маршрут для страницы анализа договора по ID
    @app.route('/analyze/<contract_id>')
    def analyze_contract_page(contract_id):
        app.logger.info(f"Запрос на страницу анализа договора с ID: {contract_id}")
        return render_template('index_template.html', contract_id=contract_id, is_seo_page=False)

    # Маршрут для обслуживания файлов из data/sample_contracts
    @app.route('/data/sample_contracts/<path:filename>')
    def serve_sample_contract(filename):
        return send_from_directory(os.path.join(app.root_path, 'data', 'sample_contracts'), filename)

    # Маршрут для обслуживания сгенерированных файлов договоров для SEO-страниц
    @app.route('/content/seo_pages/<slug>/<filename>')
    def serve_generated_contract(slug, filename):
        if filename != 'generated_contract.txt':
            abort(404)
        file_path = os.path.join(app.root_path, 'content', 'seo_pages', slug)
        return send_from_directory(file_path, filename)

    @app.route('/get_test_contract', methods=['GET'])
    def get_test_contract():
        app.logger.info('API: Получен запрос на /get_test_contract (без параметров)')
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        file_to_parse = os.path.join(
            project_root, 'content', 'seo_pages', 'analiz-dogovora-arendy', 'generated_contract.txt'
        )
        app.logger.info(f'API: Попытка загрузить тестовый файл по явному пути: {file_to_parse}')
        if not os.path.exists(file_to_parse) or not os.path.isfile(file_to_parse):
            app.logger.error(f'API: Тестовый файл не найден по явному пути: {file_to_parse}')
            return jsonify({"error": "Тестовый файл не найден"}), 404
        app.logger.info(f'API: Конечный путь к файлу для парсинга: {file_to_parse}')
        try:
            with open(file_to_parse, 'rb') as f:
                file_stream = io.BytesIO(f.read())
            filename = os.path.basename(file_to_parse)
            _parsing_service = app.config.get('PARSING_SERVICE')
            app.logger.info(f'API: Конвертация тестового файла {filename} в Markdown...')
            app.logger.info(f'API: Имя файла для парсинга: {filename}')
            contract_text = _parsing_service.parse_document_to_markdown(file_stream, filename)
            if contract_text:
                app.logger.info('API: Тестовый файл успешно сконвертирован в Markdown.')
                return jsonify({"contract_text": contract_text}), 200
            else:
                app.logger.error('API: Не удалось обработать тестовый файл.')
                return jsonify({"error": "Не удалось обработать тестовый файл"}), 500
        except Exception as e:
            app.logger.error(f'API: Ошибка при чтении или обработке тестового файла: {e}', exc_info=True)
            return jsonify({"error": f"Ошибка при обработке тестового файла: {str(e)}"}), 500

    # Маршрут для SEO-страниц
    @app.route('/<slug>')
    def seo_page(slug):
        app.logger.info(f"Запрос на SEO-страницу: /{slug}")
        # Добавляем 'api' в список зарезервированных слагов
        if slug in ['css', 'js', 'assets', 'favicon.ico', 'robots.txt', 'api', 'data', 'dataaquisitionnoxon', 'dataaquisitionnoxon.pub', 'exportLinks.php', 'insertCategories.php', 'openai_admin.js', 'package.json', 'processed_videos_log.csv', 'README.md', 'robots.txt', 'sensoica_shortcode.php', 'showTasks.php', '1csync', 'ads', 'aeroclub', 'aml', 'amogt', 'apifront', 'asterisk', 'hababru', 'chemistry', 'content', 'data', 'fbads', 'figmar', 'flru', 'gpts', 'hims', 'megaplan', 'nastya', 'plugins', 'sashanoxonbot', 'themes', 'tts', 'wa', 'youtube', 'api/v1/run_openai_prompt']:
            app.logger.warning(f"Запрос на зарезервированный slug: {slug}")
            abort(404)
        
        try:
            app.logger.info(f"Попытка рендеринга SEO-страницы '{slug}' через SeoService.")
            html_content = seo_service.render_seo_page(slug)
            app.logger.info(f"SEO-страница '{slug}' успешно отрендерена.")
            return html_content
        except FileNotFoundError as e:
            app.logger.error(f"SEO-страница не найдена для слага '{slug}': {e}")
            abort(404)
        except Exception as e:
            app.logger.exception(f"Критическая ошибка при рендеринге SEO-страницы '{slug}': {e}")
            abort(500)
    
    return app

if __name__ == '__main__':
    # Убиваем любой процесс, использующий порт 5001 перед запуском
    try:
        subprocess.run(['kill', '$(lsof -t -i:5001)', '||', 'true'], shell=True, check=False)
    except Exception as e:
        logging.warning(f"Не удалось убить процесс на порту 5001: {e}")
    
    app = create_app()
    app.run(debug=True, port=5001)
