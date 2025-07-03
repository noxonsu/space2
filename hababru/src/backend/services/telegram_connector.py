"""
Коннектор для работы с Telegram API и получения сообщений из канала
"""

import requests
import logging
import time
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from .telegram_product_generator import TelegramMessage


class TelegramConnector:
    """Коннектор для работы с Telegram Bot API"""
    
    def __init__(self, bot_token: str, channel_username: str):
        """
        Инициализация коннектора
        
        Args:
            bot_token: Токен Telegram бота
            channel_username: Имя канала (например, @aideaxondemos)
        """
        self.bot_token = bot_token
        self.channel_username = channel_username.lstrip('@')
        self.api_base_url = f"https://api.telegram.org/bot{bot_token}"
        self.logger = logging.getLogger(__name__)
        
        # Для хранения последнего обработанного сообщения
        self.last_message_id = 0
    
    def fetch_recent_messages(self, limit: int = 10, offset: int = 0) -> List[TelegramMessage]:
        """
        Получает последние сообщения из канала
        
        Args:
            limit: Максимальное количество сообщений
            offset: Смещение для пагинации
            
        Returns:
            Список объектов TelegramMessage
        """
        try:
            # Получаем информацию о канале
            chat_info = self._get_chat_info()
            if not chat_info:
                self.logger.error("Не удалось получить информацию о канале")
                return []
            
            chat_id = chat_info['id']
            
            # Получаем сообщения из канала
            messages = self._get_chat_history(chat_id, limit, offset)
            
            # Конвертируем в объекты TelegramMessage
            telegram_messages = []
            for msg_data in messages:
                message = self._convert_to_telegram_message(msg_data)
                if message:
                    telegram_messages.append(message)
            
            self.logger.info(f"Получено {len(telegram_messages)} сообщений из канала")
            return telegram_messages
            
        except Exception as e:
            self.logger.error(f"Ошибка получения сообщений: {e}")
            return []
    
    def fetch_new_messages_since_last(self) -> List[TelegramMessage]:
        """
        Получает новые сообщения с момента последней проверки
        
        Returns:
            Список новых TelegramMessage
        """
        messages = self.fetch_recent_messages(limit=50)
        
        # Фильтруем только новые сообщения
        new_messages = []
        for message in messages:
            if message.message_id > self.last_message_id:
                new_messages.append(message)
        
        # Обновляем ID последнего сообщения
        if new_messages:
            self.last_message_id = max(msg.message_id for msg in new_messages)
        
        return new_messages
    
    def _get_chat_info(self) -> Optional[Dict[str, Any]]:
        """Получает информацию о канале"""
        try:
            url = f"{self.api_base_url}/getChat"
            params = {"chat_id": f"@{self.channel_username}"}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("ok"):
                return data["result"]
            else:
                self.logger.error(f"Ошибка API Telegram: {data}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Ошибка HTTP запроса к Telegram API: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка получения информации о канале: {e}")
            return None
    
    def _get_chat_history(self, chat_id: int, limit: int, offset: int) -> List[Dict[str, Any]]:
        """
        Получает историю сообщений канала
        
        Примечание: Для публичных каналов Telegram Bot API имеет ограничения.
        В реальной ситуации может потребоваться использование MTProto API или webhook.
        """
        try:
            # Для демонстрации используем getUpdates с offset
            # В продакшене лучше использовать webhook или MTProto
            url = f"{self.api_base_url}/getUpdates"
            params = {
                "offset": offset,
                "limit": limit,
                "timeout": 10
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            if data.get("ok"):
                # Фильтруем только сообщения из нужного канала
                channel_messages = []
                for update in data["result"]:
                    if "channel_post" in update:
                        msg = update["channel_post"]
                        if msg.get("chat", {}).get("username") == self.channel_username:
                            channel_messages.append(msg)
                
                return channel_messages
            else:
                self.logger.error(f"Ошибка API при получении истории: {data}")
                return []
                
        except requests.RequestException as e:
            self.logger.error(f"Ошибка HTTP при получении истории: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Ошибка получения истории сообщений: {e}")
            return []
    
    def _convert_to_telegram_message(self, msg_data: Dict[str, Any]) -> Optional[TelegramMessage]:
        """Конвертирует данные Telegram API в объект TelegramMessage"""
        try:
            message_id = msg_data.get("message_id")
            text = msg_data.get("text", msg_data.get("caption", ""))
            date_timestamp = msg_data.get("date")
            
            if not message_id or not text:
                return None
            
            # Конвертируем timestamp в ISO format
            date_str = datetime.fromtimestamp(date_timestamp, tz=timezone.utc).isoformat()
            
            # Извлекаем медиа файлы
            media_files = self._extract_media_files(msg_data)
            
            return TelegramMessage(
                message_id=message_id,
                text=text,
                date=date_str,
                media_files=media_files
            )
            
        except Exception as e:
            self.logger.error(f"Ошибка конвертации сообщения: {e}")
            return None
    
    def _extract_media_files(self, msg_data: Dict[str, Any]) -> List[str]:
        """Извлекает информацию о медиа файлах из сообщения"""
        media_files = []
        
        try:
            # Проверяем фото
            if "photo" in msg_data:
                # Берем фото наибольшего размера
                photos = msg_data["photo"]
                if photos:
                    largest_photo = max(photos, key=lambda p: p.get("width", 0) * p.get("height", 0))
                    media_files.append(f"photo_{largest_photo['file_id']}")
            
            # Проверяем документы
            if "document" in msg_data:
                doc = msg_data["document"]
                media_files.append(f"document_{doc['file_id']}")
            
            # Проверяем видео
            if "video" in msg_data:
                video = msg_data["video"]
                media_files.append(f"video_{video['file_id']}")
            
            return media_files
            
        except Exception as e:
            self.logger.error(f"Ошибка извлечения медиа файлов: {e}")
            return []
    
    def download_media_file(self, file_id: str, save_path: str) -> bool:
        """
        Скачивает медиа файл по file_id
        
        Args:
            file_id: ID файла в Telegram
            save_path: Путь для сохранения файла
            
        Returns:
            True если файл успешно скачан
        """
        try:
            # Получаем информацию о файле
            file_info_url = f"{self.api_base_url}/getFile"
            params = {"file_id": file_id}
            
            response = requests.get(file_info_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if not data.get("ok"):
                self.logger.error(f"Ошибка получения информации о файле: {data}")
                return False
            
            file_path = data["result"]["file_path"]
            
            # Скачиваем файл
            download_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Файл {file_id} успешно скачан в {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка скачивания файла {file_id}: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Тестирует соединение с Telegram API
        
        Returns:
            True если соединение работает
        """
        try:
            url = f"{self.api_base_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("ok"):
                bot_info = data["result"]
                self.logger.info(f"Соединение с Telegram API успешно. Бот: {bot_info.get('username')}")
                return True
            else:
                self.logger.error(f"Ошибка соединения с Telegram API: {data}")
                return False
                
        except Exception as e:
            self.logger.error(f"Ошибка тестирования соединения: {e}")
            return False


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
    
    def start_monitoring(self):
        """Запускает мониторинг канала"""
        self.is_running = True
        self.logger.info("Запуск мониторинга Telegram канала")
        
        while self.is_running:
            try:
                # Получаем новые сообщения
                new_messages = self.connector.fetch_new_messages_since_last()
                
                if new_messages:
                    self.logger.info(f"Найдено {len(new_messages)} новых сообщений")
                    
                    # Обрабатываем новые сообщения
                    results = self.product_generator.process_batch_messages(new_messages)
                    
                    self.logger.info(f"Обработка завершена: {results['successful']} успешно, {results['failed']} ошибок")
                    
                    # Логируем созданные продукты
                    for product in results['products']:
                        self.logger.info(f"Создан продукт: {product['product_id']} - {product['product_name']}")
                
                # Ждем до следующей проверки
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Получен сигнал прерывания, останавливаем мониторинг")
                break
            except Exception as e:
                self.logger.error(f"Ошибка в цикле мониторинга: {e}")
                time.sleep(60)  # Ждем минуту перед повторной попыткой
    
    def stop_monitoring(self):
        """Останавливает мониторинг"""
        self.is_running = False
        self.logger.info("Мониторинг остановлен")
