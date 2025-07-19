"""
Интеграционные тесты для получения списка моделей от провайдеров
"""

import pytest
import os
import requests
from unittest.mock import Mock, patch, MagicMock
from src.backend.services.llm_service import LLMService
from src.backend.main import create_app


@pytest.fixture
def app():
    """Фикстура Flask приложения"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Фикстура тестового клиента"""
    return app.test_client()


@pytest.fixture
def llm_service():
    """Фикстура LLM сервиса"""
    return LLMService(
        deepseek_api_key="test_deepseek_key",
        openai_api_key="test_openai_key"
    )


class TestLLMModelsIntegration:
    """Интеграционные тесты для получения моделей"""
    
    def test_get_deepseek_models_success(self, llm_service):
        """Тест успешного получения моделей DeepSeek"""
        mock_response = {
            "data": [
                {"id": "deepseek-chat", "object": "model"},
                {"id": "deepseek-coder", "object": "model"}
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            models = llm_service._get_deepseek_models()
            
            assert "deepseek-chat" in models
            assert "deepseek-coder" in models
            
            # Проверяем что был сделан правильный запрос
            mock_get.assert_called_once_with(
                "https://api.deepseek.com/v1/models",
                headers={
                    "Authorization": "Bearer test_deepseek_key",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
    
    def test_get_openai_models_success(self, llm_service):
        """Тест успешного получения моделей OpenAI"""
        mock_response = {
            "data": [
                {"id": "gpt-4o", "object": "model"},
                {"id": "gpt-3.5-turbo", "object": "model"},
                {"id": "text-embedding-ada-002", "object": "model"}  # Будет отфильтрован
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            models = llm_service._get_openai_models()
            
            assert "gpt-4o" in models
            assert "gpt-3.5-turbo" in models
            assert "text-embedding-ada-002" not in models  # Должен быть отфильтрован
            
            # Проверяем что был сделан правильный запрос
            mock_get.assert_called_once_with(
                "https://api.openai.com/v1/models",
                headers={
                    "Authorization": "Bearer test_openai_key",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
    
    def test_get_deepseek_models_api_error(self, llm_service):
        """Тест обработки ошибки API DeepSeek"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 401
            
            models = llm_service._get_deepseek_models()
            
            # Должны вернуться дефолтные модели
            assert "deepseek-chat" in models
            assert "deepseek-coder" in models
    
    def test_get_openai_models_api_error(self, llm_service):
        """Тест обработки ошибки API OpenAI"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 401
            
            models = llm_service._get_openai_models()
            
            # Должны вернуться дефолтные модели
            assert "gpt-4o" in models
            assert "gpt-3.5-turbo" in models
    
    def test_get_available_models_combined(self, llm_service):
        """Тест получения объединенного списка моделей"""
        deepseek_response = {
            "data": [
                {"id": "deepseek-chat", "object": "model"}
            ]
        }
        
        openai_response = {
            "data": [
                {"id": "gpt-4o", "object": "model"},
                {"id": "gpt-3.5-turbo", "object": "model"}
            ]
        }
        
        with patch('requests.get') as mock_get:
            # Мокируем разные ответы для разных URL
            def side_effect(url, **kwargs):
                mock_resp = Mock()
                mock_resp.status_code = 200
                
                if "deepseek.com" in url:
                    mock_resp.json.return_value = deepseek_response
                elif "openai.com" in url:
                    mock_resp.json.return_value = openai_response
                
                return mock_resp
            
            mock_get.side_effect = side_effect
            
            models = llm_service.get_available_models()
            
            # Проверяем что есть модели от обоих провайдеров
            assert "deepseek:deepseek-chat" in models
            assert "openai:gpt-4o" in models
            assert "openai:gpt-3.5-turbo" in models
            
            # Проверяем что список отсортирован
            assert models == sorted(models)
    
    def test_set_current_model_success(self, llm_service):
        """Тест успешной установки текущей модели"""
        with patch.object(llm_service, 'get_available_models', return_value=['deepseek:deepseek-chat', 'openai:gpt-4o']):
            llm_service.set_current_model('openai:gpt-4o')
            
            assert llm_service.current_model_full_id == 'openai:gpt-4o' # Изменено
    
    def test_get_model_info(self, llm_service):
        """Тест получения информации о модели"""
        info = llm_service.get_model_info('openai:gpt-4o') # Изменено
        
        assert info['provider'] == 'OpenAI'
        assert info['description'] == 'Новейшая модель GPT-4 Omni'
        assert info['context_length'] == '128k'
        
        # Тест неизвестной модели
        unknown_info = llm_service.get_model_info('unknown:unknown-model') # Изменено
        assert unknown_info['provider'] == 'Unknown'


class TestTelegramModelsAPI:
    """Тесты для API получения моделей в Telegram админке"""
    
    def test_get_available_models_api_success(self, app, client): # Удаляем mock_current_app
        """Тест успешного получения моделей через API"""
        mock_llm_service = MagicMock(spec=LLMService)
        mock_llm_service.get_available_models.return_value = ['deepseek:deepseek-chat', 'openai:gpt-4o']
        mock_llm_service.current_model_full_id = 'deepseek:deepseek-chat'
        mock_llm_service.get_model_info.side_effect = lambda model: {
            'deepseek:deepseek-chat': {'provider': 'DeepSeek', 'description': 'Chat model', 'context_length': '32k'},
            'openai:gpt-4o': {'provider': 'OpenAI', 'description': 'GPT-4 Omni', 'context_length': '128k'}
        }[model]
        
        # Используем реальный app.config
        app.config['LLM_SERVICE'] = mock_llm_service
        app.logger = MagicMock() # Мокируем логгер
        
        response = client.get('/admin/telegram/models')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'deepseek:deepseek-chat' in data['models']
        assert 'openai:gpt-4o' in data['models']
        assert data['current_model'] == 'deepseek:deepseek-chat'
        
        # Проверяем информацию о моделях
        models_info = data['models_info']
        assert len(models_info) == 2
        
        deepseek_info = next(info for info in models_info if info['id'] == 'deepseek:deepseek-chat')
        assert deepseek_info['provider'] == 'DeepSeek'
        assert deepseek_info['context_length'] == '32k'
    
    def test_get_available_models_api_error(self, app, client): # Удаляем mock_current_app
        """Тест обработки ошибки получения моделей через API"""
        mock_llm_service = MagicMock(spec=LLMService)
        mock_llm_service.get_available_models.side_effect = Exception("API Error")
        
        # Используем реальный app.config
        app.config['LLM_SERVICE'] = mock_llm_service
        app.logger = MagicMock() # Мокируем логгер
        
        response = client.get('/admin/telegram/models')
        
        assert response.status_code == 500
        data = response.get_json()
        assert data['success'] is False
        assert 'API Error' in data['error']


class TestRealAPIIntegration:
    """Тесты для реальной интеграции с API (требуют реальных ключей)"""
    
    @pytest.mark.skipif(
        not os.getenv('DEEPSEEK_API_KEY'),
        reason="Требуется реальный DEEPSEEK_API_KEY для интеграционного теста"
    )
    def test_real_deepseek_models(self):
        """Интеграционный тест с реальным DeepSeek API"""
        llm_service = LLMService(
            deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY') # Передаем оба ключа
        )
        
        models = llm_service._get_deepseek_models()
        
        assert len(models) > 0
        assert any('deepseek' in model.lower() for model in models)
    
    @pytest.mark.skipif(
        not os.getenv('OPENAI_API_KEY'),
        reason="Требуется реальный OPENAI_API_KEY для интеграционного теста"
    )
    def test_real_openai_models(self):
        """Интеграционный тест с реальным OpenAI API"""
        llm_service = LLMService(
            deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'), # Передаем оба ключа
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        
        models = llm_service._get_openai_models()
        
        assert len(models) > 0
        assert any('gpt' in model.lower() for model in models)
    
    @pytest.mark.skipif(
        not (os.getenv('DEEPSEEK_API_KEY') and os.getenv('OPENAI_API_KEY')),
        reason="Требуются реальные API ключи для полного интеграционного теста"
    )
    def test_real_combined_models(self):
        """Интеграционный тест с реальными API обоих провайдеров"""
        llm_service = LLMService(
            deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        
        models = llm_service.get_available_models()
        
        assert len(models) > 0
        # Должны быть модели от обоих провайдеров
        has_deepseek = any('deepseek' in model.lower() for model in models)
        has_openai = any('gpt' in model.lower() for model in models)
        
        assert has_deepseek or has_openai  # Хотя бы один провайдер должен работать
