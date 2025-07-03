"""
Тесты для Telegram коннектора и генератора продуктов
"""

import pytest
import tempfile
import os
import yaml
from unittest.mock import Mock, patch, MagicMock
from src.backend.services.telegram_product_generator import TelegramProductGenerator, TelegramMessage


class TestTelegramMessage:
    """Тесты для класса TelegramMessage"""
    
    def test_telegram_message_creation(self):
        """Тест создания объекта TelegramMessage"""
        message = TelegramMessage(
            message_id=123,
            text="Тестовое сообщение",
            date="2025-07-03T10:00:00Z",
            media_files=["image1.jpg"]
        )
        
        assert message.message_id == 123
        assert message.text == "Тестовое сообщение"
        assert message.date == "2025-07-03T10:00:00Z"
        assert message.media_files == ["image1.jpg"]
    
    def test_telegram_message_without_media(self):
        """Тест создания сообщения без медиа файлов"""
        message = TelegramMessage(
            message_id=124,
            text="Сообщение без картинок",
            date="2025-07-03T11:00:00Z"
        )
        
        assert message.media_files == []


class TestTelegramProductGenerator:
    """Тесты для TelegramProductGenerator"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Создаем mock LLM service
        self.mock_llm_service = Mock()
        self.mock_llm_service.generate_text.return_value = self._get_sample_yaml_response()
        
        # Создаем генератор
        self.generator = TelegramProductGenerator(
            llm_service=self.mock_llm_service,
            products_dir=self.temp_dir
        )
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _get_sample_yaml_response(self):
        """Возвращает пример ответа LLM с YAML конфигурацией"""
        return """---
product_id: "ai_assistant"
name: "AI Помощник для Бизнеса"
description: "Интеллектуальный помощник для автоматизации бизнес-процессов"
version: "1.0"
category: "ai"
status: "active"

demo_data:
  key_features:
    - "Обработка естественного языка"
    - "Автоматизация задач"
    - "Интеграция с CRM"

product_info:
  key_benefits:
    - "Экономия времени до 60%"
    - "Снижение ошибок"
    - "24/7 доступность"
  
  target_audience:
    - "Малый бизнес"
    - "IT компании"
    - "Консалтинг"

seo:
  keywords:
    - "AI помощник"
    - "автоматизация бизнеса"
    - "искусственный интеллект"
"""
    
    def test_generate_product_prompt_creation(self):
        """Тест создания промпта для генерации продукта"""
        message = TelegramMessage(
            message_id=123,
            text="Новый AI помощник для автоматизации бизнес процессов. Умеет обрабатывать документы и отвечать на вопросы.",
            date="2025-07-03T10:00:00Z",
            media_files=["assistant.jpg"]
        )
        
        prompt = self.generator._create_product_generation_prompt(message)
        
        # Проверяем что промпт содержит нужные элементы
        assert "AI помощник" in prompt
        assert "автоматизации" in prompt  # правильная форма слова из сообщения
        assert "YAML" in prompt
        assert "product_id" in prompt
        assert "assistant.jpg" in prompt
    
    def test_parse_yaml_from_llm_response_success(self):
        """Тест успешного парсинга YAML из ответа LLM"""
        llm_response = self._get_sample_yaml_response()
        
        parsed_data = self.generator._parse_yaml_from_llm_response(llm_response)
        
        assert parsed_data is not None
        assert parsed_data["product_id"] == "ai_assistant"
        assert parsed_data["name"] == "AI Помощник для Бизнеса"
        assert "key_benefits" in parsed_data["product_info"]
    
    def test_parse_yaml_from_llm_response_with_markdown(self):
        """Тест парсинга YAML из ответа LLM с markdown форматированием"""
        llm_response = f"""
Вот сгенерированная конфигурация продукта:

```yaml
{self._get_sample_yaml_response()}
```

