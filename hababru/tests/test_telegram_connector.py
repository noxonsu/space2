"""
Тесты для Telegram коннектора
"""

import pytest
import requests
import asyncio
from unittest.mock import Mock, patch, MagicMock
from src.backend.services.telegram_connector import TelegramConnector, TelegramMonitor
from src.backend.services.telegram_product_generator import TelegramMessage


class TestTelegramConnector:
    """Тесты для TelegramConnector"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        # Используем фиктивные, но корректные аргументы для инициализации
        self.api_id = "1234567"
        self.api_hash = "test_api_hash"
        self.phone_number = "+1234567890"
        self.channel_username = "@aideaxondemos"
        self.connector = TelegramConnector(
            api_id=self.api_id,
            api_hash=self.api_hash,
            phone_number=self.phone_number,
            channel_username=self.channel_username
        )
        # Мокируем клиент Pyrogram для всех тестов
        self.connector.client = MagicMock()
        self.connector.client.start = MagicMock(return_value=None)
        self.connector.client.stop = MagicMock(return_value=None)
        self.connector.client.is_connected = True
        self.connector.client.export_session_string = MagicMock(return_value="test_session_string")
        self.connector.client.get_me = MagicMock(return_value=Mock(first_name="Test", username="testuser"))
        self.connector.client.get_chat = MagicMock(return_value=Mock(id=-1001234567890))
        self.connector.channel_id = -1001234567890 # Устанавливаем channel_id для тестов

    @pytest.mark.asyncio
    async def test_connector_initialization(self):
        """Тест инициализации коннектора"""
        assert self.connector.api_id == int(self.api_id)
        assert self.connector.api_hash == self.api_hash
        assert self.connector.phone_number == self.phone_number
        assert self.connector.channel_username == self.channel_username.lstrip('@')
        assert self.connector.last_message_id == 0
        assert self.connector.client is not None

    @pytest.mark.asyncio
    async def test_connector_initialization_with_at_symbol(self):
        """Тест инициализации с @ в имени канала"""
        connector = TelegramConnector(self.api_id, self.api_hash, self.phone_number, channel_username="@testchannel")
        assert connector.channel_username == "testchannel"

    @pytest.mark.asyncio
    async def test_test_connection_success(self):
        """Тест успешной проверки соединения"""
        result = await self.connector.test_connection()
        assert result is True
        self.connector.client.start.assert_called_once()
        self.connector.client.get_me.assert_called_once()
        self.connector.client.get_chat.assert_called_once_with(self.channel_username)
        assert self.connector.session_string == "test_session_string"

    @pytest.mark.asyncio
    async def test_test_connection_failure(self):
        """Тест неудачной проверки соединения"""
        self.connector.client.start.side_effect = Exception("Connection failed")
        result = await self.connector.test_connection()
        assert result is False

    @pytest.mark.asyncio
    async def test_fetch_recent_messages_success(self):
        """Тест успешного получения последних сообщений"""
        mock_message1 = Mock(id=100, text="Первое сообщение", date=datetime.fromtimestamp(1704283200, tz=timezone.utc), photo=None, document=None, video=None, caption=None)
        mock_message2 = Mock(id=101, text="Второе сообщение", date=datetime.fromtimestamp(1704283260, tz=timezone.utc), photo=None, document=None, video=None, caption=None)
        
        # Mocking async for loop
        async def async_iter_messages(*args, **kwargs):
            yield mock_message1
            yield mock_message2

        self.connector.client.get_chat_history.return_value = async_iter_messages()
        
        messages = await self.connector.fetch_recent_messages(limit=2)
        
        assert len(messages) == 2
        assert messages[0].message_id == 100
        assert messages[1].message_id == 101
        self.connector.client.get_chat.assert_called_once_with(self.channel_username)
        self.connector.client.get_chat_history.assert_called_once_with(self.connector.channel_id, limit=2)
        self.connector.client.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_recent_messages_no_chat_info(self):
        """Тест обработки ошибки получения информации о канале"""
        self.connector.client.get_chat.side_effect = Exception("Chat not found")
        messages = await self.connector.fetch_recent_messages()
        assert messages == []

    @pytest.mark.asyncio
    async def test_fetch_new_messages_since_last(self):
        """Тест получения новых сообщений с момента последней проверки"""
        self.connector.last_message_id = 100
        
        mock_message1 = Mock(id=101, text="Новое сообщение 1", date=datetime.fromtimestamp(1704283200, tz=timezone.utc), photo=None, document=None, video=None, caption=None)
        mock_message2 = Mock(id=102, text="Новое сообщение 2", date=datetime.fromtimestamp(1704283260, tz=timezone.utc), photo=None, document=None, video=None, caption=None)
        mock_message_old = Mock(id=99, text="Старое сообщение", date=datetime.fromtimestamp(1704283100, tz=timezone.utc), photo=None, document=None, video=None, caption=None)

        async def async_iter_messages(*args, **kwargs):
            yield mock_message2
            yield mock_message1
            yield mock_message_old # Это сообщение должно быть отфильтровано

        self.connector.client.get_chat_history.return_value = async_iter_messages()
        
        new_messages = await self.connector.fetch_new_messages_since_last()
        
        assert len(new_messages) == 2
        assert new_messages[0].message_id == 101
        assert new_messages[1].message_id == 102
        assert self.connector.last_message_id == 102

    @pytest.mark.asyncio
    async def test_convert_to_telegram_message_success(self):
        """Тест успешной конвертации сообщения"""
        mock_msg = Mock(
            id=100,
            text="Новый AI продукт для автоматизации",
            date=datetime.fromtimestamp(1704283200, tz=timezone.utc),
            photo=Mock(file_id="photo2", width=800, height=600),
            caption=None,
            document=None,
            video=None
        )
        
        message = self.connector._convert_to_telegram_message(mock_msg)
        
        assert message is not None
        assert message.message_id == 100
        assert message.text == "Новый AI продукт для автоматизации"
        assert "2024-01-03T12:00:00+00:00" in message.date
        assert len(message.media_files) == 1
        assert "photo_photo2" in message.media_files

    @pytest.mark.asyncio
    async def test_convert_to_telegram_message_with_caption(self):
        """Тест конвертации сообщения с caption вместо text"""
        mock_msg = Mock(
            id=101,
            text=None,
            caption="Описание к изображению продукта",
            date=datetime.fromtimestamp(1704283200, tz=timezone.utc),
            document=Mock(file_id="doc123", file_name="product.pdf"),
            photo=None,
            video=None
        )
        
        message = self.connector._convert_to_telegram_message(mock_msg)
        
        assert message is not None
        assert message.text == "Описание к изображению продукта"
        assert "document_doc123" in message.media_files

    @pytest.mark.asyncio
    async def test_convert_to_telegram_message_incomplete_data(self):
        """Тест обработки неполных данных сообщения"""
        # Сообщение без text и caption
        mock_msg = Mock(
            id=102,
            text=None,
            caption=None,
            date=datetime.fromtimestamp(1704283200, tz=timezone.utc),
            photo=None, document=None, video=None
        )
        message = self.connector._convert_to_telegram_message(mock_msg)
        assert message is None
        
        # Сообщение без message_id
        mock_msg_no_id = Mock(
            id=None,
            text="Текст есть",
            date=datetime.fromtimestamp(1704283200, tz=timezone.utc),
            photo=None, document=None, video=None
        )
        message = self.connector._convert_to_telegram_message(mock_msg_no_id)
        assert message is None

    @pytest.mark.asyncio
    async def test_extract_media_files_all_types(self):
        """Тест извлечения всех типов медиа файлов"""
        mock_msg = Mock(
            photo=Mock(file_id="photo123", width=800, height=600),
            document=Mock(file_id="doc456"),
            video=Mock(file_id="video789")
        )
        
        media_files = self.connector._extract_media_files(mock_msg)
        
        assert len(media_files) == 3
        assert "photo_photo123" in media_files
        assert "document_doc456" in media_files
        assert "video_video789" in media_files

    @pytest.mark.asyncio
    async def test_extract_media_files_empty(self):
        """Тест извлечения медиа из сообщения без файлов"""
        mock_msg = Mock(text="Просто текст", photo=None, document=None, video=None)
        
        media_files = self.connector._extract_media_files(mock_msg)
        
        assert media_files == []


class TestTelegramMonitor:
    """Тесты для TelegramMonitor"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        self.mock_connector = MagicMock(spec=TelegramConnector)
        self.mock_generator = Mock()
        
        self.monitor = TelegramMonitor(
            connector=self.mock_connector,
            product_generator=self.mock_generator,
            check_interval=0.1  # Короткий интервал для тестов
        )
        # Мокируем цикл событий для тестов
        self.monitor.loop = asyncio.get_event_loop()
    
    def test_monitor_initialization(self):
        """Тест инициализации монитора"""
        assert self.monitor.connector == self.mock_connector
        assert self.monitor.product_generator == self.mock_generator
        assert self.monitor.check_interval == 0.1
        assert self.monitor.is_running is False
    
    @pytest.mark.asyncio
    async def test_start_monitoring_with_new_messages(self):
        """Тест мониторинга с новыми сообщениями"""
        new_messages = [
            TelegramMessage(101, "Новый продукт 1", "2024-01-01T12:00:00Z"),
            TelegramMessage(102, "Новый продукт 2", "2024-01-01T13:00:00Z")
        ]
        
        # Настраиваем моки для асинхронных вызовов
        self.mock_connector.fetch_new_messages_since_last.side_effect = [
            new_messages,  # Первый вызов - есть новые сообщения
            [],           # Второй вызов - нет новых сообщений
            asyncio.CancelledError # Третий вызов - прерывание для завершения цикла
        ]
        
        self.mock_generator.process_batch_messages_async.return_value = {
            "successful": 2,
            "failed": 0,
            "products": [
                {"product_id": "prod1", "product_name": "Продукт 1", "message_id": 101},
                {"product_id": "prod2", "product_name": "Продукт 2", "message_id": 102}
            ]
        }
        
        # Запускаем мониторинг
        await self.monitor._monitor_loop() # Вызываем напрямую асинхронный метод
        
        # Проверяем что методы были вызваны
        assert self.mock_connector.fetch_new_messages_since_last.call_count == 3
        self.mock_generator.process_batch_messages_async.assert_called_once_with(new_messages)
    
    def test_stop_monitoring(self):
        """Тест остановки мониторинга"""
        self.monitor.is_running = True
        
        # Мокируем asyncio.all_tasks
        mock_task = Mock()
        mock_task.cancel = Mock()
        with patch('asyncio.all_tasks', return_value=[mock_task]):
            self.monitor.stop_monitoring()
        
        assert self.monitor.is_running is False
        mock_task.cancel.assert_called_once()
