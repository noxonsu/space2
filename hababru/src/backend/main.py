import os
import sys
from flask import Flask, render_template, send_from_directory, abort, jsonify, request, redirect
from dotenv import load_dotenv
import subprocess
import io
import threading
import time

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Импорты сервисов
from hababru.src.backend.api.v1.contract_analyzer import contract_analyzer_bp
from hababru.src.backend.api.v1.site_presentations import site_presentations_bp
from hababru.src.backend.api.v1.amoexcel_googledrive_sync import amoexcel_googledrive_sync_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.bitcoin_mempool_explorer import bitcoin_mempool_explorer_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.crm_automation import crm_automation_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.hr_dialogue_mimic import hr_dialogue_mimic_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.telephony_dashboard import telephony_dashboard_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.test_ai_tool import test_ai_tool_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.youtube_telegram_scraper import youtube_telegram_scraper_bp # Импортируем новый Blueprint
from hababru.src.backend.api.v1.seo_tools import create_seo_tools_blueprint
from hababru.src.backend.api.v1.browser_log import browser_log_bp # Импортируем новый Blueprint
from hababru.src.backend.services.llm_service import LLMService
from hababru.src.backend.services.seo_service import SeoService
from hababru.src.backend.services.seo_prompt_service import SeoPromptService
from hababru.src.backend.services.parsing_service import ParsingService
from hababru.src.backend.services.cache_service import CacheService
from hababru.src.backend.services.llms_txt_service import LlmsTxtService
from hababru.src.backend.services.telegram_connector import TelegramConnector
from hababru.src.backend.services.telegram_product_generator import TelegramProductGenerator

# Загрузка переменных окружения из .env файла
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Настройка логирования для отладки
import logging


