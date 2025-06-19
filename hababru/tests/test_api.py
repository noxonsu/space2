import pytest
import os
from src.backend.main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_services():
    with patch('src.backend.services.parsing_service.ParsingService') as MockParsingService, \
         patch('src.backend.services.cache_service.CacheService') as MockCacheService, \
         patch('src.backend.services.llm_service.LLMService') as MockLLMService, \
         patch('src.backend.main.seo_service') as MockSeoServiceInstance: # Patch the global instance in main.py
        
        # Configure mocks
        mock_llm_instance = MockLLMService.return_value
        mock_parsing_instance = MockParsingService.return_value
        mock_cache_instance = MockCacheService.return_value
        # MockSeoServiceInstance is already the mock of the global instance

        # Patch app.config to return our mock instances (for other parts of the app that might use app.config)
        app.config['PARSING_SERVICE'] = mock_parsing_instance
        app.config['LLM_SERVICE'] = mock_llm_instance
        app.config['CACHE_SERVICE'] = mock_cache_instance
        # app.config['SEO_SERVICE'] is not directly used by the route, but the global seo_service is.

        yield mock_parsing_instance, mock_cache_instance, mock_llm_instance, MockSeoServiceInstance # Yield the mocked global instance

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    # Check for a more generic string that is likely to be present
    assert b"<!DOCTYPE html>" in rv.data 

def test_seo_page(client, mock_services):
    mock_parsing_instance, mock_cache_instance, mock_llm_instance, mock_seo_service_global_mock = mock_services
    mock_seo_service_global_mock.render_seo_page.return_value = "<html><body>Test SEO Page Content</body></html>"
    rv = client.get('/analiz-dogovora-arendy')
    assert rv.status_code == 200
    assert b"Test SEO Page Content" in rv.data
    mock_seo_service_global_mock.render_seo_page.assert_called_once_with('analiz-dogovora-arendy')

def test_get_sample_contract(client, mock_services):
    mock_parsing_instance, mock_cache_instance, mock_llm_instance, mock_seo_service_global_mock = mock_services
    # The actual implementation of get_sample_contract reads from a file
    # We need to mock the file reading or the method that provides the text
    # Assuming it calls parsing_service.get_text_from_file or similar
    # For now, let's mock the response directly if it's a simple JSON endpoint
    # If it reads from default_nda.txt, we might need to mock open() or the service method
    
    # Let's assume the endpoint directly returns JSON with 'contract_text'
    # If the endpoint uses parsing_service, we'd mock that.
    # For now, we'll just check the key.
    rv = client.get('/api/v1/get_sample_contract')
    assert rv.status_code == 200
    assert "contract_text" in rv.json
    assert isinstance(rv.json["contract_text"], str)

def test_upload_contract(client, mock_services):
    mock_parsing_instance, mock_cache_instance, mock_llm_instance, mock_seo_service_global_mock = mock_services
    
    mock_parsing_instance.parse_document_to_markdown.return_value = "Parsed PDF content"
    
    # Create a dummy file for upload
    with open("dummy.pdf", "w") as f:
        f.write("dummy content")

    with open("dummy.pdf", "rb") as f:
        rv = client.post('/api/v1/upload_contract', data={'file': (f, 'dummy.pdf')})
    
    os.remove("dummy.pdf")
    
    assert rv.status_code == 200
    assert "message" in rv.json
    assert "contract_text" in rv.json
    assert rv.json["contract_text"] == "Parsed PDF content"
    mock_parsing_instance.parse_document_to_markdown.assert_called_once()
    # segment_text_into_paragraphs and create_analysis_task are called in /start_analysis, not /upload_contract
    # mock_parsing_instance.segment_text_into_paragraphs.assert_called_once()
    # mock_cache_instance.create_analysis_task.assert_called_once()
