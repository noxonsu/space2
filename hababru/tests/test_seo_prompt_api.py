import pytest
import os
import json
from unittest.mock import patch, MagicMock
from src.backend.main import create_app # Изменено на create_app
from src.backend.services.llm_service import LLMService # Импортируем для spec
from src.backend.services.seo_prompt_service import SeoPromptService # Импортируем для spec

# Базовый URL для Flask приложения
BASE_URL = "http://127.0.0.1:5001/api/v1"

# Пример полезной нагрузки, предоставленный пользователем
TEST_PAYLOAD = {
    "slug": "dareniya",
    "prompt": "Собери, пожалуйста, целевую аудиторию для этой страницы: {{PAGE_TITLE}}. Текст договора: {{CONTRACT_TEXT}}",
    "output_filename_prefix": "target_audience_result",
    "page_data": {
        "contract_file": "generated_contract.txt",
        "main_keyword": "дарения",
        "meta_description": "Быстрая онлайн проверка договора дарения с помощью нейросети. Анализ условий дарственной, юридическая экспертиза и оценка легальности договора дарения.",
        "meta_keywords": ["проверка договора дарения", "анализ условий дарственной", "юридическая экспертиза дарения", "проверка легальности договора дарения", "оценка условий договора дарения"],
        "slug": "dareniya",
        "title": "Проверка договора дарения онлайн нейросетью. Анализ условий и консультаця"
    }
}

# Путь к директории, где должен быть сохранен результат
# Это должно соответствовать логике в seo_prompt_service.py
# content_base_path + slug
SEO_PAGES_CONTENT_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'content', 'seo_pages'))
EXPECTED_OUTPUT_DIR = os.path.join(SEO_PAGES_CONTENT_BASE, TEST_PAYLOAD['slug'])

@pytest.fixture(scope='module', autouse=True)
def setup_and_teardown_output_dir():
    """
    Фикстура для очистки тестовой директории перед и после тестов.
    """
    os.makedirs(EXPECTED_OUTPUT_DIR, exist_ok=True)
    
    for f_name in os.listdir(EXPECTED_OUTPUT_DIR):
        if f_name.startswith(TEST_PAYLOAD['output_filename_prefix']):
            os.remove(os.path.join(EXPECTED_OUTPUT_DIR, f_name))
    
    yield
    
    for f_name in os.listdir(EXPECTED_OUTPUT_DIR):
        if f_name.startswith(TEST_PAYLOAD['output_filename_prefix']):
            os.remove(os.path.join(EXPECTED_OUTPUT_DIR, f_name))

@pytest.fixture
def mock_services():
    # Создаем моки для сервисов
    mock_llm_service = MagicMock(spec=LLMService)
    mock_seo_prompt_service = MagicMock(spec=SeoPromptService)

    # Настраиваем возвращаемые значения для моков
    mock_llm_service.generate_text.return_value = "Mocked LLM output for target audience and channels."
    mock_seo_prompt_service.run_openai_prompt_for_page.return_value = {
        "llm_output": "Mocked LLM output for target audience and channels.",
        "output_file_path": os.path.join(EXPECTED_OUTPUT_DIR, f"{TEST_PAYLOAD['output_filename_prefix']}_mock_timestamp.txt")
    }

    yield mock_llm_service, mock_seo_prompt_service

@pytest.fixture
def client(mock_services):
    mock_llm_service, mock_seo_prompt_service = mock_services
    
    # Передаем моки в create_app
    test_app = create_app(
        llm_service_mock=mock_llm_service,
        seo_prompt_service_mock=mock_seo_prompt_service
    )
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        yield client

def test_run_openai_prompt_success(client, mock_services): # Добавляем mock_services в аргументы
    mock_llm_service, mock_seo_prompt_service_instance = mock_services
    
    print(f"\nОтправка запроса на /admin/run_openai_prompt с payload: {json.dumps(TEST_PAYLOAD, indent=2)}")
    
    response = client.post('/admin/run_openai_prompt', json=TEST_PAYLOAD)
    
    print(f"Статус ответа: {response.status_code}")
    print(f"Тело ответа: {response.text}")

    assert response.status_code == 200
    response_data = response.get_json()
    
    assert "llm_output" in response_data
    assert "output_file_path" in response_data
    
    output_file_path = response_data["output_file_path"]
    print(f"Ожидаемый путь к файлу: {output_file_path}")
    
    mock_seo_prompt_service_instance.run_openai_prompt_for_page.assert_called_once_with(
        TEST_PAYLOAD['slug'],
        TEST_PAYLOAD['prompt'],
        TEST_PAYLOAD['output_filename_prefix'],
        TEST_PAYLOAD['page_data']
    )

    assert response_data["llm_output"] == "Mocked LLM output for target audience and channels."
    assert response_data["output_file_path"] == os.path.join(EXPECTED_OUTPUT_DIR, f"{TEST_PAYLOAD['output_filename_prefix']}_mock_timestamp.txt")
