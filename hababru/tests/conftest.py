"""
Конфигурация тестов для админки
"""
import pytest
import tempfile
import shutil
from unittest.mock import MagicMock
from src.backend.main import create_app
from src.backend.services.llm_service import LLMService
from src.backend.services.parsing_service import ParsingService
from src.backend.services.cache_service import CacheService
from src.backend.services.seo_service import SeoService
from src.backend.services.seo_prompt_service import SeoPromptService


@pytest.fixture
def mock_services():
    """Создает моки всех сервисов"""
    mock_llm_service = MagicMock(spec=LLMService)
    mock_parsing_service = MagicMock(spec=ParsingService)
    mock_cache_service = MagicMock(spec=CacheService)
    mock_seo_service = MagicMock(spec=SeoService)
    mock_seo_prompt_service = MagicMock(spec=SeoPromptService)

    # Настраиваем базовые возвращаемые значения
    mock_llm_service.generate_text.return_value = "Тестовый ответ от LLM"
    mock_parsing_service.parse_document_to_markdown.return_value = "Обработанный документ"
    mock_cache_service._generate_hash.return_value = "test_hash_123"

    # Создаем временную директорию для кэша
    temp_cache_dir = tempfile.mkdtemp()
    mock_cache_service.get_file_cache_dir.return_value = temp_cache_dir

    yield mock_llm_service, mock_parsing_service, mock_cache_service, mock_seo_service, mock_seo_prompt_service
    
    # Очищаем временную директорию
    shutil.rmtree(temp_cache_dir, ignore_errors=True)


@pytest.fixture
def app(mock_services):
    """Создает тестовое приложение Flask"""
    mock_llm_service, mock_parsing_service, mock_cache_service, mock_seo_service, mock_seo_prompt_service = mock_services
    
    test_app = create_app(
        llm_service_mock=mock_llm_service,
        parsing_service_mock=mock_parsing_service,
        cache_service_mock=mock_cache_service,
        seo_service_mock=mock_seo_service,
        seo_prompt_service_mock=mock_seo_prompt_service
    )
    test_app.config['TESTING'] = True
    return test_app


@pytest.fixture
def client(app):
    """Создает тестовый клиент Flask"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_client(client):
    """Клиент для тестирования админки (с возможной авторизацией в будущем)"""
    # В будущем здесь можно добавить логику авторизации админа
    return client
