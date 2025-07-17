import pytest
import os
import sys
import time
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import shutil
import markdown
import yaml
from io import BytesIO # Импортируем BytesIO

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from hababru.src.backend.main import create_app
from hababru.src.backend.services.llm_service import LLMService # Импортируем для spec
from hababru.src.backend.services.parsing_service import ParsingService # Импортируем для spec
from hababru.src.backend.services.cache_service import CacheService # Импортируем для spec
from hababru.src.backend.services.seo_service import SeoService # Импортируем для spec
from hababru.src.backend.services.seo_prompt_service import SeoPromptService # Импортируем для spec
from bs4 import BeautifulSoup # Импортируем BeautifulSoup
import json # Импортируем json

# Список для отслеживания пройденных тестов
passed_tests = []
passed_tests_times = []

@pytest.fixture(autouse=True)
def test_tracker(request):
    test_name = request.node.name
    print(f"\n🔄 НАЧИНАЮ ТЕСТ: {test_name}")
    
    start_time = time.time()
    
    try:
        yield
        end_time = time.time()
        execution_time = end_time - start_time
        
        if hasattr(request.node, 'rep_call') and request.node.rep_call.passed:
            passed_tests.append(test_name)
            passed_tests_times.append(execution_time)
            print(f"✅ ТЕСТ ПРОШЕЛ: {test_name} (время: {execution_time:.2f}с)")
        elif hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            print(f"❌ ТЕСТ ПРОВАЛЕН: {test_name} (время: {execution_time:.2f}с)")
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"💥 ОШИБКА В ТЕСТЕ: {test_name} (время: {execution_time:.2f}с) - {str(e)}")
        raise

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture
def mock_services():
    mock_llm_service = MagicMock(spec=LLMService)
    mock_parsing_service = MagicMock(spec=ParsingService)
    mock_cache_service = MagicMock(spec=CacheService)
    mock_seo_service = MagicMock(spec=SeoService)
    mock_seo_prompt_service = MagicMock(spec=SeoPromptService)

    mock_llm_service.generate_text.return_value = "Mocked LLM response for testing."
    mock_parsing_service.parse_document_to_markdown.return_value = "Parsed PDF content"
    mock_cache_service._generate_hash.return_value = "mocked_hash_123"

    temp_cache_dir = tempfile.mkdtemp()
    mock_cache_service.get_file_cache_dir.return_value = temp_cache_dir

    yield mock_llm_service, mock_parsing_service, mock_cache_service, mock_seo_service, mock_seo_prompt_service
    
    shutil.rmtree(temp_cache_dir)

@pytest.fixture
def client(mock_services):
    mock_llm_service, mock_parsing_service, mock_cache_service, mock_seo_service, mock_seo_prompt_service = mock_services
    
    test_app = create_app(
        llm_service_mock=mock_llm_service,
        parsing_service_mock=mock_parsing_service,
        cache_service_mock=mock_cache_service,
        seo_service_mock=mock_seo_service,
        seo_prompt_service_mock=mock_seo_prompt_service
    )
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def real_client():
    """Фикстура для создания клиента Flask без мокирования LLMService."""
    test_app = create_app() # Создаем приложение без моков для LLMService
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data 

def test_seo_page(client, mock_services):
    mock_llm_service, mock_parsing_service, mock_cache_service, mock_seo_service, mock_seo_prompt_service = mock_services
    
    mock_seo_service.render_seo_page.return_value = "<html><body>Test SEO Page Content</body></html>"
    rv = client.get('/arendy')
    assert rv.status_code == 200
    assert b"Test SEO Page Content" in rv.data
    mock_seo_service.render_seo_page.assert_called_once_with('arendy')

def test_get_sample_contract(client, mock_services):
    mock_llm_service, mock_parsing_instance, mock_cache_instance, mock_seo_service_instance, mock_seo_prompt_service_instance = mock_services
    
    mock_parsing_instance.parse_document_to_markdown.return_value = "Mocked contract text from sample file."

    with patch('os.path.exists', return_value=True), \
         patch('os.path.isfile', return_value=True), \
         patch('builtins.open', mock_open(read_data=b"dummy file content")) as mock_file_open:
        
        rv = client.get('/get_test_contract')
        assert rv.status_code == 200
        assert "contract_text" in rv.json
        assert rv.json["contract_text"] == "Mocked contract text from sample file."
        mock_parsing_instance.parse_document_to_markdown.assert_called_once()
        mock_file_open.assert_called_once()

