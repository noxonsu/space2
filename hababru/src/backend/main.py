import os
from flask import Flask, render_template, send_from_directory, abort, jsonify, request, redirect
from dotenv import load_dotenv
import subprocess
import io
import threading
import time

# Импорты сервисов
from src.backend.api.v1.contract_analyzer import contract_analyzer_bp
from src.backend.api.v1.seo_tools import create_seo_tools_blueprint
from src.backend.services.llm_service import LLMService
from src.backend.services.seo_service import SeoService
from src.backend.services.seo_prompt_service import SeoPromptService
from src.backend.services.parsing_service import ParsingService
from src.backend.services.cache_service import CacheService
from src.backend.services.llms_txt_service import LlmsTxtService
from src.backend.services.telegram_connector import TelegramConnector
from src.backend.services.telegram_product_generator import TelegramProductGenerator

# Загрузка переменных окружения из .env файла
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Настройка логирования для отладки
import logging


class TelegramMonitoringThread:
    """Класс для управления мониторингом Telegram в отдельном потоке"""
    
    def __init__(self, telegram_connector, telegram_generator, check_interval=300):
        self.telegram_connector = telegram_connector
        self.telegram_generator = telegram_generator
        self.check_interval = check_interval  # 5 минут по умолчанию
        self.monitoring_thread = None
        self.stop_monitoring = False
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self):
        """Запуск мониторинга в отдельном потоке"""
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.stop_monitoring = False
            self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitoring_thread.start()
            self.logger.info("Telegram мониторинг запущен")
    
    def stop_monitoring_process(self):
        """Остановка мониторинга"""
        self.stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Telegram мониторинг остановлен")
    
    def _monitor_loop(self):
        """Основной цикл мониторинга"""
        while not self.stop_monitoring:
            try:
                # Получаем новые сообщения
                messages = self.telegram_connector.get_latest_messages(limit=10)
                
                for message in messages:
                    try:
                        # Генерируем продукт из сообщения
                        product_yaml = self.telegram_generator.generate_product_from_message(message)
                        
                        if product_yaml:
                            # Сохраняем в файл
                            filename = self._save_product_yaml(product_yaml, message.get('id'))
                            self.logger.info(f"Создан новый продукт из Telegram: {filename}")
                    
                    except Exception as e:
                        self.logger.error(f"Ошибка обработки сообщения {message.get('id')}: {str(e)}")
                
            except Exception as e:
                self.logger.error(f"Ошибка в цикле мониторинга Telegram: {str(e)}")
            
            # Ждем до следующей проверки
            time.sleep(self.check_interval)
    
    def _save_product_yaml(self, product_yaml, message_id):
        """Сохранение YAML файла продукта"""
        import yaml
        import datetime
        
        products_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'content', 'products')
        
        # Генерируем уникальное имя файла
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"telegram_product_{timestamp}_{message_id}.yaml"
        filepath = os.path.join(products_dir, filename)
        
        # Сохраняем файл
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(product_yaml, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return filename


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

    # Инициализация системы продуктов ПОСЛЕ инициализации сервисов
    from .services.products import product_registry
    from .services.products.contract_analysis import ContractAnalysisProduct
    from .services.products.news_analysis import NewsAnalysisProduct
    
    # Регистрация продуктов
    contract_product = ContractAnalysisProduct(llm_service, parsing_service, cache_service)
    news_product = NewsAnalysisProduct(llm_service)
    
    product_registry.register_product(contract_product)
    product_registry.register_product(news_product)
    
    app.logger.info(f"Зарегистрированы продукты: {list(product_registry.get_all_products().keys())}")

    # Инициализация Telegram мониторинга (опционально)
    telegram_monitor = None
    if os.getenv('TELEGRAM_API_ID') and os.getenv('TELEGRAM_API_HASH') and os.getenv('ENABLE_TELEGRAM_MONITORING', 'false').lower() == 'true':
        try:
            telegram_connector = TelegramConnector(
                api_id=int(os.getenv('TELEGRAM_API_ID')),
                api_hash=os.getenv('TELEGRAM_API_HASH'),
                phone_number=os.getenv('TELEGRAM_PHONE_NUMBER'),
                channel_username='@aideaxondemos'
            )
            telegram_generator = TelegramProductGenerator(llm_service=llm_service)
            telegram_monitor = TelegramMonitoringThread(
                telegram_connector=telegram_connector,
                telegram_generator=telegram_generator,
                check_interval=int(os.getenv('TELEGRAM_CHECK_INTERVAL', '300'))  # 5 минут по умолчанию
            )
            
            # Запускаем мониторинг
            telegram_monitor.start_monitoring()
            app.logger.info("Telegram мониторинг инициализирован и запущен")
            
        except Exception as e:
            app.logger.warning(f"Не удалось запустить Telegram мониторинг: {str(e)}")
            telegram_monitor = None
    else:
        app.logger.info("Telegram мониторинг отключен (не настроены переменные окружения)")

    # Сохраняем мониторинг в конфигурации для возможности управления
    app.config['TELEGRAM_MONITOR'] = telegram_monitor

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

    # Устаревший роут для совместимости  
    @app.route('/seo_admin')
    def seo_admin():
        app.logger.info("Редирект со старой админки на новую.")
        from flask import redirect
        return redirect('/admin')

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

    @app.route('/llms.txt')
    def serve_llms_txt():
        """Обслуживание llms.txt файла согласно спецификации llmstxt.org"""
        try:
            # Определяем базовый URL для генерации ссылок
            base_url = request.url_root.rstrip('/')
            
            # Создаем сервис и генерируем содержимое
            llms_service = LlmsTxtService(base_url=base_url)
            content = llms_service.generate_llms_txt()
            
            # Возвращаем как plain text
            from flask import Response
            return Response(content, mimetype='text/plain; charset=utf-8')
            
        except Exception as e:
            app.logger.error(f"Ошибка генерации llms.txt: {str(e)}")
            # Возвращаем базовую версию в случае ошибки
            fallback_content = """# HababRu - B2B Платформа для Кастомных Решений

> B2B-сервис, специализирующийся на разработке кастомных решений для бизнеса с демонстрационными AI-сервисами.

## Документация

- [Главная страница]({base_url}): Основная информация о платформе

## Продукты

- [Анализ договоров]({base_url}/demo/contract_analysis): Демонстрация анализа юридических документов
- [Мониторинг новостей]({base_url}/demo/news_analysis): Пример анализа отраслевых новостей
""".format(base_url=request.url_root.rstrip('/'))
            
            from flask import Response
            return Response(fallback_content, mimetype='text/plain; charset=utf-8')

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

    # Админка - основная страница
    @app.route('/admin')
    def admin_dashboard():
        app.logger.info("Запрос к главной странице админки.")
        return render_template('admin/dashboard.html')

    # Админка - список SEO-страниц
    @app.route('/admin/seo-pages')
    def admin_seo_pages():
        app.logger.info("Запрос к списку SEO-страниц.")
        return render_template('admin/seo_pages.html')

    # Админка - создание страницы
    @app.route('/admin/create-page')
    def admin_create_page():
        app.logger.info("Запрос к странице создания SEO-страницы.")
        return render_template('admin/create_page.html')

    # Админка - редактирование страницы
    @app.route('/admin/edit-page/<slug>')
    def admin_edit_page(slug):
        app.logger.info(f"Запрос к редактированию SEO-страницы: {slug}")
        try:
            # Загружаем данные страницы
            page_data = seo_service.get_page_data(slug)
            return render_template('admin/edit_page.html', page_data=page_data, slug=slug)
        except FileNotFoundError:
            app.logger.error(f"SEO-страница не найдена: {slug}")
            abort(404)

    # Админка - массовая генерация
    @app.route('/admin/bulk-generate')
    def admin_bulk_generate():
        app.logger.info("Запрос к странице массовой генерации.")
        return render_template('admin/bulk_generate.html')

    # Админка - генерация кластера
    @app.route('/admin/generate-cluster')
    def admin_generate_cluster():
        app.logger.info("Запрос к странице генерации кластера.")
        return render_template('admin/generate_cluster.html')

    # Админка - промпты для страницы
    @app.route('/admin/prompts/<slug>')
    def admin_page_prompts(slug):
        app.logger.info(f"Запрос к промптам для страницы: {slug}")
        try:
            page_data = seo_service.get_page_data(slug)
            return render_template('admin/page_prompts.html', page_data=page_data, slug=slug)
        except FileNotFoundError:
            app.logger.error(f"SEO-страница не найдена: {slug}")
            abort(404)

    # Админка - аналитика
    @app.route('/admin/analytics')
    def admin_analytics():
        app.logger.info("Запрос к странице аналитики.")
        return render_template('admin/analytics.html')

    # Админка - управление продуктами
    @app.route('/admin/products')
    def admin_products():
        app.logger.info("Запрос к странице управления продуктами.")
        return render_template('admin/products.html')

    # Админка - детальная страница продукта
    @app.route('/admin/products/<product_id>')
    def admin_product_detail(product_id):
        app.logger.info(f"Запрос к детальной странице продукта: {product_id}")
        # Здесь будет логика отображения детальной информации о продукте
        from .services.products import product_registry
        product = product_registry.get_product(product_id)
        if not product:
            abort(404)
        
        product_info = product.get_product_info()
        seo_pages = product_registry.get_seo_pages_for_product(product_id)
        
        return render_template('admin/product_detail.html', 
                             product=product,
                             product_info=product_info, 
                             seo_pages=seo_pages,
                             product_id=product_id,
                             stats={'total_pages': len(seo_pages), 'total_keywords': 0, 'avg_keywords': 0},
                             screenshots=product.get_screenshots())

    # Обработчик завершения приложения для корректной остановки мониторинга
    @app.teardown_appcontext
    def shutdown_telegram_monitor(error):
        telegram_monitor = app.config.get('TELEGRAM_MONITOR')
        if telegram_monitor:
            telegram_monitor.stop_monitoring_process()

    return app

if __name__ == '__main__':
    # Убиваем любой процесс, использующий порт 5001 перед запуском
    try:
        subprocess.run(['kill', '$(lsof -t -i:5001)', '||', 'true'], shell=True, check=False)
    except Exception as e:
        logging.warning(f"Не удалось убить процесс на порту 5001: {e}")
    
    app = create_app()
    app.run(debug=True, port=5001)