Это конфигурация для нового продукта.
"""
        
        parsed_data = self.generator._parse_yaml_from_llm_response(llm_response)
        
        assert parsed_data is not None
        assert parsed_data["product_id"] == "ai_assistant"
    
    def test_parse_yaml_from_llm_response_invalid(self):
        """Тест обработки невалидного YAML ответа"""
        invalid_response = "Это не YAML контент, а обычный текст"
        
        parsed_data = self.generator._parse_yaml_from_llm_response(invalid_response)
        
        # Невалидный YAML должен возвращать None
        assert parsed_data is None
    
    def test_validate_product_data_success(self):
        """Тест успешной валидации данных продукта"""
        valid_data = {
            "product_id": "test_product",
            "name": "Тестовый продукт",
            "description": "Описание тестового продукта",
            "category": "test",
            "demo_data": {},
            "product_info": {"key_benefits": []},
            "seo": {"keywords": []}
        }
        
        is_valid = self.generator._validate_product_data(valid_data)
        assert is_valid is True
    
    def test_validate_product_data_missing_fields(self):
        """Тест валидации с отсутствующими обязательными полями"""
        invalid_data = {
            "name": "Продукт без ID",
            "description": "Описание"
        }
        
        is_valid = self.generator._validate_product_data(invalid_data)
        assert is_valid is False
    
    def test_save_product_config_success(self):
        """Тест успешного сохранения конфигурации продукта"""
        product_data = {
            "product_id": "test_save",
            "name": "Тест сохранения",
            "description": "Тестовое описание"
        }
        
        file_path = self.generator._save_product_config(product_data)
        
        # Проверяем что файл создан
        assert os.path.exists(file_path)
        assert str(file_path).endswith("test_save.yaml")
        
        # Проверяем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = yaml.safe_load(f)
        
        assert saved_data["product_id"] == "test_save"
        assert saved_data["name"] == "Тест сохранения"
    
    def test_generate_product_from_message_success(self):
        """Тест успешной генерации продукта из Telegram сообщения"""
        message = TelegramMessage(
            message_id=125,
            text="Инновационный AI помощник для бизнеса",
            date="2025-07-03T12:00:00Z"
        )
        
        # Настраиваем LLM на возврат полного YAML с уникальным ID
        complete_yaml = """---
product_id: "innovation_ai_assistant"
name: "Инновационный AI Помощник"
description: "Продвинутый AI помощник для автоматизации бизнес-процессов"
version: "1.0"
category: "ai"
status: "active"

demo_data:
  key_features:
    - "Обработка естественного языка"
    - "Интеллектуальная автоматизация"
    - "Интеграция с бизнес-системами"

product_info:
  key_benefits:
    - "Повышение эффективности на 50%"
    - "Снижение операционных затрат"
    - "Круглосуточная поддержка"
  
  target_audience:
    - "Средний бизнес"
    - "Стартапы"
    - "IT компании"

seo:
  keywords:
    - "AI помощник"
    - "автоматизация бизнеса"
    - "искусственный интеллект"
"""
        self.mock_llm_service.generate_text.return_value = complete_yaml
        
        result = self.generator.generate_product_from_message(message)
        
        # Проверяем что генерация прошла успешно
        assert result["success"] is True
        assert "product_id" in result
        assert result["product_id"] == "innovation_ai_assistant"
        assert "file_path" in result
        
        # Проверяем что файл был создан
        assert os.path.exists(result["file_path"])
        
        # Проверяем что LLM был вызван с правильным промптом
        self.mock_llm_service.generate_text.assert_called_once()
        call_args = self.mock_llm_service.generate_text.call_args[0][0]
        assert "AI помощник" in call_args
    
    def test_generate_product_from_message_llm_failure(self):
        """Тест обработки ошибки LLM при генерации продукта"""
        # Настраиваем LLM на возврат ошибки
        self.mock_llm_service.generate_text.return_value = None
        
        message = TelegramMessage(
            message_id=126,
            text="Тестовое сообщение",
            date="2025-07-03T13:00:00Z"
        )
        
        result = self.generator.generate_product_from_message(message)
        
        # Проверяем что обработка ошибки корректная
        assert result["success"] is False
        assert "error" in result
        assert "LLM не вернул" in result["error"]
    
    def test_generate_product_from_message_invalid_yaml(self):
        """Тест обработки невалидного YAML от LLM"""
        # Настраиваем LLM на возврат невалидного YAML
        self.mock_llm_service.generate_text.return_value = "Невалидный YAML контент"
        
        message = TelegramMessage(
            message_id=127,
            text="Тестовое сообщение",
            date="2025-07-03T14:00:00Z"
        )
        
        result = self.generator.generate_product_from_message(message)
        
        # Проверяем что ошибка обработана корректно
        assert result["success"] is False
        assert "error" in result
        # Может быть ошибка парсинга или валидации
        assert any(keyword in result["error"] for keyword in ["парсинг", "валидацию", "YAML"])
    
    def test_get_existing_products(self):
        """Тест получения списка существующих продуктов"""
        # Создаем несколько тестовых файлов продуктов
        test_products = ["product1.yaml", "product2.yaml", "not_yaml.txt"]
        
        for filename in test_products:
            file_path = os.path.join(self.temp_dir, filename)
            with open(file_path, 'w') as f:
                if filename.endswith('.yaml'):
                    f.write("product_id: test\nname: Test")
                else:
                    f.write("not yaml content")
        
        existing = self.generator._get_existing_products()
        
        # Должен вернуть только YAML файлы
        assert len(existing) == 2
        assert "product1" in existing
        assert "product2" in existing
        assert "not_yaml" not in existing
    
    def test_semantic_duplicate_detection(self):
        """Тест обнаружения семантических дублей"""
        # Создаем первый продукт
        first_message = TelegramMessage(
            message_id=200,
            text="Система анализа договоров с использованием ИИ",
            date="2025-07-03T15:00:00Z"
        )
        
        # Мокируем LLM для создания первого продукта
        first_yaml = """---
