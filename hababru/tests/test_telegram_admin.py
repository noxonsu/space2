"""
Тесты для Telegram админки
"""

import pytest
import json
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
def mock_telegram_connector():
    """Мок Telegram коннектора"""
    connector = Mock()
    connector.fetch_recent_messages.return_value = [
        TelegramMessage(
            message_id=123,
            text="Новый AI инструмент для автоматизации бизнес-процессов",
            date="2025-01-03T10:00:00Z",
            media_files=["image1.jpg"]
        ),
        TelegramMessage(
            message_id=124,
            text="Короткий текст",
            date="2025-01-03T11:00:00Z",
            media_files=[]
        )
    ]
    return connector


class TestTelegramAdmin:
    """Тесты для Telegram админки"""
    
    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_get_telegram_messages_success(self, mock_connector_class, client, mock_telegram_connector):
        """Тест успешного получения Telegram сообщений"""
        mock_connector_class.return_value = mock_telegram_connector
        
        response = client.get('/admin/telegram/messages?limit=10')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['messages']) == 2
        assert data['messages'][0]['message_id'] == 123
        assert data['messages'][0]['is_suitable'] is True
        assert data['messages'][1]['is_suitable'] is False
    
    def test_get_telegram_messages_no_token(self, client):
        """Тест получения сообщений без токена"""
        response = client.get('/admin/telegram/messages')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'не настроен' in data['error']
    
    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_check_telegram_duplicates_no_duplicate(self, mock_connector_class, client, mock_telegram_connector):
        """Тест проверки дублей - дубликатов нет"""
        mock_connector_class.return_value = mock_telegram_connector
        
        with patch('src.backend.api.v1.seo_tools.TelegramProductGenerator') as mock_generator_class:
            mock_generator = mock_generator_class.return_value
            mock_generator._check_semantic_duplicate.return_value = None
            
            response = client.post('/admin/telegram/check-duplicates',
                                 data=json.dumps({'message_id': 123}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['has_duplicate'] is False
    
    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_check_telegram_duplicates_found(self, mock_connector_class, client, mock_telegram_connector):
        """Тест проверки дублей - дубликат найден"""
        mock_connector_class.return_value = mock_telegram_connector
        
        with patch('src.backend.api.v1.seo_tools.TelegramProductGenerator') as mock_generator_class:
            mock_generator = mock_generator_class.return_value
            mock_generator._check_semantic_duplicate.return_value = 'existing_product'
            mock_generator._get_existing_products_with_data.return_value = {
                'existing_product': {
                    'name': 'Существующий продукт',
                    'description': 'Описание существующего продукта'
                }
            }
            
            response = client.post('/admin/telegram/check-duplicates',
                                 data=json.dumps({'message_id': 123}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['has_duplicate'] is True
            assert data['duplicate_product_id'] == 'existing_product'
            assert data['duplicate_product_name'] == 'Существующий продукт'
    
    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_generate_product_success(self, mock_connector_class, client, mock_telegram_connector):
        """Тест успешной генерации продукта"""
        mock_connector_class.return_value = mock_telegram_connector
        
        with patch('src.backend.api.v1.seo_tools.TelegramProductGenerator') as mock_generator_class:
            mock_generator = mock_generator_class.return_value
            mock_generator.generate_product_from_message.return_value = {
                'success': True,
                'product_id': 'ai_automation_tool',
                'product_name': 'AI инструмент автоматизации',
                'file_path': '/path/to/product.yaml'
            }
            
            response = client.post('/admin/telegram/generate',
                                 data=json.dumps({'message_id': 123}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['product_id'] == 'ai_automation_tool'
            assert data['product_name'] == 'AI инструмент автоматизации'
    
    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_generate_product_duplicate_found(self, mock_connector_class, client, mock_telegram_connector):
        """Тест генерации продукта - найден дубликат"""
        mock_connector_class.return_value = mock_telegram_connector
        
        with patch('src.backend.api.v1.seo_tools.TelegramProductGenerator') as mock_generator_class:
            mock_generator = mock_generator_class.return_value
            mock_generator.generate_product_from_message.return_value = {
                'success': False,
                'error': 'Продукт с похожим смыслом уже существует',
                'duplicate_product_id': 'existing_product'
            }
            
            response = client.post('/admin/telegram/generate',
                                 data=json.dumps({'message_id': 123}),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is False
            assert 'duplicate_product_id' in data
            assert data['duplicate_product_id'] == 'existing_product'
    
    @patch('src.backend.api.v1.seo_tools.TelegramProductGenerator')
    def test_get_existing_products(self, mock_generator_class, client):
        """Тест получения существующих продуктов"""
        mock_generator = mock_generator_class.return_value
        mock_generator._get_existing_products_with_data.return_value = {
            'product1': {
                'name': 'Продукт 1',
                'description': 'Описание продукта 1',
                'category': 'ai',
                'status': 'active'
            },
            'product2': {
                'name': 'Продукт 2',
                'description': 'Описание продукта 2',
                'category': 'analytics',
                'status': 'active'
            }
        }
        
        response = client.get('/admin/telegram/products')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['products']) == 2
        assert data['products'][0]['product_id'] == 'product1'
        assert data['products'][0]['name'] == 'Продукт 1'
        assert data['products'][0]['category'] == 'ai'
    
    def test_check_duplicates_missing_message_id(self, client):
        """Тест проверки дублей без message_id"""
        response = client.post('/admin/telegram/check-duplicates',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'message_id' in data['error']
    
    def test_generate_product_missing_message_id(self, client):
        """Тест генерации продукта без message_id"""
        response = client.post('/admin/telegram/generate',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'message_id' in data['error']
    
    @patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token'})
    @patch('src.backend.api.v1.seo_tools.TelegramConnector')
    def test_message_not_found(self, mock_connector_class, client):
        """Тест случая когда сообщение не найдено"""
        mock_connector = Mock()
        mock_connector.fetch_recent_messages.return_value = []
        mock_connector_class.return_value = mock_connector
        
        response = client.post('/admin/telegram/generate',
                             data=json.dumps({'message_id': 999}),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert 'не найдено' in data['error']