def test_upload_contract(client, mock_services):
    """Тест для проверки загрузки файла и его обработки."""
    mock_llm_service, mock_parsing_service, mock_cache_service, _, _ = mock_services

    # Создаем временную директорию для кэша
    with tempfile.TemporaryDirectory() as tmpdir:
        mock_cache_service.get_file_cache_dir.return_value = tmpdir

        # Мокируем возвращаемое значение для parse_document_to_markdown
        mock_parsing_service.parse_document_to_markdown.return_value = "Mocked Contract Text"

        # Мокируем возвращаемое значение для _generate_hash
        mock_cache_service._generate_hash.return_value = "mocked_file_hash"

        # Мокируем возвращаемое значение для create_analysis_task
        mock_cache_service.create_analysis_task.return_value = "mocked_task_id"

        # Создаем фиктивный файл для загрузки
        data = {'file': (BytesIO(b"dummy contract content"), 'test_contract.pdf', 'application/pdf')}

        # Отправляем POST запрос
        with patch('threading.Thread') as mock_thread:
            rv = client.post('/api/v1/upload_contract', data=data, content_type='multipart/form-data')

            # Проверяем, что поток был создан и запущен
            mock_thread.assert_called_once()
            # Получаем аргументы, с которыми был вызван поток
            args, kwargs = mock_thread.call_args
            # Проверяем, что target функция - это _run_analysis_task
            assert kwargs['target'].__name__ == '_run_analysis_task'
            # Проверяем, что аргументы переданы корректно
            assert len(kwargs['args']) == 4
            assert kwargs['args'][0] == rv.json['task_id']
            assert kwargs['args'][1] == rv.json['contract_id']
            assert kwargs['args'][2] == "Mocked Contract Text"

        # Проверяем статус код и ответ
        assert rv.status_code == 200
        assert rv.json['message'] == "Файл успешно загружен и обработан"
        assert rv.json['contract_id'] == 'mocked_file_hash'
        assert rv.json['task_id'] is not None

        # Проверяем, что parse_document_to_markdown был вызван
        mock_parsing_service.parse_document_to_markdown.assert_called_once()

        # Проверяем, что _generate_hash был вызван
        mock_cache_service._generate_hash.assert_called_once()

        # Проверяем, что create_analysis_task был вызван
        mock_cache_service.create_analysis_task.assert_called_once()

