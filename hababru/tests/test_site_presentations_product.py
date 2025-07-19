"""
Тесты для продукта создания презентационных сайтов
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.backend.services.products.site_presentations import SitePresentationsProduct
from src.backend.services.llm_service import LLMService
from src.backend.services.parsing_service import ParsingService
from src.backend.services.cache_service import CacheService


@pytest.fixture
def mock_llm_service():
    """Мок LLM сервиса"""
    return Mock(spec=LLMService)


@pytest.fixture
def mock_parsing_service():
    """Мок парсинг сервиса"""
    return Mock(spec=ParsingService)


@pytest.fixture
def mock_cache_service():
    """Мок кэш сервиса"""
    return Mock(spec=CacheService)


@pytest.fixture
def site_presentations_product(mock_llm_service, mock_parsing_service, mock_cache_service):
    """Фикстура продукта презентационных сайтов"""
    return SitePresentationsProduct(
        llm_service=mock_llm_service,
        parsing_service=mock_parsing_service,
        cache_service=mock_cache_service
    )


class TestSitePresentationsProduct:
    """Тесты для продукта создания презентационных сайтов"""
    
    def test_product_initialization(self, site_presentations_product):
        """Тест инициализации продукта"""
        assert site_presentations_product.product_id == "habab_site_presentations" # Исправлено
        assert site_presentations_product.name == "Презентационный сайт по брендбуку"
        assert "создание одностраничного сайта" in site_presentations_product.description.lower()
    
    def test_get_product_info(self, site_presentations_product):
        """Тест получения информации о продукте"""
        info = site_presentations_product.get_product_info()
        
        assert info["product_id"] == "habab_site_presentations" # Исправлено
        assert info["name"] == "Презентационный сайт по брендбуку"
        assert "key_benefits" in info
        assert "target_audience" in info
        assert "pricing" in info
        assert isinstance(info["key_benefits"], list)
        assert len(info["key_benefits"]) > 0
    
    def test_get_seo_keywords(self, site_presentations_product):
        """Тест получения SEO ключевых слов"""
        keywords = site_presentations_product.get_seo_keywords()
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert "презентационный сайт" in keywords
        assert "создание сайта" in keywords
        assert "по брендбуку" in keywords
    
    def test_get_demo_content(self, site_presentations_product):
        """Тест получения демо-контента"""
        demo_content = site_presentations_product.get_demo_content()
        
        assert isinstance(demo_content, dict)
        assert "demo_queries" in demo_content
        assert "sample_results" in demo_content
        assert isinstance(demo_content["demo_queries"], list)
        assert len(demo_content["demo_queries"]) > 0
    
    def test_get_input_interface_description(self, site_presentations_product):
        """Тест получения описания входного интерфейса"""
        interface = site_presentations_product.get_input_interface_description()
        
        assert isinstance(interface, dict)
        assert "title" in interface # Исправлено
        assert "fields" in interface # Исправлено
        assert isinstance(interface["fields"], list) # Добавлено
        assert len(interface["fields"]) > 0 # Добавлено
        assert "name" in interface["fields"][0] # Добавлено
        assert "type" in interface["fields"][0] # Добавлено
        assert "label" in interface["fields"][0] # Добавлено
        assert "accept" in interface["fields"][0] # Добавлено
        assert "required" in interface["fields"][0] # Добавлено
    
    def test_get_output_interface_description(self, site_presentations_product):
        """Тест получения описания выходного интерфейса"""
        interface = site_presentations_product.get_output_interface_description()
        
        assert isinstance(interface, dict)
        assert "title" in interface # Исправлено
        assert "format" in interface # Исправлено
        assert interface["format"] == "html" # Добавлено
    
    def test_execute_demo_success(self, site_presentations_product, mock_llm_service, mock_parsing_service):
        """Тест успешного выполнения демо"""
        # Подготавливаем мок данные
        input_data = {
            "presentation_files": ["presentation.pdf", "brandbook.pdf"],
            "telegram_contact": "@company_bot",
            "company_name": "Test Company"
        }
        
        # Мокируем парсинг презентации
        mock_parsing_service.parse_presentation.return_value = {
            "text_content": "Презентация компании Test Company",
            "design_elements": ["logo.png", "colors.json"],
            "structure": ["title", "about", "services", "contact"]
        }
        
        # Мокируем генерацию HTML
        mock_llm_service.generate_html_from_presentation.return_value = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Company</title></head>
        <body>
            <h1>Test Company</h1>
            <p>Презентация компании</p>
            <a href="https://t.me/company_bot" class="buy-button">Купить</a>
        </body>
        </html>
        """
        
        # Мокируем сохранение сайта
        with patch.object(site_presentations_product, '_save_website_files') as mock_save:
            mock_save.return_value = "https://testsite.example.com"
            
            result = site_presentations_product.execute_demo(input_data)
            
            # Проверяем результат
            assert "website_url" in result
            assert result["website_url"] == "https://testsite.example.com"
            assert "success" in result
            assert result["success"] is True
            
            # Проверяем вызовы моков
            mock_parsing_service.parse_presentation.assert_called_once()
            mock_llm_service.generate_html_from_presentation.assert_called_once()
            mock_save.assert_called_once()
    
    def test_execute_demo_missing_files(self, site_presentations_product):
        """Тест выполнения демо без файлов"""
        input_data = {}
        
        result = site_presentations_product.execute_demo(input_data)
        
        assert "error" in result
        assert "файлы презентации не предоставлены" in result["error"].lower()
    
    def test_execute_demo_parsing_error(self, site_presentations_product, mock_parsing_service):
        """Тест обработки ошибки парсинга"""
        input_data = {
            "presentation_files": ["presentation.pdf"]
        }
        
        # Мокируем ошибку парсинга
        mock_parsing_service.parse_presentation.side_effect = Exception("Ошибка парсинга")
        
        result = site_presentations_product.execute_demo(input_data)
        
        assert "error" in result
        assert "ошибка" in result["error"].lower()
    
    def test_generate_website_structure(self, site_presentations_product):
        """Тест генерации структуры сайта"""
        presentation_data = {
            "text_content": "Компания Test\nО нас\nУслуги\nКонтакты",
            "design_elements": ["#FF0000", "#00FF00"],
            "company_name": "Test Company"
        }
        
        structure = site_presentations_product._generate_website_structure(presentation_data)
        
        assert isinstance(structure, dict)
        assert "sections" in structure
        assert "styles" in structure
        assert len(structure["sections"]) > 0
    
    def test_validate_input_data_valid(self, site_presentations_product):
        """Тест валидации корректных входных данных"""
        input_data = {
            "presentation_files": ["presentation.pdf", "brandbook.pdf"],
            "telegram_contact": "@company_bot"
        }
        
        is_valid, error = site_presentations_product._validate_input_data(input_data)
        
        assert is_valid is True
        assert error is None
    
    def test_validate_input_data_invalid(self, site_presentations_product):
        """Тест валидации некорректных входных данных"""
        input_data = {}
        
        is_valid, error = site_presentations_product._validate_input_data(input_data)
        
        assert is_valid is False
        assert error is not None
        assert "presentation_files" in error
    
    def test_extract_telegram_contact(self, site_presentations_product):
        """Тест извлечения Telegram контакта"""
        # Тест корректного формата
        contact1 = site_presentations_product._extract_telegram_contact("@company_bot")
        assert contact1 == "@company_bot"
        
        # Тест URL формата
        contact2 = site_presentations_product._extract_telegram_contact("https://t.me/company_bot")
        assert contact2 == "@company_bot"
        
        # Тест без @
        contact3 = site_presentations_product._extract_telegram_contact("company_bot")
        assert contact3 == "@company_bot"
    
    def test_generate_seo_meta(self, site_presentations_product):
        """Тест генерации SEO метаданных"""
        presentation_data = {
            "company_name": "Test Company",
            "text_content": "Описание компании и услуг"
        }
        
        seo_meta = site_presentations_product._generate_seo_meta(presentation_data)
        
        assert isinstance(seo_meta, dict)
        assert "title" in seo_meta
        assert "description" in seo_meta
        assert "keywords" in seo_meta
        assert "Test Company" in seo_meta["title"]


class TestSitePresentationsIntegration:
    """Интеграционные тесты для продукта презентационных сайтов"""
    
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', create=True)
    def test_save_website_files(self, mock_open, mock_mkdir, site_presentations_product):
        """Тест сохранения файлов сайта"""
        html_content = "<html><body>Test</body></html>"
        css_content = "body { margin: 0; }"
        assets = {"logo.png": b"fake_image_data"}
        
        with patch.object(site_presentations_product, '_get_website_url') as mock_url:
            mock_url.return_value = "https://testsite.example.com"
            
            result_url = site_presentations_product._save_website_files(
                html_content, css_content, assets
            )
            
            assert result_url == "https://testsite.example.com"
            mock_mkdir.assert_called()
            assert mock_open.call_count >= 2  # HTML и CSS файлы
