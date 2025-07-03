"""
Сервис для мониторинга Telegram канала и извлечения информации о продуктах
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class TelegramChannelMonitor:
    """Мониторинг публичного Telegram канала"""
    
    def __init__(self, channel_username: str = "aideaxondemos"):
        self.channel_username = channel_username
        self.base_url = "https://api.telegram.org/bot"
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.last_message_id = 0
        
    async def get_channel_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получает последние сообщения из канала"""
        if not self.bot_token:
            logger.warning("TELEGRAM_BOT_TOKEN не установлен")
            return []
            
        url = f"{self.base_url}{self.bot_token}/getUpdates"
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'offset': self.last_message_id + 1,
                    'limit': limit,
                    'timeout': 10
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('ok'):
                            updates = data.get('result', [])
                            messages = []
                            
                            for update in updates:
                                if 'channel_post' in update:
                                    message = update['channel_post']
                                    
                                    # Проверяем что сообщение из нужного канала
                                    chat = message.get('chat', {})
                                    if chat.get('username') == self.channel_username:
                                        messages.append(message)
                                        self.last_message_id = max(self.last_message_id, update['update_id'])
                            
                            return messages
                        else:
                            logger.error(f"Ошибка Telegram API: {data.get('description')}")
                            return []
                    else:
                        logger.error(f"HTTP ошибка: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Ошибка получения сообщений: {str(e)}")
            return []
    
    async def get_channel_info_web(self) -> List[Dict[str, Any]]:
        """Получает информацию о канале через веб-интерфейс (fallback метод)"""
        try:
            # Используем публичный API для получения информации о канале
            url = f"https://t.me/s/{self.channel_username}"
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        # Здесь можно добавить парсинг HTML для извлечения сообщений
                        # Но это более сложный подход, требующий HTML-парсера
                        logger.info("Получен HTML канала для дальнейшего парсинга")
                        return []
                    else:
                        logger.error(f"Не удалось получить страницу канала: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Ошибка получения информации о канале: {str(e)}")
            return []
    
    def extract_product_info(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Извлекает информацию о продукте из сообщения"""
        text = message.get('text', '')
        
        if not text or len(text.strip()) < 50:  # Слишком короткое сообщение
            return None
        
        # Извлекаем медиа (фото)
        photos = []
        if 'photo' in message:
            photo = message['photo']
            if isinstance(photo, list) and photo:
                # Берем фото с наибольшим разрешением
                largest_photo = max(photo, key=lambda p: p.get('width', 0) * p.get('height', 0))
                photos.append({
                    'file_id': largest_photo.get('file_id'),
                    'width': largest_photo.get('width'),
                    'height': largest_photo.get('height')
                })
        
        return {
            'message_id': message.get('message_id'),
            'date': message.get('date'),
            'text': text,
            'photos': photos,
            'raw_message': message
        }


class ProductGeneratorFromTelegram:
    """Генератор YAML конфигураций продуктов из Telegram сообщений"""
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.products_dir = Path(__file__).parent.parent.parent.parent / "content" / "products"
    
    def create_product_generation_prompt(self, message_text: str, has_photos: bool = False) -> str:
        """Создает промпт для генерации YAML конфигурации продукта"""
        
        prompt = f"""
Анализируй следующее описание продукта из Telegram канала и создай YAML конфигурацию продукта по нашей стандартной структуре.

ОПИСАНИЕ ПРОДУКТА:
{message_text}

{'ПРИМЕЧАНИЕ: К сообщению прикреплены изображения.' if has_photos else ''}

ТРЕБОВАНИЯ К ГЕНЕРАЦИИ:

1. Создай уникальный product_id (латинские буквы, цифры, подчеркивания)
2. Определи название продукта на русском языке
3. Напиши краткое описание (1-2 предложения)
4. Определи категорию: "analytics", "legal", "automation", "ai", "other"
5. Статус всегда "active"

6. В demo_data включи:
   - key_features (3-5 ключевых функций)
   - supported_formats (если применимо)
   - target_users (целевая аудитория)

7. В product_info добавь:
   - key_benefits (5-7 преимуществ)
   - target_audience (5-7 типов пользователей)
   - use_cases (5-7 сценариев использования)
   - demo_available: true
   - pricing с тремя уровнями

8. В interfaces опиши:
   - input: ожидаемые входные данные
   - output: формат выходных данных

9. В seo добавь:
   - keywords (15-20 релевантных ключевых слов)
   - demo_content с примерами

10. В demo_examples создай:
    - Примеры данных для демонстрации
    - Дефолтные значения

ВАЖНО: 
- Используй только русский язык для текстов
- Делай реалистичные и полезные описания
- Ориентируйся на B2B аудиторию
- Структура должна точно соответствовать нашему формату

ВЕРНИ ТОЛЬКО YAML КОД БЕЗ ДОПОЛНИТЕЛЬНЫХ КОММЕНТАРИЕВ:
"""
        return prompt
    
    async def generate_product_config(self, telegram_message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Генерирует конфигурацию продукта из Telegram сообщения"""
        
        message_text = telegram_message.get('text', '')
        has_photos = len(telegram_message.get('photos', [])) > 0
        
        if not message_text or len(message_text.strip()) < 50:
            logger.warning("Сообщение слишком короткое для создания продукта")
            return None
        
        try:
            # Создаем промпт для LLM
            prompt = self.create_product_generation_prompt(message_text, has_photos)
            
            # Генерируем YAML через LLM
            yaml_content = await self.llm_service.generate_text_async(prompt)
            
            if not yaml_content:
                logger.error("LLM не смог сгенерировать конфигурацию")
                return None
            
            # Очищаем ответ от лишнего текста
            yaml_content = self._clean_yaml_response(yaml_content)
            
            # Парсим YAML для валидации
            import yaml
            try:
                parsed_config = yaml.safe_load(yaml_content)
                
                # Базовая валидация структуры
                required_fields = ['product_id', 'name', 'description']
                for field in required_fields:
                    if field not in parsed_config:
                        logger.error(f"Отсутствует обязательное поле: {field}")
                        return None
                
                return {
                    'config': parsed_config,
                    'yaml_content': yaml_content,
                    'source_message': telegram_message
                }
                
            except yaml.YAMLError as e:
                logger.error(f"Ошибка парсинга YAML: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка генерации конфигурации продукта: {str(e)}")
            return None
    
    def _clean_yaml_response(self, response: str) -> str:
        """Очищает ответ LLM, оставляя только YAML код"""
        lines = response.split('\n')
        yaml_lines = []
        in_yaml = False
        
        for line in lines:
            # Начало YAML (находим строку, начинающуюся с ---)
            if line.strip().startswith('---'):
                in_yaml = True
                yaml_lines.append(line)
                continue
            
            # Если мы внутри YAML и встречаем пустую строку или коментарий
            if in_yaml:
                # Останавливаемся на строках, которые явно не YAML
                if line.strip() and not line.startswith(' ') and not line.startswith('#') and ':' not in line and '-' not in line:
                    break
                yaml_lines.append(line)
        
        return '\n'.join(yaml_lines).strip()
    
    async def save_product_config(self, product_data: Dict[str, Any]) -> bool:
        """Сохраняет конфигурацию продукта в файл"""
        try:
            config = product_data['config']
            yaml_content = product_data['yaml_content']
            product_id = config['product_id']
            
            # Проверяем, что директория существует
            self.products_dir.mkdir(parents=True, exist_ok=True)
            
            # Путь к файлу
            file_path = self.products_dir / f"{product_id}.yaml"
            
            # Проверяем, что файл еще не существует
            if file_path.exists():
                logger.warning(f"Продукт {product_id} уже существует")
                return False
            
            # Сохраняем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            
            logger.info(f"Создан новый продукт: {product_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения конфигурации: {str(e)}")
            return False


class TelegramProductMonitorService:
    """Основной сервис для мониторинга и создания продуктов"""
    
    def __init__(self, llm_service, channel_username: str = "aideaxondemos"):
        self.monitor = TelegramChannelMonitor(channel_username)
        self.generator = ProductGeneratorFromTelegram(llm_service)
        self.processed_messages = set()  # Для избежания дублирования
    
    async def check_new_messages(self) -> List[Dict[str, Any]]:
        """Проверяет новые сообщения и создает продукты"""
        new_products = []
        
        try:
            # Получаем новые сообщения
            messages = await self.monitor.get_channel_messages()
            
            for message in messages:
                message_id = message.get('message_id')
                
                # Пропускаем уже обработанные сообщения
                if message_id in self.processed_messages:
                    continue
                
                # Извлекаем информацию о продукте
                product_info = self.monitor.extract_product_info(message)
                
                if product_info:
                    # Генерируем конфигурацию продукта
                    product_data = await self.generator.generate_product_config(product_info)
                    
                    if product_data:
                        # Сохраняем продукт
                        if await self.generator.save_product_config(product_data):
                            new_products.append(product_data)
                            logger.info(f"Создан новый продукт из сообщения {message_id}")
                        else:
                            logger.warning(f"Не удалось сохранить продукт из сообщения {message_id}")
                    else:
                        logger.warning(f"Не удалось сгенерировать продукт из сообщения {message_id}")
                
                # Отмечаем сообщение как обработанное
                self.processed_messages.add(message_id)
            
            return new_products
            
        except Exception as e:
            logger.error(f"Ошибка проверки новых сообщений: {str(e)}")
            return []
    
    async def run_monitoring_loop(self, interval_seconds: int = 300):
        """Запускает цикл мониторинга канала"""
        logger.info(f"Запуск мониторинга канала @{self.monitor.channel_username}")
        
        while True:
            try:
                new_products = await self.check_new_messages()
                
                if new_products:
                    logger.info(f"Создано продуктов: {len(new_products)}")
                    for product in new_products:
                        product_name = product['config'].get('name', 'Неизвестный')
                        logger.info(f"  - {product_name}")
                
                # Ждем перед следующей проверкой
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Ошибка в цикле мониторинга: {str(e)}")
                await asyncio.sleep(60)  # Ждем минуту при ошибке