product_id: "contract_ai_system"
name: "ИИ-система анализа договоров"
description: "Автоматический анализ юридических документов"
version: "1.0"
category: "legal"
status: "active"

demo_data:
  key_features:
    - "Анализ договоров"
    - "Выявление рисков"
    - "Юридические рекомендации"

product_info:
  key_benefits:
    - "Экономия времени юристов"
    - "Снижение правовых рисков"
    - "Автоматизация процессов"

seo:
  keywords:
    - "анализ договоров"
    - "юридический ИИ"
    - "проверка контрактов"
"""
        self.mock_llm_service.generate_text.return_value = first_yaml
        
        # Создаем первый продукт
        result1 = self.generator.generate_product_from_message(first_message)
        assert result1["success"] is True
        
        # Теперь пытаемся создать похожий продукт
        duplicate_message = TelegramMessage(
            message_id=201,
            text="Новый сервис для проверки договоров с помощью искусственного интеллекта",
            date="2025-07-03T16:00:00Z"
        )
        
        # Мокируем LLM для второго вызова (хотя он не должен быть вызван)
        # Это нужно, чтобы избежать падения на этапе парсинга, если семантическая проверка не сработает
        second_yaml = """---
product_id: "new_contract_service"
name: "Новый сервис проверки договоров"
description: "Проверка контрактов с ИИ"
version: "1.0"
category: "legal"
status: "active"
demo_data:
  key_features: ["Проверка"]
product_info:
  key_benefits: ["Скорость"]
seo:
  keywords: ["договор", "ИИ"]
"""
        self.mock_llm_service.generate_text.return_value = second_yaml

        # Пытаемся создать дубль (семантическая проверка должна сработать раньше LLM)
        result2 = self.generator.generate_product_from_message(duplicate_message)
        
        # Проверяем что дубль был обнаружен
        assert result2["success"] is False, f"Ожидался неуспех, но результат: {result2}"
        assert "duplicate_product_id" in result2, f"Ключ 'duplicate_product_id' отсутствует в результате: {result2}"
        assert result2["duplicate_product_id"] == "contract_ai_system"
        assert "похожим смыслом" in result2["error"]
    
    def test_different_categories_no_duplicate(self):
        """Тест что продукты разных категорий не считаются дублями"""
        # Создаем продукт категории legal
        legal_message = TelegramMessage(
            message_id=202,
            text="Анализ договоров с ИИ",
            date="2025-07-03T17:00:00Z"
        )
        
        legal_yaml = """---
product_id: "legal_analyzer"
name: "Анализатор договоров"
description: "Юридический анализ"
version: "1.0"
category: "legal"
status: "active"

demo_data:
  key_features: ["Анализ"]

product_info:
  key_benefits: ["Польза"]

seo:
  keywords: ["договор"]
