import pytest
import os
from src.backend.main import app
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import shutil
import markdown # Added for markdown conversion in test
import yaml # Added for yaml parsing in test

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_services(): # Removed request fixture
    with patch('src.backend.services.parsing_service.ParsingService') as MockParsingService, \
         patch('src.backend.services.cache_service.CacheService') as MockCacheService, \
         patch('src.backend.services.llm_service.LLMService') as MockLLMService, \
         patch('os.makedirs') as mock_makedirs:
        
        # Configure mocks
        mock_llm_instance = MockLLMService.return_value
        mock_parsing_instance = MockParsingService.return_value
        mock_cache_instance = MockCacheService.return_value
        
        # Configure mock for CacheService.get_file_cache_dir to return a valid path
        temp_cache_dir = tempfile.mkdtemp()
        mock_cache_instance.get_file_cache_dir.return_value = temp_cache_dir
        # Mock _generate_hash as well for test_upload_contract
        mock_cache_instance._generate_hash.return_value = "mocked_hash_123"

        # Patch app.config to return our mock instances
        app.config['PARSING_SERVICE'] = mock_parsing_instance
        app.config['LLM_SERVICE'] = mock_llm_instance
        app.config['CACHE_SERVICE'] = mock_cache_instance

        yield mock_parsing_instance, mock_cache_instance, mock_llm_instance # Removed seo_service_global_mock from yield
        
        # Clean up the temporary directory after tests
        shutil.rmtree(temp_cache_dir)

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    # Check for a more generic string that is likely to be present
    assert b"<!DOCTYPE html>" in rv.data 

def test_seo_page(client): # Removed mock_services from args
    with patch('src.backend.main.seo_service') as mock_seo_service_global_mock: # Moved patch here
        mock_seo_service_global_mock.render_seo_page.return_value = "<html><body>Test SEO Page Content</body></html>"
        rv = client.get('/arendy')
        assert rv.status_code == 200
        assert b"Test SEO Page Content" in rv.data
        mock_seo_service_global_mock.render_seo_page.assert_called_once_with('arendy')

def test_get_sample_contract(client, mock_services):
    mock_parsing_instance, mock_cache_instance, mock_llm_instance = mock_services
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
    mock_parsing_instance, mock_cache_instance, mock_llm_instance = mock_services
    
    mock_parsing_instance.parse_document_to_markdown.return_value = "Parsed PDF content"
    
    # Use BytesIO for dummy file data to avoid real file system interaction
    from io import BytesIO
    file_data = BytesIO(b"dummy content")
    file_data.name = "dummy.pdf" # Flask expects a 'name' attribute for file objects

    # Patch the open call within contract_analyzer.py
    with patch('src.backend.api.v1.contract_analyzer.open', mock_open()) as mock_file_open:
        rv = client.post('/api/v1/upload_contract', data={'file': (file_data, 'dummy.pdf')})
    
    assert rv.status_code == 200
    assert "message" in rv.json
    assert "contract_id" in rv.json # Changed from "contract_text" to "contract_id" as per contract_analyzer.py
    assert rv.json["contract_id"] == mock_cache_instance._generate_hash.return_value # Assert with mocked hash
    mock_parsing_instance.parse_document_to_markdown.assert_called_once()
    mock_cache_instance._generate_hash.assert_called_once() # Ensure hash generation is called
    mock_cache_instance.get_file_cache_dir.assert_called_once() # Ensure cache dir is retrieved
    mock_file_open.assert_called_once() # Ensure open was called to write to cache
    mock_file_open().write.assert_called_once_with("Parsed PDF content") # Ensure content was written

