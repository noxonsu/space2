"""
Коннектор для работы с Telegram API и получения сообщений из канала
"""

import logging
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pyrogram import Client, enums
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeExpired, FloodWait, AuthKeyUnregistered

from .telegram_product_generator import TelegramMessage


class TelegramConnector:
    """Коннектор для работы с Telegram MTProto API (пользовательский аккаунт)"""

    def __init__(self, api_id: str, api_hash: str, phone_number: str, session_string: Optional[str] = None, channel_username: str = '@aideaxondemos'):
        """
        Инициализация коннектора
        
        Args:
            api_id: Telegram API ID
            api_hash: Telegram API Hash
            phone_number: Номер телефона для авторизации (с кодом страны)
            session_string: Строка сессии Pyrogram (для повторного использования)
            channel_username: Имя канала (например, @aideaxondemos)
        """
        self.api_id = int(api_id)
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_string = session_string
        self.channel_username = channel_username.lstrip('@')
        self.logger = logging.getLogger(__name__)
        self.client: Optional[Client] = None
        self.channel_id: Optional[int] = None

        # Для хранения последнего обработанного сообщения
        self.last_message_id = 0

    async def _initialize_client(self):
        """Инициализирует Pyrogram клиент"""
        if self.client is None:
            self.client = Client(
                name="hababru_session",
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number,
                session_string=self.session_string,
                workdir="." # Рабочая директория для файлов сессии
            )
            self.logger.info("Pyrogram Client initialized.")
        else:
            self.logger.info("Pyrogram Client already initialized.")

    async def test_connection(self) -> bool:
        """
        Тестирует соединение с Telegram API и авторизуется при необходимости.
        
        Returns:
            True если соединение работает и авторизация успешна
        """
        await self._initialize_client()
        try:
            self.logger.info("Попытка запуска Pyrogram клиента...")
            await self.client.start()
            self.logger.info("✓ Pyrogram клиент запущен.")

            # Если сессия новая, получаем и сохраняем session_string
            if not self.session_string:
                new_session_string = await self.client.export_session_string()
                self.session_string = new_session_string
                self.logger.info(f"Новая строка сессии получена. Сохраните ее в .env: TELEGRAM_SESSION_STRING='{new_session_string}'")
            
            # Получаем информацию о себе
            me = await self.client.get_me()
            self.logger.info(f"Авторизован как: {me.first_name} (@{me.username})")

            # Получаем ID канала
            try:
                chat = await self.client.get_chat(self.channel_username)
                self.channel_id = chat.id
                self.logger.info(f"ID канала '{self.channel_username}': {self.channel_id}")
            except Exception as e:
                self.logger.error(f"Не удалось получить информацию о канале '{self.channel_username}': {e}")
                return False

            return True
        except SessionPasswordNeeded:
            self.logger.error("Требуется двухфакторная аутентификация. Пожалуйста, введите пароль.")
            # Здесь можно добавить логику для запроса пароля у пользователя
            return False
        except PhoneCodeExpired:
            self.logger.error("Код подтверждения истек. Пожалуйста, перезапустите скрипт для получения нового кода.")
            return False
        except FloodWait as e:
            self.logger.error(f"Слишком много запросов к Telegram API. Пожалуйста, подождите {e.value} секунд.")
            await asyncio.sleep(e.value + 5) # Ждем немного дольше
            return False
        except AuthKeyUnregistered:
            self.logger.error("Ключ авторизации недействителен. Возможно, сессия была отозвана или удалена. Пожалуйста, удалите TELEGRAM_SESSION_STRING из .env и перезапустите.")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка тестирования соединения: {e}")
            return False
        # НЕ закрываем клиент здесь

    async def fetch_recent_messages(self, limit: int = 10, offset: int = 0) -> List[TelegramMessage]:
        """
        Получает последние сообщения из канала
        
        Args:
            limit: Максимальное количество сообщений
            offset: Смещение для пагинации (в Pyrogram это skip)
            
        Returns:
            Список объектов TelegramMessage
        """
        if self.client is None or not self.client.is_connected:
            await self._initialize_client()
            await self.client.start()
            self.logger.info("Pyrogram клиент запущен для получения сообщений.")

        if self.channel_id is None:
            try:
                chat = await self.client.get_chat(self.channel_username)
                self.channel_id = chat.id
            except Exception as e:
                self.logger.error(f"Не удалось получить ID канала '{self.channel_username}': {e}")
                return []

        telegram_messages = []
        try:
            # Pyrogram не имеет прямого "offset" для get_chat_history,
            # но можно использовать offset_id или просто итерировать
            # Для "всей истории" лучше использовать iter_messages
            
            # Если offset используется как количество пропущенных сообщений
            # то нужно итерировать и пропускать
            
            # Для простоты, если нужен offset, будем использовать get_messages с offset
            # Если offset не 0, то это не "последние N", а "N сообщений после offset"
            # Для массовой генерации лучше использовать iter_messages без offset
            
            if offset > 0:
                # Если нужен конкретный offset, то это сложнее с iter_messages
                # Проще получить все и обрезать, или использовать offset_id
                # Для данной задачи, где нужно "всю историю", будем использовать iter_messages
                self.logger.warning("Параметр 'offset' не поддерживается напрямую для 'fetch_recent_messages' в Pyrogram. Будут получены последние сообщения.")
            
            count = 0
            async for message in self.client.get_chat_history(self.channel_id, limit=limit):
                if message.text or message.caption: # Только сообщения с текстом или подписью
                    msg = self._convert_to_telegram_message(message)
                    if msg:
                        telegram_messages.append(msg)
                        count += 1
                        if count >= limit:
                            break
            
            self.logger.info(f"Получено {len(telegram_messages)} сообщений из канала '{self.channel_username}'")
            return telegram_messages
            
        except FloodWait as e:
            self.logger.warning(f"Слишком много запросов к Telegram API. Ожидание {e.value} секунд.")
            await asyncio.sleep(e.value + 5)
            return await self.fetch_recent_messages(limit, offset) # Повторная попытка
        except Exception as e:
            self.logger.error(f"Ошибка получения сообщений из канала '{self.channel_username}': {e}")
            return []
        finally:
            if self.client and self.client.is_connected:
                await self.client.stop()
                self.logger.info("Pyrogram клиент остановлен после получения сообщений.")

    async def fetch_all_messages(self) -> List[TelegramMessage]:
        """
        Получает все сообщения из канала.
        Используется для массовой генерации.
        """
        if self.client is None or not self.client.is_connected:
            await self._initialize_client()
            await self.client.start()
            self.logger.info("Pyrogram клиент запущен для получения всех сообщений.")

        if self.channel_id is None:
            try:
                chat = await self.client.get_chat(self.channel_username)
                self.channel_id = chat.id
            except Exception as e:
                self.logger.error(f"Не удалось получить ID канала '{self.channel_username}': {e}")
                return []

        all_messages = []
        try:
            self.logger.info(f"Начинаем получать ВСЮ историю сообщений из канала '{self.channel_username}'...")
            async for message in self.client.get_chat_history(self.channel_id):
                if message.text or message.caption:
                    msg = self._convert_to_telegram_message(message)
                    if msg:
                        all_messages.append(msg)
            self.logger.info(f"Получено {len(all_messages)} сообщений из канала '{self.channel_username}'")
            return all_messages
        except FloodWait as e:
            self.logger.warning(f"Слишком много запросов к Telegram API. Ожидание {e.value} секунд.")
            await asyncio.sleep(e.value + 5)
            return await self.fetch_all_messages() # Повторная попытка
        except Exception as e:
            self.logger.error(f"Ошибка получения всех сообщений из канала '{self.channel_username}': {e}")
            return []
        # НЕ закрываем клиент здесь, он будет закрыт в контексте CLI

    def _convert_to_telegram_message(self, msg: Any) -> Optional[TelegramMessage]:
        """Конвертирует объект сообщения Pyrogram в объект TelegramMessage"""
        try:
            message_id = msg.id
            text = msg.text if msg.text else msg.caption if msg.caption else ""
            date_str = msg.date.isoformat() if msg.date else datetime.now(timezone.utc).isoformat()
            
            if not message_id:
                return None
            
            media_files = []
            if msg.photo:
                media_files.append(f"photo_{msg.photo.file_id}")
            elif msg.document:
                media_files.append(f"document_{msg.document.file_id}")
            elif msg.video:
                media_files.append(f"video_{msg.video.file_id}")
            # Добавьте другие типы медиа по необходимости

            return TelegramMessage(
                message_id=message_id,
                text=text,
                date=date_str,
                media_files=media_files
            )
            
        except Exception as e:
            self.logger.error(f"Ошибка конвертации сообщения Pyrogram: {e}")
            return None
    
    async def download_media_file(self, file_id: str, save_path: str) -> bool:
        """
        Скачивает медиа файл по file_id
        
        Args:
            file_id: ID файла в Telegram (например, photo_FILE_ID)
            save_path: Путь для сохранения файла
            
        Returns:
            True если файл успешно скачан
        """
        if self.client is None or not self.client.is_connected:
            self.logger.error("Pyrogram клиент не запущен для скачивания файла.")
            return False

        try:
            # Pyrogram download_media принимает объект Message или file_id
            # Если file_id содержит префикс, извлекаем его
            actual_file_id = file_id.split('_', 1)[-1]
            
            # Для скачивания по file_id нужно получить объект File
            # Это не всегда прямолинейно, проще, если у нас есть сам объект Message
            # Для простоты, если у нас есть только file_id, мы можем попробовать
            # найти сообщение, содержащее этот файл, или использовать get_file
            
            # Pyrogram download_media может принимать file_id напрямую
            downloaded_file_path = await self.client.download_media(actual_file_id, file_name=save_path)
            
            if downloaded_file_path:
                self.logger.info(f"Файл {file_id} успешно скачан в {downloaded_file_path}")
                return True
            else:
                self.logger.error(f"Не удалось скачать файл {file_id}")
                return False
            
        except Exception as e:
            self.logger.error(f"Ошибка скачивания файла {file_id}: {e}")
            return False

    async def close(self):
        """Закрывает соединение с Telegram"""
        if self.client and self.client.is_connected:
            await self.client.stop()
            self.logger.info("Pyrogram клиент остановлен.")


