import pytest
import requests
from unittest.mock import patch, MagicMock
from src.backend.services.llm_service import LLMService
from src.backend.services.cache_service import CacheService

@pytest.fixture
def llm_service():
    with patch('src.backend.services.llm_service.CacheService') as mock_cache:
        service = LLMService(deepseek_api_key="test_key", openai_api_key="")
        service.cache_service = MagicMock()
        yield service

@patch('src.backend.services.llm_service.requests.post')
def test_generate_text_deepseek(mock_post, llm_service):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "DeepSeek response"}}]
    }
    mock_post.return_value = mock_response

    response = llm_service.generate_text("Test prompt")
    assert response == "DeepSeek response"
    mock_post.assert_called_once()
    assert "api.deepseek.com" in mock_post.call_args[0][0]

@patch('src.backend.services.llm_service.requests.post')
def test_generate_text_openai(mock_post):
    with patch('src.backend.services.llm_service.CacheService'):
        service = LLMService(deepseek_api_key="", openai_api_key="test_key")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "OpenAI response"}}]
        }
        mock_post.return_value = mock_response

        response = service.generate_text("Test prompt")
        assert response == "OpenAI response"
        mock_post.assert_called_once()
        assert "api.openai.com" in mock_post.call_args[0][0]

@patch('src.backend.services.llm_service.requests.post')
def test_api_error_handling(mock_post, llm_service):
    mock_post.side_effect = requests.exceptions.Timeout
    with pytest.raises(TimeoutError):
        llm_service.generate_text("Test prompt")
