"""
Тесты для функциональности перегенерации продуктов из Telegram
"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from src.backend.main import create_app
from src.backend.services.telegram_product_generator import TelegramMessage


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
def mock_telegram_message():
    """Фикстура для тестового Telegram сообщения"""
    return TelegramMessage(
        message_id=123,
        text="Новый AI инструмент для автоматизации бизнес-процессов",
        date="2025-01-03T10:00:00Z",
        media_files=["image1.jpg"]
    )


class TestTelegramRegeneration:
    """Тесты для перегенерации продуктов из Telegram"""

    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_regenerate_product_success(self, mock_connector_class, client, mock_telegram_message):
        """Тест успешной перегенерации продукта"""
        mock_connector = Mock()
        mock_connector.fetch_recent_messages.return_value = [mock_telegram_message]
        mock_connector_class.return_value = mock_connector
        
        with patch('src.backend.api.v1.seo_tools.TelegramProductGenerator') as mock_generator_class:
            mock_generator = mock_generator_class.return_value
            mock_generator.generate_product_from_message.return_value = {
                'success': True,
                'product_id': 'regenerated_ai_tool',
                'product_name': 'Перегенерированный AI инструмент',
                'file_path': '/path/to/regenerated.yaml'
            }
            
            with patch('src.backend.api.v1.seo_tools.llm_service') as mock_llm_service:
                mock_llm_service.set_current_model.return_value = None
                
                response = client.post('/admin/telegram/regenerate',
                                     data=json.dumps({
                                         'message_id': 123,
                                         'model': 'gpt-4o',
                                         'force_regenerate': True
                                     }),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
                assert data['product_id'] == 'regenerated_ai_tool'
                assert data['model_used'] == 'gpt-4o'
                assert data['regenerated'] is True
                
                # Проверяем что модель была установлена
                mock_llm_service.set_current_model.assert_called_once_with('gpt-4o')

    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_regenerate_product_invalid_model(self, mock_connector_class, client, mock_telegram_message):
        """Тест перегенерации с некорректной моделью"""
        mock_connector = Mock()
        mock_connector.fetch_recent_messages.return_value = [mock_telegram_message]
        mock_connector_class.return_value = mock_connector
        
        with patch('src.backend.api.v1.seo_tools.llm_service') as mock_llm_service:
            mock_llm_service.set_current_model.side_effect = ValueError("Модель 'invalid-model' недоступна")
            
            response = client.post('/admin/telegram/regenerate',
                                 data=json.dumps({
                                     'message_id': 123,
                                     'model': 'invalid-model'
                                 }),
                                 content_type='application/json')
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] is False
            assert 'недоступна' in data['error']

    @patch('src.backend.api.v1.seo_tools.TelegramProductGenerator')
    def test_batch_regenerate_success(self, mock_generator_class, client):
        """Тест успешной массовой перегенерации"""
        mock_generator = mock_generator_class.return_value
        mock_generator._get_existing_products_with_data.return_value = {
            'product1': {'name': 'Продукт 1', 'description': 'Описание 1'},
            'product2': {'name': 'Продукт 2', 'description': 'Описание 2'}
        }
        
        # Мокируем успешную генерацию
        mock_generator.generate_product_from_message.side_effect = [
            {
                'success': True,
                'product_id': 'regenerated_product1',
                'product_name': 'Перегенерированный продукт 1'
            },
            {
                'success': True,
                'product_id': 'regenerated_product2',
                'product_name': 'Перегенерированный продукт 2'
            }
        ]
        
        with patch('src.backend.api.v1.seo_tools.llm_service') as mock_llm_service:
            mock_llm_service.set_current_model.return_value = None
            
            with patch('os.remove') as mock_remove:
                response = client.post('/admin/telegram/batch-regenerate',
                                     data=json.dumps({
                                         'model': 'gpt-4o',
                                         'product_ids': ['product1', 'product2']
                                     }),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
                assert data['model_used'] == 'gpt-4o'
                assert data['regenerated'] == 2
                assert data['failed'] == 0
                assert len(data['results']) == 2
                
                # Проверяем что модель была установлена
                mock_llm_service.set_current_model.assert_called_once_with('gpt-4o')

    def test_batch_regenerate_missing_product_ids(self, client):
        """Тест массовой перегенерации без указания product_ids"""
        response = client.post('/admin/telegram/batch-regenerate',
                             data=json.dumps({
                                 'model': 'gpt-4o',
                                 'product_ids': []
                             }),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'product_ids' in data['error']