class TelegramMonitor:
    """Монитор для непрерывного отслеживания новых сообщений"""
    
    def __init__(self, connector: TelegramConnector, product_generator, check_interval: int = 300):
        """
        Инициализация монитора
        
        Args:
            connector: Экземпляр TelegramConnector
            product_generator: Экземпляр TelegramProductGenerator
            check_interval: Интервал проверки в секундах (по умолчанию 5 минут)
        """
        self.connector = connector
        self.product_generator = product_generator
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.loop = asyncio.get_event_loop() # Получаем текущий цикл событий

    def start_monitoring(self):
        """Запускает мониторинг канала"""
        self.is_running = True
        self.logger.info("Запуск мониторинга Telegram канала")
        
        # Запускаем асинхронную функцию в цикле событий
        self.loop.run_until_complete(self._monitor_loop())
    
    async def _monitor_loop(self):
        """Асинхронный цикл мониторинга"""
        while self.is_running:
            try:
                # Получаем новые сообщения
                new_messages = await self.connector.fetch_new_messages_since_last()
                
                if new_messages:
                    self.logger.info(f"Найдено {len(new_messages)} новых сообщений")
                    
                    # Обрабатываем новые сообщения
                    results = await self.product_generator.process_batch_messages_async(new_messages)
                    
                    self.logger.info(f"Обработка завершена: {results['successful']} успешно, {results['failed']} ошибок")
                    
                    # Логируем созданные продукты
                    for product in results['products']:
                        self.logger.info(f"Создан продукт: {product['product_id']} - {product['product_name']}")
                
                # Ждем до следующей проверки
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                self.logger.info("Мониторинг отменен.")
                break
            except Exception as e:
                self.logger.error(f"Ошибка в цикле мониторинга: {e}")
                await asyncio.sleep(60)  # Ждем минуту перед повторной попыткой
    
    def stop_monitoring(self):
        """Останавливает мониторинг"""
        self.is_running = False
        # Завершаем асинхронные задачи
        for task in asyncio.all_tasks(self.loop):
            task.cancel()
        self.logger.info("Мониторинг остановлен")
