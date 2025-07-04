"""
Сервис для генерации продуктов из Telegram сообщений канала @aideaxondemos
"""

import os
import re
import yaml
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from .llm_service import LLMService


@dataclass
class TelegramMessage:
    """Класс для представления Telegram сообщения"""
    message_id: int
    text: str
    date: str
    media_files: List[str] = None
    
    def __post_init__(self):
        if self.media_files is None:
            self.media_files = []


class TelegramProductGenerator:
    """Генератор продуктов из Telegram сообщений"""
    
    def __init__(self, llm_service: LLMService, products_dir: str = None):
        self.llm_service = llm_service
        
        if products_dir is None:
            # Определяем путь к директории products относительно этого файла
            current_dir = Path(__file__).parent
            self.products_dir = current_dir.parent.parent.parent / "content" / "products"
        else:
            self.products_dir = Path(products_dir)
        
        # Создаем директорию если она не существует
        self.products_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
    
    def generate_product_from_message(self, message: TelegramMessage) -> Dict[str, Any]:
        """
        Генерирует конфигурацию продукта из Telegram сообщения
        
        Args:
            message: Объект TelegramMessage с данными сообщения
            
        Returns:
            Dict с результатом генерации: success, product_id, file_path или error
        """
        try:
            self.logger.info(f"Генерируем продукт из сообщения {message.message_id}")
            
            # Проверяем на семантические дубли
            duplicate_id = self._check_semantic_duplicate(message)
            if duplicate_id:
                return {
                    "success": False,
                    "error": f"Продукт с похожим смыслом уже существует: {duplicate_id}",
                    "duplicate_product_id": duplicate_id,
                    "message_id": message.message_id
                }
            
            # Создаем промпт для LLM
            prompt = self._create_product_generation_prompt(message)
            
            # Отправляем запрос к LLM
            llm_response = self.llm_service.generate_text(prompt)
            
            if not llm_response:
                return {
                    "success": False,
                    "error": "LLM не вернул ответ для генерации продукта"
                }
            
            # Парсим YAML из ответа LLM
            product_data = self._parse_yaml_from_llm_response(llm_response)
            
            if not product_data:
                return {
                    "success": False,
                    "error": "Не удалось выполнить парсинг YAML из ответа LLM"
                }
            
            # Валидируем данные продукта
            if not self._validate_product_data(product_data):
                return {
                    "success": False,
                    "error": "Сгенерированные данные продукта не прошли валидацию"
                }
            
            # Сохраняем конфигурацию продукта
            file_path = self._save_product_config(product_data)
            
            self.logger.info(f"Продукт успешно создан: {product_data['product_id']}")
            
            return {
                "success": True,
                "product_id": product_data["product_id"],
                "product_name": product_data["name"],
                "file_path": str(file_path),
                "message_id": message.message_id
            }
            
        except Exception as e:
            self.logger.error(f"Ошибка генерации продукта: {str(e)}")
            return {
                "success": False,
                "error": f"Ошибка генерации продукта: {str(e)}"
            }
    
    def _create_product_generation_prompt(self, message: TelegramMessage) -> str:
        """Создает промпт для LLM на основе Telegram сообщения"""
        
        # Получаем список существующих продуктов для избежания дублирования
        existing_products = self._get_existing_products()
        
        prompt = f"""
Ты - эксперт по созданию конфигураций продуктов для B2B платформы HababRu.

ЗАДАЧА: На основе описания продукта из Telegram канала создай YAML конфигурацию нового продукта.

ВХОДНЫЕ ДАННЫЕ:
Текст сообщения: "{message.text}"
Дата: {message.date}
Медиа файлы: {', '.join(message.media_files) if message.media_files else 'отсутствуют'}

СУЩЕСТВУЮЩИЕ ПРОДУКТЫ (избегай дублирования):
{', '.join(existing_products)}

ТРЕБОВАНИЯ К СТРУКТУРЕ YAML:

```yaml
---
# Метаданные продукта
product_id: "уникальный_id_латиницей_без_пробелов"
name: "Читаемое название продукта"
description: "Краткое описание продукта в 1-2 предложениях"
version: "1.0"
category: "категория" # ai, analytics, automation, legal, finance, marketing
status: "active"

# Демо-данные
demo_data:
  key_features:
    - "Основная функция 1"
    - "Основная функция 2"
    - "Основная функция 3"
  
  supported_formats: # если применимо
    - "PDF"
    - "DOC"
  
  processing_time: "время обработки" # если применимо
  accuracy: "точность в %" # если применимо

# Информация о продукте для SEO
product_info:
  key_benefits:
    - "Польза 1 с конкретными цифрами"
    - "Польза 2"
    - "Польза 3"

  target_audience:
    - "Целевая аудитория 1"
    - "Целевая аудитория 2"
    - "Целевая аудитория 3"

  use_cases:
    - "Сценарий использования 1"
    - "Сценарий использования 2"
    - "Сценарий использования 3"

  demo_available: true
  screenshots: []
  
  pricing:
    basic: "Базовый тариф описание"
    professional: "Профессиональный тариф описание"
    enterprise: "Корпоративный тариф описание"

# Интерфейсы ввода/вывода (адаптируй под тип продукта)
interfaces:
  input:
    type: "object"
    properties:
      input_field:
        type: "string"
        description: "Описание входных данных"
        example: "Пример входных данных"
    required:
      - "input_field"

  output:
    type: "object"
    properties:
      output_field:
        type: "string"
        description: "Описание выходных данных"
        example: "Пример результата"

# SEO данные
seo:
  keywords:
    - "ключевое слово 1"
    - "ключевое слово 2"
    - "ключевое слово 3"
    # минимум 10-15 ключевых слов

  demo_content:
    demo_queries: # примеры запросов для демо
      - "пример запроса 1"
      - "пример запроса 2"
    
    sample_results: # примеры результатов
      metric1: "значение"
      metric2: "значение"

# Демо-примеры
demo_examples:
  sample_data: # примеры данных для демонстрации
    - example: "пример 1"
      result: "результат 1"
```

ИНСТРУКЦИИ:
1. Анализируй текст сообщения и выдели ключевую информацию о продукте
2. Определи категорию продукта (ai, analytics, automation, legal, finance, marketing)
3. Создай уникальный product_id (проверь что его нет в существующих)
4. Заполни все секции релевантной информацией
5. Сгенерируй SEO ключевые слова на русском языке
6. Если в сообщении есть эмодзи или особое форматирование, учти это при создании названия
7. Верни ТОЛЬКО YAML без дополнительных комментариев

Начинай с --- и заканчивай корректным YAML форматом.
"""
        
        return prompt
    
    def _parse_yaml_from_llm_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Извлекает и парсит YAML из ответа LLM"""
        try:
            # Ищем YAML блок в markdown
            yaml_match = re.search(r'```yaml\n(.*?)\n```', response, re.DOTALL)
            if yaml_match:
                yaml_content = yaml_match.group(1)
            else:
                # Ищем YAML начинающийся с ---
                yaml_match = re.search(r'---(.*)', response, re.DOTALL)
                if yaml_match:
                    yaml_content = "---" + yaml_match.group(1)
                else:
                    # Пробуем парсить весь ответ как YAML
                    yaml_content = response.strip()
            
            # Парсим YAML
            product_data = yaml.safe_load(yaml_content)
            
            # Проверяем что это действительно словарь (валидный YAML объект)
            if not isinstance(product_data, dict):
                self.logger.error(f"YAML не является объектом: {type(product_data)}")
                return None
                
            return product_data
            
        except yaml.YAMLError as e:
            self.logger.error(f"Ошибка парсинга YAML: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка извлечения YAML из ответа: {e}")
            return None
    
    def _validate_product_data(self, data: Dict[str, Any]) -> bool:
        """Валидирует структуру данных продукта"""
        required_fields = [
            'product_id', 'name', 'description', 'category',
            'demo_data', 'product_info', 'seo'
        ]
        
        try:
            # Проверяем обязательные поля верхнего уровня
            for field in required_fields:
                if field not in data:
                    self.logger.error(f"Отсутствует обязательное поле: {field}")
                    return False
            
            # Проверяем product_id на уникальность и формат
            product_id = data['product_id']
            if not re.match(r'^[a-z0-9_]+$', product_id):
                self.logger.error(f"Неверный формат product_id: {product_id}")
                return False
            
            # Проверяем что продукт с таким ID еще не существует
            existing_products = self._get_existing_products()
            if product_id in existing_products:
                self.logger.error(f"Продукт с ID {product_id} уже существует")
                return False
            
            # Проверяем подструктуры
            if 'key_benefits' not in data.get('product_info', {}):
                self.logger.error("Отсутствует product_info.key_benefits")
                return False
            
            if 'keywords' not in data.get('seo', {}):
                self.logger.error("Отсутствует seo.keywords")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка валидации данных продукта: {e}")
            return False
    
    def _save_product_config(self, product_data: Dict[str, Any]) -> Path:
        """Сохраняет конфигурацию продукта в YAML файл"""
        product_id = product_data['product_id']
        file_path = self.products_dir / f"{product_id}.yaml"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(product_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        self.logger.info(f"Конфигурация продукта сохранена: {file_path}")
        return file_path
    
    def _get_existing_products(self) -> List[str]:
        """Возвращает список ID существующих продуктов"""
        existing = []
        
        if not self.products_dir.exists():
            return existing
        
        for file_path in self.products_dir.glob("*.yaml"):
            product_id = file_path.stem
            existing.append(product_id)
        
        return existing
    
    def _check_semantic_duplicate(self, message: TelegramMessage) -> Optional[str]:
        """
        Проверяет, есть ли уже продукт с похожим смыслом
        
        Args:
            message: Telegram сообщение для проверки
            
        Returns:
            product_id существующего продукта если найден дубль, иначе None
        """
        try:
            # Получаем существующие продукты
            existing_products = self._get_existing_products_with_data()
            
            if not existing_products:
                return None

            for product_id, product_data in existing_products.items():
                # Формируем полный текст продукта из всех текстовых полей YAML
                product_full_text = self._extract_all_text_from_product(product_data)
                
                # Используем LLM для семантического сравнения
                is_duplicate = self._llm_semantic_comparison(message.text, product_full_text, product_id)
                
                if is_duplicate:
                    self.logger.info(f"LLM обнаружил семантический дубль: {product_id} для сообщения {message.message_id}")
                    return product_id
            
            return None
            
        except Exception as e:
            self.logger.error(f"Ошибка проверки семантических дублей: {e}")
            return None
    
    def _get_existing_products_with_data(self) -> Dict[str, Dict[str, Any]]:
        """Возвращает словарь существующих продуктов с их данными"""
        products = {}
        
        if not self.products_dir.exists():
            return products
        
        for file_path in self.products_dir.glob("*.yaml"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    product_data = yaml.safe_load(f)
                    if product_data and 'product_id' in product_data:
                        products[product_data['product_id']] = product_data
            except Exception as e:
                self.logger.error(f"Ошибка чтения продукта {file_path}: {e}")
        
        return products

    def _extract_all_text_from_product(self, data: Any) -> str:
        """
        Рекурсивно извлекает весь текст из данных продукта (dict, list, str).
        """
        texts = []
        if isinstance(data, dict):
            for key, value in data.items():
                # Игнорируем заведомо нерелевантные для семантики поля
                if key in ['product_id', 'version', 'status', 'demo_available', 'screenshots', 'type', 'required', 'processing_time', 'accuracy']:
                    continue
                texts.append(self._extract_all_text_from_product(value))
        elif isinstance(data, list):
            for item in data:
                texts.append(self._extract_all_text_from_product(item))
        elif isinstance(data, str):
            texts.append(data)
        
        return " ".join(filter(None, texts))

    def _llm_semantic_comparison(self, text1: str, text2: str, product_id_for_logging: str) -> bool:
        """
        Использует LLM для семантического сравнения двух текстов.
        """
        prompt = f"""