def test_seo_page_content_display(client, mock_services):
    mock_llm_service, mock_parsing_instance, mock_cache_instance, mock_seo_service_instance, mock_seo_prompt_service_instance = mock_services

    seo_page_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'seo_pages', 'arendy')
    source_md_path = os.path.join(seo_page_dir, 'source.md')
    generated_contract_path = os.path.join(seo_page_dir, 'generated_contract.txt')

    with open(source_md_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    parts = source_content.split('---', 2)
    front_matter = yaml.safe_load(parts[1])
    page_text_content_md = parts[2].strip()
    expected_page_text_html = markdown.markdown(page_text_content_md)

    with open(generated_contract_path, 'r', encoding='utf-8') as f:
        expected_contract_text = f.read()

    mock_app_config_data = {
        "isSeoPage": True,
        "mainKeyword": front_matter['main_keyword'],
        "seoPageContractTextRaw": expected_contract_text,
        "analysisResultsRaw": {"mocked_analysis_data": "some_value"}
    }
    mock_html_response = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{front_matter['title']}</title>
        <meta name="keywords" content="{', '.join(front_matter['meta_keywords'])}">
        <meta name="description" content="{front_matter['meta_description']}">
        <link rel="stylesheet" href="/css/style.css">
    </head>
    <body>
        <div id="app-root">
            <h1>{front_matter['title']}</h1>
            <div>{expected_page_text_html}</div>
        </div>
        <div id="app-config-data" style="display:none;">{json.dumps(mock_app_config_data)}</div>
        <script src="/js/app.js"></script>
    </body>
    </html>
    """
    mock_seo_service_instance.render_seo_page.return_value = mock_html_response

    rv = client.get('/arendy')
    assert rv.status_code == 200
    assert front_matter['title'].encode('utf-8') in rv.data
    assert expected_page_text_html.encode('utf-8') in rv.data

    # Проверяем, что данные appConfig корректно переданы и содержат текст договора
    soup = BeautifulSoup(rv.data, 'html.parser')
    app_config_div = soup.find('div', id='app-config-data')
    assert app_config_div is not None, "Не удалось найти div с id='app-config-data'"
    app_config_json_string = app_config_div.text.strip()
    assert app_config_json_string, "div с id='app-config-data' пуст"
    app_config = json.loads(app_config_json_string)
    assert app_config['seoPageContractTextRaw'] == expected_contract_text
    assert 'analysisResultsRaw' in app_config # Проверяем наличие данных анализа
    assert app_config['analysisResultsRaw'] == {"mocked_analysis_data": "some_value"} # Проверяем моковые данные анализа


def test_seo_page_ipotechnyh_dogovorov_content_display(client, mock_services):
    mock_llm_service, mock_parsing_instance, mock_cache_instance, mock_seo_service_instance, mock_seo_prompt_service_instance = mock_services

    seo_page_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'seo_pages', 'ipotechnyh-dogovorov')
    source_md_path = os.path.join(seo_page_dir, 'source.md')
    generated_contract_path = os.path.join(seo_page_dir, 'generated_contract.txt')

    with open(source_md_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    parts = source_content.split('---', 2)
    front_matter = yaml.safe_load(parts[1])
    page_text_content_md = parts[2].strip()
    expected_page_text_html = markdown.markdown(page_text_content_md)

    with open(generated_contract_path, 'r', encoding='utf-8') as f:
        expected_contract_text = f.read()

    mock_analysis_results = {
        "summary": "Это анализ договора, выполненный 'на лету'.",
        "paragraphs": [
            {"original_paragraph": "Пункт 1 договора.", "analysis": "Анализ пункта 1."},
            {"original_paragraph": "Пункт 2 договора.", "analysis": "Анализ пункта 2."}
        ]
    }

    mock_app_config_data = {
        "isSeoPage": True,
        "mainKeyword": front_matter['main_keyword'],
        "seoPageContractTextRaw": expected_contract_text,
        "analysisResultsRaw": mock_analysis_results # Используем мок с 2 пунктами
    }
    mock_html_response = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{front_matter['title']}</title>
        <meta name="keywords" content="{', '.join(front_matter['meta_keywords'])}">
        <meta name="description" content="{front_matter['meta_description']}">
        <link rel="stylesheet" href="/css/style.css">
    </head>
    <body>
        <div id="app-root">
            <h1>{front_matter['title']}</h1>
            <div>{expected_page_text_html}</div>
        </div>
        <div id="app-config-data" style="display:none;">{json.dumps(mock_app_config_data)}</div>
        <script src="/js/app.js"></script>
    </body>
    </html>
    """
    mock_seo_service_instance.render_seo_page.return_value = mock_html_response

    rv = client.get('/ipotechnyh-dogovorov')
    assert rv.status_code == 200
    assert front_matter['title'].encode('utf-8') in rv.data
    assert expected_page_text_html.encode('utf-8') in rv.data

    soup = BeautifulSoup(rv.data, 'html.parser')
    app_config_div = soup.find('div', id='app-config-data')
    assert app_config_div is not None, "Could not find app-config-data div"
    app_config_json_string = app_config_div.text.strip()
    assert app_config_json_string, "app-config-data div is empty"
    app_config = json.loads(app_config_json_string)
    assert app_config['seoPageContractTextRaw'] == expected_contract_text
    assert 'analysisResultsRaw' in app_config # Проверяем наличие данных анализа
    assert len(app_config['analysisResultsRaw']['paragraphs']) == 2 # Проверяем, что только 2 пункта
    mock_seo_service_instance.render_seo_page.assert_called_once_with('ipotechnyh-dogovorov')

def test_get_page_prompt_results(client, mock_services):
    mock_llm_service, mock_parsing_service, mock_cache_service, mock_seo_service, mock_seo_prompt_service = mock_services

    test_slug = "dareniya"
    mock_results = [
        {"prefix": "find_channels_for_ads1", "file_path": f"/path/to/content/seo_pages/{test_slug}/find_channels_for_ads1_20250625_143631.txt", "content": "Mocked content 1"},
        {"prefix": "ad_text_140_chars", "file_path": f"/path/to/content/seo_pages/{test_slug}/ad_text_140_chars_20250625_132220.txt", "content": "Mocked content 2"}
    ]
    mock_cache_service.get_all_prompt_results_for_page.return_value = mock_results

    rv = client.get(f'/api/v1/get_page_prompt_results?slug={test_slug}')
    assert rv.status_code == 200
    assert rv.json['status'] == 'ok'
    assert len(rv.json['results']) == len(mock_results)
    assert rv.json['results'][0]['prefix'] == "find_channels_for_ads1"
    assert rv.json['results'][1]['content'] == "Mocked content 2"
    mock_cache_service.get_all_prompt_results_for_page.assert_called_once_with(test_slug)


def pytest_sessionfinish(session, exitstatus):
    """Выводит итоговую статистику по завершении всех тестов"""
    print(f"\n{'='*50}")
    print(f"ИТОГОВАЯ СТАТИСТИКА ТЕСТОВ")
    print(f"{'='*50}")
    print(f"Всего пройдено тестов: {len(passed_tests)}")
    print(f"Список пройденных тестов (время выполнения):")
    for i, (test_name, exec_time) in enumerate(zip(passed_tests, passed_tests_times), 1):
        print(f"  {i}. {test_name} — {exec_time:.2f}с")
    print(f"{'='*50}")

def test_get_llm_models(real_client):
    """Тест для проверки эндпоинта /api/v1/get_llm_models."""
    rv = real_client.get('/api/v1/get_llm_models')
    assert rv.status_code == 200
    assert rv.json['status'] == 'ok'
    assert isinstance(rv.json['models'], list)
    assert len(rv.json['models']) > 0, "Должен быть возвращен хотя бы один доступный LLM"
    # Проверяем, что в списке есть модели (любые модели OpenAI или DeepSeek)
    models = rv.json['models']
    assert len(models) > 0, "Список моделей не должен быть пустым"