class TelegramMonitoringThread:
    """Класс для управления мониторингом Telegram в отдельном потоке"""
    
    def __init__(self, telegram_connector, check_interval=300): # Удаляем telegram_generator из аргументов
        self.telegram_connector = telegram_connector
        self.check_interval = check_interval
        self.monitoring_thread = None
        self.stop_monitoring = False
        self.logger = logging.getLogger(__name__)
        # telegram_generator будет инициализирован внутри _monitor_loop, чтобы иметь доступ к current_app
        self.telegram_generator = None 
    
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
        # Инициализируем telegram_generator здесь, чтобы иметь доступ к current_app
        if self.telegram_generator is None:
            try:
                llm_service_instance = current_app.config.get('LLM_SERVICE')
                if not llm_service_instance:
                    self.logger.error("LLMService не инициализирован в app.config для TelegramMonitoringThread.")
                    return # Не можем продолжить без LLMService
                self.telegram_generator = TelegramProductGenerator(llm_service=llm_service_instance)
            except Exception as e:
                self.logger.error(f"Ошибка инициализации TelegramProductGenerator в мониторинге: {e}")
                return # Не можем продолжить без генератора

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
    from hababru.src.backend.services.products import product_registry
    from hababru.src.backend.services.product_factory import ProductFactory
    
    # Создаем фабрику продуктов
    product_factory = ProductFactory()
    
    # Регистрируем доступные зависимости
    product_factory.register_dependency("llm_service", llm_service)
    product_factory.register_dependency("parsing_service", parsing_service)
    product_factory.register_dependency("cache_service", cache_service)
    
    # Создаем и регистрируем все активные продукты
    try:
        created_products = product_factory.create_all_active_products()
        
        for product_id, product_instance in created_products.items():
            product_registry.register_product(product_instance)
            app.logger.info(f"Зарегистрирован продукт: {product_id}")
            
        app.logger.info(f"Всего зарегистрировано продуктов: {list(product_registry.get_all_products().keys())}")
        
        # Регистрируем связи между продуктами и SEO-страницами
        try:
            # Связываем продукт анализа новостей с его SEO-страницами
            product_registry.map_seo_page_to_product('monitoring-novostey', 'news_analysis')
            product_registry.map_seo_page_to_product('monitoring-ved-novostey', 'news_analysis')
            product_registry.map_seo_page_to_product('monitoring-finansovyh-novostey', 'news_analysis')
            product_registry.map_seo_page_to_product('monitoring-it-novostey', 'news_analysis')
            product_registry.map_seo_page_to_product('monitoring-pravovyh-izmeneniy', 'news_analysis')
            product_registry.map_seo_page_to_product('monitoring-logisticheskih-novostey', 'news_analysis')
            app.logger.info("Зарегистрированы связи между продуктами и SEO-страницами")
        except Exception as e:
            app.logger.warning(f"Ошибка при регистрации связей продуктов с SEO-страницами: {e}")
        
    except Exception as e:
        app.logger.error(f"Ошибка при инициализации системы продуктов: {e}")

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
    app.config['PRODUCT_FACTORY'] = product_factory # Добавляем PRODUCT_FACTORY в app.config

    # Регистрация Blueprint для API
    app.register_blueprint(contract_analyzer_bp, url_prefix='/api/v1')
    app.register_blueprint(site_presentations_bp, url_prefix='/api/v1')
    app.register_blueprint(amoexcel_googledrive_sync_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(bitcoin_mempool_explorer_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(crm_automation_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(hr_dialogue_mimic_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(telephony_dashboard_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(test_ai_tool_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(youtube_telegram_scraper_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint
    app.register_blueprint(create_seo_tools_blueprint(seo_service, seo_prompt_service), url_prefix='/admin')
    app.register_blueprint(browser_log_bp, url_prefix='/api/v1') # Регистрируем новый Blueprint

    @app.after_request
    def add_csp_header(response):
        response.headers['Content-Security-Policy'] = "default-src 'self' https://mc.yandex.com; script-src 'self' 'unsafe-inline' https://mc.yandex.ru https://mc.yandex.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://mc.yandex.com; font-src 'self'; connect-src 'self' https://mc.yandex.com;"
        return response

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

    @app.route('/sites/<site_id>/')
    def serve_generated_site(site_id):
        """Обслуживание созданных презентационных сайтов"""
        sites_dir = os.path.join(app.root_path, 'public', 'sites', site_id)
        index_file = os.path.join(sites_dir, 'index.html')
        
        if not os.path.exists(index_file):
            abort(404)
        
        return send_from_directory(sites_dir, 'index.html')

    @app.route('/sites/<site_id>/<path:filename>')
    def serve_site_assets(site_id, filename):
        """Обслуживание ресурсов сайтов (CSS, JS, изображения)"""
        sites_dir = os.path.join(app.root_path, 'public', 'sites', site_id)
        return send_from_directory(sites_dir, filename)

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

- [Анализ договоров]({base_url}/contract_analysis): Демонстрация анализа юридических документов
- [Мониторинг новостей]({base_url}/news_analysis): Пример анализа отраслевых новостей
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

    # Маршрут для детальной страницы продукта
    @app.route('/products/<product_id>')
    def product_page(product_id):
        app.logger.info(f"Запрос на страницу продукта: /products/{product_id}")
        from hababru.src.backend.services.products import product_registry
        from hababru.src.backend.services.product_data_loader import ProductDataLoader
        
        product_instance = product_registry.get_product(product_id)
        
        if not product_instance:
            app.logger.error(f"Продукт не найден для ID: {product_id}")
            abort(404)
            
        # Загружаем данные продукта для передачи в шаблон
        try:
            loader = ProductDataLoader()
            product_data = loader.load_product_data(product_id)
            app.logger.info(f"Загружены данные продукта: {product_id}")
            
            # Пытаемся загрузить SEO-страницу для контента, но с данными продукта
            try:
                html_content = seo_service.render_seo_page(product_id, product_data=product_data)
                app.logger.info(f"Страница продукта '{product_id}' успешно отрендерена через SeoService с данными продукта.")
                return html_content
            except FileNotFoundError:
                # Если SEO-страница не найдена, рендерим базовую страницу продукта
                app.logger.info(f"SEO-страница не найдена для продукта '{product_id}', рендерим базовую страницу")
                
                # Подготавливаем данные для шаблона
                template_data = {
                    'product_data': product_data,
                    'page_title': product_data.get('name', 'Продукт'),
                    'page_content': f"<h1>{product_data.get('name', 'Продукт')}</h1><p>{product_data.get('description', '')}</p>",
                    'is_seo_page': False,
                    'product_info': product_data
                }
                
                return render_template('index_template.html', **template_data)
                
        except Exception as e:
            app.logger.exception(f"Ошибка при загрузке данных продукта '{product_id}': {e}")
            abort(500)

    # Маршрут для SEO-страниц
    @app.route('/<slug>')
    def seo_page(slug):
        app.logger.info(f"Запрос на SEO-страницу: /{slug}")
        # Список зарезервированных слагов, которые не должны быть SEO-страницами
        # Удален 'products' из этого списка, так как теперь у него есть свой маршрут
        reserved_slugs = [
            'css', 'js', 'assets', 'favicon.ico', 'robots.txt', 'api', 'data', 
            'dataaquisitionnoxon', 'dataaquisitionnoxon.pub', 'exportLinks.php', 
            'insertCategories.php', 'openai_admin.js', 'package.json', 
            'processed_videos_log.csv', 'README.md', 'robots.txt', 
            'sensoica_shortcode.php', 'showTasks.php', '1csync', 'ads', 
            'aeroclub', 'aml', 'amogt', 'apifront', 'asterisk', 'hababru', 
            'chemistry', 'content', 'data', 'fbads', 'figmar', 'flru', 'gpts', 
            'hims', 'megaplan', 'nastya', 'plugins', 'sashanoxonbot', 'themes', 
            'tts', 'wa', 'youtube', 'api/v1/run_openai_prompt', 'admin', 
            'analyze', 'get_test_contract', 'get_page_prompt_results', 
            'get_llm_models', 'generate-test-products', 'sites'
        ]
        
        if slug in reserved_slugs:
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

    # Админка - генерация продуктов
    @app.route('/admin/generate-products')
    def admin_generate_products():
        app.logger.info("Запрос к странице генерации продуктов.")
        return render_template('admin/generate_products.html')

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

    # API для генерации тестовых продуктов
    @app.route('/api/generate-test-products', methods=['POST'])
    def generate_test_products():
        """Генерация тестовых продуктов для демонстрации функциональности"""
        try:
            app.logger.info("Начинаем генерацию тестовых продуктов")
            
            # Получаем llm_service из app.config
            llm_service_instance = app.config.get('LLM_SERVICE')
            if not llm_service_instance:
                raise RuntimeError("LLMService не инициализирован для генерации тестовых продуктов.")

            # Создаем генератор продуктов
            product_generator = TelegramProductGenerator(llm_service=llm_service_instance)
            
            # Тестовые данные для генерации продуктов
            test_products_data = [
                {
                    "name": "CRM Автоматизация",
                    "description": "Умный помощник для автоматизации CRM-процессов с искусственным интеллектом",
                    "category": "automation",
                    "text": "Революционная CRM-автоматизация с ИИ для малого и среднего бизнеса. Автоматически обрабатывает клиентские запросы, ведет базу данных, создает отчеты и предлагает следующие шаги для увеличения продаж."
                },
                {
                    "name": "Анализ финансовых отчетов",
                    "description": "Автоматический анализ финансовых документов и отчетов с помощью ИИ",
                    "category": "finance", 
                    "text": "Мощный инструмент для анализа финансовых отчетов. Обрабатывает балансы, P&L, cash flow отчеты. Выявляет риски, тренды и дает рекомендации по улучшению финансового состояния компании."
                },
                {
                    "name": "Маркетинговый ИИ-помощник",
                    "description": "Генерация контента и анализ маркетинговых кампаний с помощью ИИ",
                    "category": "marketing",
                    "text": "Комплексное решение для маркетинга: генерация текстов для социальных сетей, анализ конкурентов, создание рекламных кампаний, A/B тестирование и оптимизация конверсий."
                }
            ]
            
            results = {
                "success": True,
                "generated_products": [],
                "errors": []
            }
            
            # Генерируем продукты
            for product_data in test_products_data:
                try:
                    # Создаем фейковое сообщение для тестирования
                    from hababru.src.backend.services.telegram_connector import TelegramMessage
                    from datetime import datetime
                    
                    test_message = TelegramMessage(
                        message_id=f"test_{product_data['name'].lower().replace(' ', '_')}",
                        date=datetime.now(),
                        text=product_data['text'],
                        media_files=[]
                    )
                    
                    # Генерируем продукт
                    result = product_generator.generate_product_from_message(test_message)
                    
                    if result["success"]:
                        results["generated_products"].append({
                            "product_id": result["product_id"],
                            "product_name": result["product_name"],
                            "file_path": result["file_path"]
                        })
                        app.logger.info(f"Успешно создан продукт: {result['product_id']}")
                    else:
                        results["errors"].append({
                            "product_name": product_data["name"],
                            "error": result["error"]
                        })
                        app.logger.error(f"Ошибка создания продукта {product_data['name']}: {result['error']}")
                        
                except Exception as e:
                    results["errors"].append({
                        "product_name": product_data["name"],
                        "error": str(e)
                    })
                    app.logger.error(f"Исключение при создании продукта {product_data['name']}: {e}")
            
            # Обновляем llms.txt после генерации
            try:
                base_url = request.url_root.rstrip('/')
                llms_service = LlmsTxtService(base_url=base_url)
                llms_content = llms_service.generate_llms_txt()
                app.logger.info("llms.txt успешно обновлен")
            except Exception as e:
                app.logger.error(f"Ошибка обновления llms.txt: {e}")
            
            return jsonify(results)
            
        except Exception as e:
            app.logger.error(f"Общая ошибка генерации продуктов: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    # API для получения списка продуктов
    @app.route('/api/products/list')
    def get_products_list():
        """Получение списка всех продуктов"""
        try:
            # Используем глобальный реестр продуктов
            from hababru.src.backend.services.products import product_registry
            
            products = product_registry.get_all_products()
            
            products_list = []
            for product_id, product_instance in products.items():
                # Получаем информацию о продукте через его метод get_product_info
                product_info = product_instance.get_product_info()
                products_list.append({
                    "product_id": product_id,
                    "name": product_info.get("name", "Без названия"),
                    "description": product_info.get("description", "Без описания"),
                    "category": product_info.get("category", "other"),
                    "status": product_info.get("status", "active")
                })
            
            return jsonify({
                "success": True,
                "products": products_list,
                "total": len(products_list)
            })
            
        except Exception as e:
            app.logger.error(f"Ошибка получения списка продуктов: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    # API для получения результатов промптов страницы
    @app.route('/api/v1/get_page_prompt_results')
    def get_page_prompt_results():
        """Получение результатов промптов для конкретной страницы"""
        slug = request.args.get('slug')
        if not slug:
            return jsonify({"error": "Slug is required"}), 400
        
        try:
            cache_service = app.config.get('CACHE_SERVICE')
            results = cache_service.get_all_prompt_results_for_page(slug)
            return jsonify({
                "status": "ok",
                "results": results
            })
        except Exception as e:
            app.logger.error(f"Ошибка получения результатов промптов для страницы {slug}: {e}")
            return jsonify({"error": str(e)}), 500

    # API для получения доступных LLM моделей
    @app.route('/api/v1/get_llm_models')
    def get_llm_models():
        """Получение списка доступных LLM моделей"""
        try:
            llm_service = app.config.get('LLM_SERVICE')
            models = llm_service.get_available_models()
            return jsonify({
                "status": "ok",
                "models": models
            })
        except Exception as e:
            app.logger.error(f"Ошибка получения списка LLM моделей: {e}")
            return jsonify({"error": str(e)}), 500

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
    app.run(debug=False, host='0.0.0.0', port=5001, use_reloader=False)