ЗАДАЧА: Определи, являются ли два текста семантически эквивалентными.
Оцени, описывают ли они один и тот же продукт или идею, даже если использованы разные слова.

Текст 1 (из нового сообщения в Telegram):
---
{text1}
---

Текст 2 (из существующего продукта "{product_id_for_logging}"):
---
{text2}
---

Проанализируй оба текста и дай ответ в формате JSON.

- Если тексты описывают один и тот же продукт или идею, верни:
  {{"is_duplicate": true, "reason": "краткое объяснение, почему это дубликат"}}

- Если тексты описывают разные продукты, верни:
  {{"is_duplicate": false, "reason": "краткое объяснение, почему это не дубликат"}}
"""
        try:
            response_text = self.llm_service.generate_text(prompt)
            if not response_text:
                self.logger.warning("LLM не вернул ответ для семантического сравнения.")
                return False

            # Извлекаем JSON из ответа
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                self.logger.warning(f"Не удалось найти JSON в ответе LLM для сравнения: {response_text}")
                # В случае неясного ответа, считаем что не дубликат, чтобы не блокировать генерацию
                return False
            
            result = json.loads(json_match.group(0))
            is_duplicate = result.get("is_duplicate", False)
            
            self.logger.info(f"Результат сравнения для '{product_id_for_logging}': is_duplicate={is_duplicate}, причина: {result.get('reason')}")

            return is_duplicate

        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка декодирования JSON из ответа LLM: {e}. Ответ: {response_text}")
            return False # Не дубликат, если не можем распарсить
        except Exception as e:
            self.logger.error(f"Ошибка при семантическом сравнении LLM: {e}")
            return False # Не дубликат в случае ошибки

    def process_batch_messages(self, messages: List[TelegramMessage]) -> Dict[str, Any]:
        """
        Обрабатывает пакет сообщений и генерирует продукты
        
        Args:
            messages: Список Telegram сообщений
            
        Returns:
            Dict с результатами обработки
        """
        results = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "products": [],
            "errors": []
        }
        
        for message in messages:
            results["processed"] += 1
            
            result = self.generate_product_from_message(message)
            
            if result["success"]:
                results["successful"] += 1
                results["products"].append({
                    "product_id": result["product_id"],
                    "product_name": result["product_name"],
                    "message_id": result["message_id"]
                })
            else:
                results["failed"] += 1
                results["errors"].append({
                    "message_id": message.message_id,
                    "error": result["error"]
                })
        
        return results
    
    def process_all_historical_messages(self, telegram_connector) -> Dict[str, Any]:
        """
        Обрабатывает все исторические сообщения из Telegram канала
        
        Args:
            telegram_connector: Объект TelegramConnector для получения сообщений
            
        Returns:
            Dict с результатами обработки всех сообщений
        """
        try:
            self.logger.info("Начинаем обработку всех исторических сообщений")
            
            # Получаем все сообщения из канала (большой лимит) через асинхронный вызов
            import asyncio
            
            async def fetch_messages_async():
                return await telegram_connector.fetch_all_messages()
            
            # Проверяем, есть ли активный цикл событий
            try:
                loop = asyncio.get_running_loop()
                # Если цикл уже запущен, создаем новый
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, fetch_messages_async())
                    all_messages = future.result()
            except RuntimeError:
                # Если цикла нет, создаем новый
                all_messages = asyncio.run(fetch_messages_async())
            
            if not all_messages:
                return {
                    "processed": 0,
                    "successful": 0,
                    "failed": 0,
                    "skipped_duplicates": 0,
                    "products": [],
                    "errors": [],
                    "duplicates": []
                }
            
            self.logger.info(f"Получено {len(all_messages)} сообщений для обработки")
            
            results = {
                "processed": 0,
                "successful": 0,
                "failed": 0,
                "skipped_duplicates": 0,
                "products": [],
                "errors": [],
                "duplicates": []
            }
            
            for message in all_messages:
                # Фильтруем только содержательные сообщения
                if not self._is_suitable_for_product_generation(message):
                    continue
                
                results["processed"] += 1
                
                result = self.generate_product_from_message(message)
                
                if result["success"]:
                    results["successful"] += 1
                    results["products"].append({
                        "product_id": result["product_id"],
                        "product_name": result["product_name"],
                        "message_id": result["message_id"]
                    })
                    self.logger.info(f"Создан продукт: {result['product_id']}")
                    
                elif "duplicate_product_id" in result:
                    results["skipped_duplicates"] += 1
                    results["duplicates"].append({
                        "message_id": result["message_id"],
                        "duplicate_of": result["duplicate_product_id"],
                        "error": result["error"]
                    })
                    self.logger.info(f"Пропущен дубль: сообщение {result['message_id']}")
                    
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "message_id": message.message_id,
                        "error": result["error"]
                    })
                    self.logger.error(f"Ошибка обработки сообщения {message.message_id}: {result['error']}")
            
            self.logger.info(f"Обработка завершена. Создано: {results['successful']}, пропущено дублей: {results['skipped_duplicates']}, ошибок: {results['failed']}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Ошибка обработки исторических сообщений: {e}")
            return {
                "processed": 0,
                "successful": 0,
                "failed": 1,
                "skipped_duplicates": 0,
                "products": [],
                "errors": [{"error": str(e)}],
                "duplicates": []
            }
    
    def _is_suitable_for_product_generation(self, message: TelegramMessage) -> bool:
        """
        Проверяет, подходит ли сообщение для генерации продукта
        
        Args:
            message: Telegram сообщение
            
        Returns:
            True если сообщение подходит для генерации продукта
        """
        if not message.text or len(message.text.strip()) < 20:
            return False
        
        # Исключаем служебные сообщения
        text_lower = message.text.lower()
        excluded_patterns = [
            "подписывайтесь",
            "реклама",
            "спонсор",
            "партнер",
            "@",  # сообщения с упоминаниями
            "http",  # сообщения только со ссылками
            "📢",  # объявления
            "🎉",  # поздравления
        ]
        
        for pattern in excluded_patterns:
            if pattern in text_lower:
                return False
        
        # Ищем ключевые слова, указывающие на продукт/сервис
        product_indicators = [
            "сервис",
            "продукт", 
            "платформа",
            "система",
            "решение",
            "инструмент",
            "помощник",
            "анализ",
            "автоматизация",
            "мониторинг",
            "генератор",
            "бот",
            "приложение"
        ]
        
        for indicator in product_indicators:
            if indicator in text_lower:
                return True
        
        return False
    
    def _normalize_text(self, text: str) -> str:
        """Нормализует текст для сравнения"""
        if not text:
            return ""
        
        # Приводим к нижнему регистру
        text = text.lower()
        
        # Удаляем лишние символы и оставляем только буквы, цифры и пробелы
        import re
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Удаляем множественные пробелы
        text = re.sub(r'\s+', ' ', text)
        
        # Убираем пробелы в начале и конце
        text = text.strip()
        
        return text
    
    def _extract_all_text_from_product(self, product_data: Dict[str, Any]) -> str:
        """
        Извлекает весь текстовый контент из YAML-данных продукта
        
        Args:
            product_data: Словарь с данными продукта
            
        Returns:
            Объединенный текст всех текстовых полей продукта
        """
        def extract_text_recursive(obj, texts):
            """Рекурсивно извлекает все строковые значения"""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key not in ['product_id', 'version', 'status']:  # Исключаем технические поля
                        extract_text_recursive(value, texts)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text_recursive(item, texts)
            elif isinstance(obj, str) and obj.strip():
                texts.append(obj.strip())
        
        all_texts = []
        extract_text_recursive(product_data, all_texts)
        
        # Объединяем все тексты с разделителями
        combined_text = " | ".join(all_texts)
        
        return combined_text
    
    def _llm_semantic_comparison(self, new_text: str, existing_text: str, product_id: str) -> bool:
        """
        Использует LLM для семантического сравнения двух текстов
        
        Args:
            new_text: Новый текст из Telegram сообщения
            existing_text: Существующий текст продукта
            product_id: ID существующего продукта для контекста
            
        Returns:
            True если тексты семантически похожи, False иначе
        """
        try:
            prompt = f"""