"""
        self.mock_llm_service.generate_text.return_value = legal_yaml
        result1 = self.generator.generate_product_from_message(legal_message)
        assert result1["success"] is True
        
        # Создаем продукт категории analytics с похожими словами
        analytics_message = TelegramMessage(
            message_id=203,
            text="Аналитика и анализ данных для бизнеса",
            date="2025-07-03T18:00:00Z"
        )
        
        analytics_yaml = """---
product_id: "business_analytics"
name: "Бизнес-аналитика"
description: "Анализ бизнес-данных"
version: "1.0"
category: "analytics"
status: "active"

demo_data:
  key_features: ["Аналитика"]

product_info:
  key_benefits: ["Инсайты"]

seo:
  keywords: ["аналитика"]
"""
        self.mock_llm_service.generate_text.return_value = analytics_yaml
        result2 = self.generator.generate_product_from_message(analytics_message)
        
        # Проверяем что дубль НЕ обнаружен (разные категории)
        assert result2["success"] is True
        assert "duplicate_product_id" not in result2

    # ...existing code...


class TestTelegramApiIntegration:
    """Тесты для интеграции с Telegram API"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        self.mock_llm_service = Mock()
        self.temp_dir = tempfile.mkdtemp()
        
        self.generator = TelegramProductGenerator(
            llm_service=self.mock_llm_service,
            products_dir=self.temp_dir
        )
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('requests.get')
    def test_fetch_channel_updates_success(self, mock_get):
        """Тест успешного получения обновлений из канала"""
        # Мокируем ответы Telegram API для getChat и getUpdates
        def mock_response_side_effect(url, **kwargs):
            mock_response = Mock()
            
            if "getChat" in url:
                # Ответ для получения информации о канале
                mock_response.json.return_value = {
                    "ok": True,
                    "result": {
                        "id": -123456789,
                        "username": "aideaxondemos",
                        "type": "channel"
                    }
                }
            elif "getUpdates" in url:
                # Ответ для получения обновлений (channel_post)
                mock_response.json.return_value = {
                    "ok": True,
                    "result": [
                        {
                            "channel_post": {
                                "message_id": 100,
                                "date": 1704283200,
                                "text": "Новый продукт для тестирования",
                                "chat": {
                                    "id": -123456789,
                                    "username": "aideaxondemos",
                                    "type": "channel"
                                },
                                "photo": [{"file_id": "photo123"}]
                            }
                        }
                    ]
                }
            
            mock_response.status_code = 200
            return mock_response
        
        mock_get.side_effect = mock_response_side_effect
        
        # Создаем Telegram коннектор
        from src.backend.services.telegram_connector import TelegramConnector
        connector = TelegramConnector(
            bot_token="test_token",
            channel_username="aideaxondemos"
        )
        
        messages = connector.fetch_recent_messages(limit=10)
        
        # Проверяем результат
        assert len(messages) == 1
        assert messages[0].message_id == 100
        assert messages[0].text == "Новый продукт для тестирования"
        assert len(messages[0].media_files) == 1
    
    def test_integration_message_to_product(self):
        """Интеграционный тест: от Telegram сообщения до создания продукта"""
        # Настраиваем LLM на возврат валидного YAML
        self.mock_llm_service.generate_text.return_value = """---
product_id: "integration_test"
name: "Интеграционный тест"
description: "Продукт созданный в интеграционном тесте"
category: "test"
demo_data:
  test_feature: "работает"
product_info:
  key_benefits:
    - "Автоматическое тестирование"
seo:
  keywords:
    - "интеграционный тест"
"""
        
        # Создаем тестовое сообщение
        from src.backend.services.telegram_product_generator import TelegramMessage
        message = TelegramMessage(
            message_id=200,
            text="🚀 Новый революционный продукт для интеграционного тестирования! Автоматически создает тесты и проверяет их работу.",
            date="2025-07-03T15:00:00Z",
            media_files=["integration_demo.png"]
        )
        
        # Генерируем продукт
        result = self.generator.generate_product_from_message(message)
        
        # Проверяем успешность
        assert result["success"] is True
        assert result["product_id"] == "integration_test"
        
        # Проверяем что файл создан и содержит правильные данные
        with open(result["file_path"], 'r', encoding='utf-8') as f:
            product_data = yaml.safe_load(f)
        
        assert product_data["name"] == "Интеграционный тест"
        assert product_data["demo_data"]["test_feature"] == "работает"
        assert "интеграционный тест" in product_data["seo"]["keywords"]