def test_seo_page_content_display(client, mock_services):
    mock_parsing_instance, mock_cache_instance, mock_llm_instance = mock_services

    # Define paths to the actual content files
    seo_page_dir = os.path.join(app.root_path, 'content', 'seo_pages', 'arendy')
    source_md_path = os.path.join(seo_page_dir, 'source.md')
    generated_contract_path = os.path.join(seo_page_dir, 'generated_contract.txt')

    # Read expected content
    with open(source_md_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    parts = source_content.split('---', 2)
    front_matter = yaml.safe_load(parts[1])
    page_text_content_md = parts[2].strip()
    expected_page_text_html = markdown.markdown(page_text_content_md)

    with open(generated_contract_path, 'r', encoding='utf-8') as f:
        expected_contract_text = f.read()

    # Mock the render_seo_page to allow actual rendering logic to run
    # We need to ensure the actual seo_service.render_seo_page is called, not mocked
    # So, we will remove the mock for seo_service_global_mock.render_seo_page for this test
    # Or, more simply, we can just call the route directly and let the real seo_service run

    rv = client.get('/arendy')
    assert rv.status_code == 200

    # Assert that the page title is present
    assert front_matter['title'].encode('utf-8') in rv.data

    # Assert that the main page text content is present
    assert expected_page_text_html.encode('utf-8') in rv.data

    # Assert that the contract text is present by checking the content of the script tag
    # that defines window.appConfig
    import json
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(rv.data, 'html.parser')
    script_tag = soup.find('script', string=lambda t: t and 'window.appConfig' in t)
    assert script_tag is not None

    # Extract the JavaScript code, parse it, and check the data
    import re
    import json
    import html # Import html module for unescape

    js_code = script_tag.string
    # Use regex to find the appConfig object
    # The regex needs to match the content inside JSON.parse('')
    match = re.search(r"window\.appConfig\s*=\s*JSON\.parse\('(.*)'\);", js_code, re.DOTALL)
    assert match, "Could not find window.appConfig object in script tag"
    
    app_config_escaped_json = match.group(1)
    # Unescape HTML entities before parsing as JSON
    app_config_json = html.unescape(app_config_escaped_json)
    app_config = json.loads(app_config_json)

    assert app_config['seoPageContractTextRaw'] == expected_contract_text

def test_seo_page_ipotechnyh_dogovorov_content_display(client, mock_services):
    mock_parsing_instance, mock_cache_instance, mock_llm_instance = mock_services

    # Define paths to the actual content files for 'ipotechnyh-dogovorov'
    seo_page_dir = os.path.join(app.root_path, 'content', 'seo_pages', 'ipotechnyh-dogovorov')
    source_md_path = os.path.join(seo_page_dir, 'source.md')
    generated_contract_path = os.path.join(seo_page_dir, 'generated_contract.txt')

    # Read expected content
    with open(source_md_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    parts = source_content.split('---', 2)
    front_matter = yaml.safe_load(parts[1])
    page_text_content_md = parts[2].strip()
    expected_page_text_html = markdown.markdown(page_text_content_md)

    with open(generated_contract_path, 'r', encoding='utf-8') as f:
        expected_contract_text = f.read()

    rv = client.get('/ipotechnyh-dogovorov')
    assert rv.status_code == 200

    # Assert that the page title is present
    assert front_matter['title'].encode('utf-8') in rv.data

    # Assert that the main page text content is present
    assert expected_page_text_html.encode('utf-8') in rv.data

    # Assert that the contract text is present by checking the content of the script tag
    import json
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(rv.data, 'html.parser')
    script_tag = soup.find('script', string=lambda t: t and 'window.appConfig' in t)
    assert script_tag is not None

    # Extract the JavaScript code, parse it, and check the data
    import re
    import json
    import html # Import html module for unescape

    js_code = script_tag.string
    # Use regex to find the appConfig object
    match = re.search(r"window\.appConfig\s*=\s*JSON\.parse\('(.*)'\);", js_code, re.DOTALL)
    assert match, "Could not find window.appConfig object in script tag"
    
    app_config_escaped_json = match.group(1)
    # Unescape HTML entities before parsing as JSON
    app_config_json = html.unescape(app_config_escaped_json)
    app_config = json.loads(app_config_json)

    assert app_config['seoPageContractTextRaw'] == expected_contract_text