Твоя задача - определить, описывают ли два текста один и тот же или очень похожий продукт/сервис.

НОВЫЙ ТЕКСТ (из Telegram):
"{new_text}"

СУЩЕСТВУЮЩИЙ ПРОДУКТ (ID: {product_id}):
"{existing_text}"

Критерии для определения дубликата:
1. Оба текста описывают продукты одной сферы деятельности
2. Основные функции и возможности совпадают
3. Целевая аудитория похожа
4. Решаемые задачи идентичны

ВАЖНО: Продукты считаются дублями, только если они решают ОДИНАКОВЫЕ задачи в ОДНОЙ сфере.
Например:
- "Анализ договоров" и "Проверка контрактов" = ДУБЛЬ
- "Мониторинг новостей" и "Анализ медиа" = ДУБЛЬ  
- "CRM автоматизация" и "Анализ договоров" = НЕ ДУБЛЬ (разные сферы)

Ответь только "ДА" если это дубликат, или "НЕТ" если это разные продукты.
"""
            
            response = self.llm_service.generate_text(prompt)
            
            if not response:
                self.logger.warning(f"LLM не вернул ответ для сравнения с {product_id}")
                return False
            
            # Нормализуем ответ
            response_normalized = response.strip().upper()
            
            # Проверяем ответ
            is_duplicate = "ДА" in response_normalized or "YES" in response_normalized
            
            self.logger.debug(f"LLM сравнение с {product_id}: '{response.strip()}' -> {is_duplicate}")
            
            return is_duplicate
            
        except Exception as e:
            self.logger.error(f"Ошибка LLM сравнения с {product_id}: {e}")
            return False
