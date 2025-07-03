"""
Тесты для Telegram коннектора
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from src.backend.services.telegram_connector import TelegramConnector, TelegramMonitor


class TestTelegramConnector:
    """Тесты для TelegramConnector"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        self.connector = TelegramConnector(
            bot_token="test_token_123",
            channel_username="@aideaxondemos"
        )
    
    def test_connector_initialization(self):
        """Тест инициализации коннектора"""
        assert self.connector.bot_token == "test_token_123"
        assert self.connector.channel_username == "aideaxondemos"
        assert self.connector.api_base_url == "https://api.telegram.org/bottest_token_123"
        assert self.connector.last_message_id == 0
    
    def test_connector_initialization_with_at_symbol(self):
        """Тест инициализации с @ в имени канала"""
        connector = TelegramConnector("token", "@testchannel")
        assert connector.channel_username == "testchannel"
    
    @patch('requests.get')
    def test_get_chat_info_success(self, mock_get):
        """Тест успешного получения информации о канале"""
        # Мокируем успешный ответ
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": True,
            "result": {
                "id": -1001234567890,
                "title": "AI Demo Channel",
                "username": "aideaxondemos",
                "type": "channel"
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        chat_info = self.connector._get_chat_info()
        
        assert chat_info is not None
        assert chat_info["id"] == -1001234567890
        assert chat_info["username"] == "aideaxondemos"
        
        # Проверяем правильность вызова API
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "getChat" in call_args[0][0]
        assert call_args[1]["params"]["chat_id"] == "@aideaxondemos"
    
    @patch('requests.get')
    def test_get_chat_info_api_error(self, mock_get):
        """Тест обработки ошибки API при получении информации о канале"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": False,
            "error_code": 400,
            "description": "Bad Request: chat not found"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        chat_info = self.connector._get_chat_info()
        
        assert chat_info is None
    
    @patch('requests.get')
    def test_get_chat_info_http_error(self, mock_get):
        """Тест обработки HTTP ошибки"""
        mock_get.side_effect = requests.RequestException("Network error")
        
        chat_info = self.connector._get_chat_info()
        
        assert chat_info is None
    
    def test_convert_to_telegram_message_success(self):
        """Тест успешной конвертации сообщения"""
        msg_data = {
            "message_id": 100,
            "text": "Новый AI продукт для автоматизации",
            "date": 1704283200,  # 2024-01-03 12:00:00 UTC
            "photo": [
                {"file_id": "photo1", "width": 100, "height": 100},
                {"file_id": "photo2", "width": 800, "height": 600}
            ]
        }
        
        message = self.connector._convert_to_telegram_message(msg_data)
        
        assert message is not None
        assert message.message_id == 100
        assert message.text == "Новый AI продукт для автоматизации"
        assert "2024-01-03T12:00:00+00:00" in message.date
        assert len(message.media_files) == 1
        assert "photo_photo2" in message.media_files  # Должно взять фото большего размера
    
    def test_convert_to_telegram_message_with_caption(self):
        """Тест конвертации сообщения с caption вместо text"""
        msg_data = {
            "message_id": 101,
            "caption": "Описание к изображению продукта",
            "date": 1704283200,
            "document": {"file_id": "doc123", "file_name": "product.pdf"}
        }
        
        message = self.connector._convert_to_telegram_message(msg_data)
        
        assert message is not None
        assert message.text == "Описание к изображению продукта"
        assert "document_doc123" in message.media_files
    
    def test_convert_to_telegram_message_incomplete_data(self):
        """Тест обработки неполных данных сообщения"""
        # Сообщение без text и caption
        msg_data = {
            "message_id": 102,
            "date": 1704283200
        }
        
        message = self.connector._convert_to_telegram_message(msg_data)
        assert message is None
        
        # Сообщение без message_id
        msg_data = {
            "text": "Текст есть",
            "date": 1704283200
        }
        
        message = self.connector._convert_to_telegram_message(msg_data)
        assert message is None
    
    def test_extract_media_files_all_types(self):
        """Тест извлечения всех типов медиа файлов"""
        msg_data = {
            "photo": [{"file_id": "photo123", "width": 800, "height": 600}],
            "document": {"file_id": "doc456"},
            "video": {"file_id": "video789"}
        }
        
        media_files = self.connector._extract_media_files(msg_data)
        
        assert len(media_files) == 3
        assert "photo_photo123" in media_files
        assert "document_doc456" in media_files
        assert "video_video789" in media_files
    
    def test_extract_media_files_empty(self):
        """Тест извлечения медиа из сообщения без файлов"""
        msg_data = {"text": "Просто текст"}
        
        media_files = self.connector._extract_media_files(msg_data)
        
        assert media_files == []
    
    @patch('requests.get')
    def test_test_connection_success(self, mock_get):
        """Тест успешной проверки соединения"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": True,
            "result": {
                "id": 123456789,
                "username": "test_bot",
                "first_name": "Test Bot"
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = self.connector.test_connection()
        
        assert result is True
        mock_get.assert_called_once()
        assert "getMe" in mock_get.call_args[0][0]
    
    @patch('requests.get')
    def test_test_connection_failure(self, mock_get):
        """Тест неудачной проверки соединения"""
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        result = self.connector.test_connection()
        
        assert result is False
    
    @patch.object(TelegramConnector, '_get_chat_info')
    @patch.object(TelegramConnector, '_get_chat_history')
    def test_fetch_recent_messages_success(self, mock_get_history, mock_get_chat):
        """Тест успешного получения последних сообщений"""
        # Мокируем информацию о канале
        mock_get_chat.return_value = {"id": -1001234567890}
        
        # Мокируем историю сообщений
        mock_get_history.return_value = [
            {
                "message_id": 100,
                "text": "Первое сообщение",
                "date": 1704283200
            },
            {
                "message_id": 101,
                "text": "Второе сообщение",
                "date": 1704283260
            }
        ]
        
        messages = self.connector.fetch_recent_messages(limit=2)
        
        assert len(messages) == 2
        assert messages[0].message_id == 100
        assert messages[1].message_id == 101
        
        mock_get_chat.assert_called_once()
        mock_get_history.assert_called_once_with(-1001234567890, 2, 0)
    
    @patch.object(TelegramConnector, '_get_chat_info')
    def test_fetch_recent_messages_no_chat_info(self, mock_get_chat):
        """Тест обработки ошибки получения информации о канале"""
        mock_get_chat.return_value = None
        
        messages = self.connector.fetch_recent_messages()
        
        assert messages == []
    
    @patch.object(TelegramConnector, 'fetch_recent_messages')
    def test_fetch_new_messages_since_last(self, mock_fetch):
        """Тест получения новых сообщений с момента последней проверки"""
        # Устанавливаем последний обработанный message_id
        self.connector.last_message_id = 100
        
        # Мокируем сообщения, включая старые и новые
        from src.backend.services.telegram_product_generator import TelegramMessage
        mock_messages = [
            TelegramMessage(99, "Старое сообщение", "2024-01-01T10:00:00Z"),
            TelegramMessage(100, "Уже обработанное", "2024-01-01T11:00:00Z"),
            TelegramMessage(101, "Новое сообщение 1", "2024-01-01T12:00:00Z"),
            TelegramMessage(102, "Новое сообщение 2", "2024-01-01T13:00:00Z")
        ]
        mock_fetch.return_value = mock_messages
        
        new_messages = self.connector.fetch_new_messages_since_last()
        
        # Должно вернуть только новые сообщения
        assert len(new_messages) == 2
        assert new_messages[0].message_id == 101
        assert new_messages[1].message_id == 102
        
        # Должно обновить last_message_id
        assert self.connector.last_message_id == 102


class TestTelegramMonitor:
    """Тесты для TelegramMonitor"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        self.mock_connector = Mock()
        self.mock_generator = Mock()
        
        self.monitor = TelegramMonitor(
            connector=self.mock_connector,
            product_generator=self.mock_generator,
            check_interval=1  # Короткий интервал для тестов
        )
    
    def test_monitor_initialization(self):
        """Тест инициализации монитора"""
        assert self.monitor.connector == self.mock_connector
        assert self.monitor.product_generator == self.mock_generator
        assert self.monitor.check_interval == 1
        assert self.monitor.is_running is False
    
    @patch('time.sleep')
    def test_start_monitoring_with_new_messages(self, mock_sleep):
        """Тест мониторинга с новыми сообщениями"""
        from src.backend.services.telegram_product_generator import TelegramMessage
        
        # Настраиваем моки
        new_messages = [
            TelegramMessage(101, "Новый продукт 1", "2024-01-01T12:00:00Z"),
            TelegramMessage(102, "Новый продукт 2", "2024-01-01T13:00:00Z")
        ]
        
        self.mock_connector.fetch_new_messages_since_last.side_effect = [
            new_messages,  # Первый вызов - есть новые сообщения
            [],           # Второй вызов - нет новых сообщений
            KeyboardInterrupt()  # Третий вызов - прерывание
        ]
        
        self.mock_generator.process_batch_messages.return_value = {
            "successful": 2,
            "failed": 0,
            "products": [
                {"product_id": "prod1", "product_name": "Продукт 1", "message_id": 101},
                {"product_id": "prod2", "product_name": "Продукт 2", "message_id": 102}
            ]
        }
        
        # Имитируем KeyboardInterrupt для завершения цикла
        mock_sleep.side_effect = [None, None, KeyboardInterrupt()]
        
        # Запускаем мониторинг
        self.monitor.start_monitoring()
        
        # Проверяем что методы были вызваны
        assert self.mock_connector.fetch_new_messages_since_last.call_count >= 1
        self.mock_generator.process_batch_messages.assert_called_once_with(new_messages)
    
    def test_stop_monitoring(self):
        """Тест остановки мониторинга"""
        self.monitor.is_running = True
        
        self.monitor.stop_monitoring()
        
        assert self.monitor.is_running is False
