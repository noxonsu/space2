import os
import requests
import json
from dotenv import load_dotenv
import logging
from flask import current_app
from typing import List, Dict, Any

# Загружаем переменные окружения из .env файла
load_dotenv()

# Импортируем функции кэширования сегментации и генерации хэша
from .cache_service import CacheService

class LLMService:
    def __init__(self, deepseek_api_key: str, openai_api_key: str):
        self.deepseek_api_key = deepseek_api_key
        self.openai_api_key = openai_api_key
        self.cache_service = CacheService()
        self.logger = self._get_logger()
        
        # Доступные модели
        # Устанавливаем модель по умолчанию на основе наличия ключей
        # Теперь available_models_list будет заполняться при первом вызове get_available_models
        # или при явном вызове set_current_model.
        # Для инициализации, попробуем установить модель по умолчанию, если ключи есть.
        self.current_model_full_id = None # Например, "openai:gpt-4o"
        self.current_model_type = None    # Например, "openai"
        self.api_url = None
        self.service_name = None
        self.api_key = None
        self.default_model_name = None # Конкретное имя модели, например "gpt-4o"

        if self.openai_api_key:
            default_openai_model = os.getenv('DEFAULT_OPENAI_MODEL', 'gpt-4o') # Получаем из .env или используем gpt-4o как запасной вариант
            self.set_current_model(f"openai:{default_openai_model}") # Устанавливаем дефолтную OpenAI модель
        elif self.deepseek_api_key:
            self.set_current_model("deepseek:deepseek-chat") # Устанавливаем дефолтную DeepSeek модель
        else:
            self.logger.warning("LLMService: Нет доступных API ключей для OpenAI или DeepSeek. LLMService не будет функционировать.")

    def set_current_model(self, model_full_id: str):
        """
        Устанавливает текущую используемую модель LLM.
        model_full_id должен быть в формате 'provider:model_name' (например, 'openai:gpt-4o').
        """
        parts = model_full_id.split(':', 1)
        if len(parts) != 2:
            raise ValueError(f"Некорректный формат model_full_id: '{model_full_id}'. Ожидается 'provider:model_name'.")
        
        model_type, model_name = parts[0], parts[1]

        if model_type == "openai":
            if not self.openai_api_key:
                raise ValueError(f"API ключ OpenAI не установлен для модели '{model_name}'.")
            self.current_model_type = "openai"
            self.api_url = "https://api.openai.com/v1/chat/completions"
            self.service_name = "OpenAI"
            self.api_key = self.openai_api_key
        elif model_type == "deepseek":
            if not self.deepseek_api_key:
                raise ValueError(f"API ключ DeepSeek не установлен для модели '{model_name}'.")
            self.current_model_type = "deepseek"
            self.api_url = "https://api.deepseek.com/chat/completions"
            self.service_name = "DeepSeek"
            self.api_key = self.deepseek_api_key
        else:
            raise ValueError(f"Неизвестный тип провайдера LLM: '{model_type}'.")
        
        self.current_model_full_id = model_full_id
        self.default_model_name = model_name # Теперь это конкретное имя модели
        self.logger.info(f"LLMService: Установлена текущая модель: {self.current_model_full_id}")

    def _get_logger(self):
        if current_app:
            return current_app.logger
        else:
            # Если нет контекста Flask, используем стандартный логгер
            logging.basicConfig(level=logging.INFO)
            return logging.getLogger(__name__)

    def generate_text(self, prompt: str, model_full_id: str = None, temperature: float = 0.7, max_tokens: int = 4000, timeout: int = 300) -> str:
        logger = self.logger
        
        # Если model_full_id не указан, используем текущую установленную модель
        if model_full_id is None:
            if self.current_model_full_id is None:
                error_msg = "LLMService: Модель не выбрана и не установлена по умолчанию."
                logger.error(error_msg)
                raise ValueError(error_msg)
            model_to_use_full_id = self.current_model_full_id
        else:
            model_to_use_full_id = model_full_id

        # Разбираем model_full_id на тип провайдера и имя модели
        try:
            model_type, model_name = model_to_use_full_id.split(':', 1)
        except ValueError:
            error_msg = f"Некорректный формат model_full_id: '{model_to_use_full_id}'. Ожидается 'provider:model_name'."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Временно переключаем контекст LLMService, если запрошенная модель отличается от текущей
        original_model_full_id = self.current_model_full_id
        if model_to_use_full_id != original_model_full_id:
            try:
                self.set_current_model(model_to_use_full_id)
            except ValueError as e:
                # Если не удалось установить модель, возвращаем ошибку
                logger.error(f"LLMService: Не удалось временно установить модель '{model_to_use_full_id}': {e}")
                raise

        logger.info(f"{self.service_name}Service: Вызов generate_text для промпта (первые 250 символов): '{prompt[:250]}...' ")

        if not self.api_key:
            error_msg = f"{self.service_name}Service: API ключ не установлен для {self.service_name}."
            logger.error(error_msg)
            raise ValueError(error_msg)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": model_name, # Используем model_name здесь
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            logger.info(f"{self.service_name}Service: Отправка запроса к {self.service_name} API. URL: {self.api_url}, Модель: {model_name}, Таймаут: {timeout}s")
            response = requests.post(self.api_url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            
            response_json = response.json()
            
            if 'choices' in response_json and len(response_json['choices']) > 0:
                content = response_json['choices'][0]['message']['content']
                if logger:
                    logger.info(f"{self.service_name}Service: Текст успешно сгенерирован (первые 250 символов): '{content[:250]}...' ")
            else:
                error_message = response_json.get("error", {}).get("message", "Неизвестная ошибка формата ответа")
                if logger:
                    logger.error(f"{self.service_name}Service: Ошибка формата ответа от {self.service_name}: {error_message} | Полный ответ: {response_json}")
                raise ValueError(f"Ошибка формата ответа от {self.service_name}: {error_message}")

        except requests.exceptions.Timeout as e:
            error_msg = f"{self.service_name}Service: Таймаут запроса к {self.service_name} API после {timeout} секунд: {e}"
            logger.error(error_msg)
            raise TimeoutError(error_msg) from e
        except requests.exceptions.HTTPError as e:
            error_msg = f"{self.service_name}Service: HTTP Ошибка от {self.service_name} API: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
        except requests.exceptions.ConnectionError as e:
            error_msg = f"{self.service_name}Service: Ошибка соединения с {self.service_name} API: {e}"
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
        except requests.exceptions.RequestException as e:
            error_msg = f"{self.service_name}Service: Общая ошибка запроса к {self.service_name} API: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        except json.JSONDecodeError as e:
            error_msg = f"{self.service_name}Service: Ошибка декодирования JSON от {self.service_name} API: {e}. Ответ: {response.text[:1000]}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
        except Exception as e:
            error_msg = f"{self.service_name}Service: Неизвестная ошибка при работе с {self.service_name} API: {e}"
            logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e
        finally:
            # Восстанавливаем исходную модель, если она была временно изменена
            if model_to_use_full_id != original_model_full_id:
                self.set_current_model(original_model_full_id)

        return content.strip()

    def analyze_sentence_in_context(self, sentence: str, full_contract_context: str, model_full_id: str = None) -> str:
        logger = self.logger
        logger.info(f"LLMService: Вызов analyze_sentence_in_context для предложения: '{sentence[:250]}...' ")

        # Используем model_full_id, если передан, иначе текущую модель
        model_to_use_full_id = model_full_id if model_full_id else self.current_model_full_id
        
        # Определяем конкретное имя модели для анализа на основе провайдера
        if model_to_use_full_id:
            model_type, model_name = model_to_use_full_id.split(':', 1)
            if model_type == "deepseek":
                model_for_analysis_name = "deepseek-reasoner"
            elif model_type == "openai":
                model_for_analysis_name = os.getenv('DEFAULT_OPENAI_MODEL', 'gpt-4o') # Используем модель из .env
            else:
                model_for_analysis_name = self.default_model_name # Fallback
        else:
            model_for_analysis_name = self.default_model_name # Fallback

        prompt = f"""
        Проанализируй следующее предложение с юридической точки зрения, учитывая полный контекст договора.
        Укажи потенциальные риски, дай рекомендации по улучшению формулировки и объясни, как это предложение связано с другими частями документа.
        Предоставь анализ в виде связного текста.

        Полный текст договора для контекста:
        ---
        {full_contract_context}
        ---
        Предложение для анализа:
        ---
        {sentence}
        ---
        Твой анализ:
        """
        return self.generate_text(prompt, model_full_id=model_to_use_full_id, temperature=0, max_tokens=2000, timeout=120)

    def analyze_paragraph_in_context(self, paragraph: str, full_contract_context: str, model_full_id: str = None) -> str:
        logger = self.logger
        logger.info(f"LLMService: Вызов analyze_paragraph_in_context для пункта: '{paragraph[:250]}...' ")

        # Используем model_full_id, если передан, иначе текущую модель
        model_to_use_full_id = model_full_id if model_full_id else self.current_model_full_id

        # Определяем конкретное имя модели для анализа на основе провайдера
        if model_to_use_full_id:
            model_type, model_name = model_to_use_full_id.split(':', 1)
            if model_type == "deepseek":
                model_for_analysis_name = "deepseek-reasoner"
            elif model_type == "openai":
                model_for_analysis_name = os.getenv('DEFAULT_OPENAI_MODEL', 'gpt-4o') # Используем модель из .env
            else:
                model_for_analysis_name = self.default_model_name # Fallback
        else:
            model_for_analysis_name = self.default_model_name # Fallback

        prompt = f"""
        Проанализируй следующий пункт/абзац с юридической точки зрения, учитывая полный контекст договора.
        Укажи потенциальные риски, дай рекомендации по улучшению формулировки и объясни, как этот пункт/абзац связан с другими частями документа.
        Предоставь анализ в виде связного текста.

        Полный текст договора для контекста:
        ---
        {full_contract_context}
        ---
        Пункт/абзац для анализа:
        ---
        {paragraph}
        ---
        Твой анализ:
        """
        return self.generate_text(prompt, model_full_id=model_to_use_full_id, temperature=0, max_tokens=4000, timeout=600)

    def segment_text_into_paragraphs(self, text_content: str, model_full_id: str = None) -> List[str]:
        logger = self.logger
        logger.info(f"LLMService: Вызов segment_text_into_paragraphs для текста (первые 250 символов): '{text_content[:250]}' ")

        text_hash = self.cache_service._generate_hash(text_content)
        cached_paragraphs = self.cache_service.get_cached_segmentation(text_hash)
        if cached_paragraphs:
            logger.info(f"LLMService: Результат сегментации для хэша {text_hash} найден в кэше.")
            return cached_paragraphs

        # Используем model_full_id, если передан, иначе текущую модель
        model_to_use_full_id = model_full_id if model_full_id else self.current_model_full_id

        prompt = f"""
        Разбей следующий текст на отдельные пункты или смысловые абзацы. Каждый пункт должен быть на новой строке.
        Не добавляй никаких дополнительных комментариев или пояснений, только список пунктов.
        Учитывай, что пункты могут быть обозначены цифрами, буквами или просто отдельными абзацами.

        Пример:
        Текст: "1. Первый пункт. Это его продолжение. 2. Второй пункт. 3. Третий пункт."
        Результат:
        1. Первый пункт. Это его продолжение.
        2. Второй пункт.
        3. Третий пункт.

        Текст: "Арендодатель обязуется предоставить. Арендатор обязуется принять. Стороны договорились."
        Результат:
        Арендодатель обязуется предоставить.
        Арендатор обязуется принять.
        Стороны договорились.

        Текст для сегментации:
        ---
        {text_content}
        ---
        Результат:
        """
        
        raw_segmented_text = self.generate_text(prompt, model_full_id=model_to_use_full_id, max_tokens=2000, temperature=0, timeout=120)
        
        logger.info(f"LLMService: Полный ответ от LLM для сегментации (до разделения): '{raw_segmented_text[:500]}' ")

        paragraphs = [p.strip() for p in raw_segmented_text.split('\n') if p.strip()]
        
        filtered_paragraphs = []
        for s in paragraphs:
            stripped_s = s.strip()
            if stripped_s and not stripped_s.startswith('#'):
                filtered_paragraphs.append(stripped_s)

        logger.info(f"LLMService: Получено {len(filtered_paragraphs)} отфильтрованных пунктов после сегментации.")
        
        self.cache_service.save_segmentation_to_cache(text_hash, filtered_paragraphs)
        logger.info(f"LLMService: Результат сегментации для хэша {text_hash} сохранен в кэш.")

        return filtered_paragraphs


    def get_available_models(self) -> List[str]:
        """Получает список доступных моделей от всех провайдеров"""
        unique_models = set()
        
        # Добавляем модели DeepSeek
        if self.deepseek_api_key:
            deepseek_models = self._get_deepseek_models()
            # Добавляем префикс "deepseek:" к моделям DeepSeek
            unique_models.update([f"deepseek:{model}" for model in deepseek_models])
        
        # Добавляем модели OpenAI
        if self.openai_api_key:
            openai_models = self._get_openai_models()
            # Добавляем префикс "openai:" к моделям OpenAI
            unique_models.update([f"openai:{model}" for model in openai_models])
        
        # Возвращаем отсортированный список
        return sorted(list(unique_models))
    
    def _get_deepseek_models(self) -> List[str]:
        """Получает список доступных моделей DeepSeek"""
        try:
            url = "https://api.deepseek.com/v1/models"
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = []
                
                for model in data.get('data', []):
                    model_id = model.get('id')
                    if model_id:
                        models.append(model_id)
                
                self.logger.info(f"Получены DeepSeek модели: {models}")
                return models
            else:
                self.logger.warning(f"Ошибка получения DeepSeek моделей: {response.status_code}")
                # Возвращаем дефолтные модели
                return ["deepseek-chat", "deepseek-coder"]
                
        except Exception as e:
            self.logger.error(f"Ошибка запроса к DeepSeek API: {e}")
            return ["deepseek-chat", "deepseek-coder"]
    
    def _get_openai_models(self) -> List[str]:
        """Получает список доступных моделей OpenAI"""
        try:
            url = "https://api.openai.com/v1/models"
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = []
                
                # Фильтруем только текстовые модели
                allowed_models = [
                    'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4',
                    'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'
                ]
                
                for model in data.get('data', []):
                    model_id = model.get('id')
                    if model_id and model_id in allowed_models:
                        models.append(model_id)
                
                self.logger.info(f"Получены OpenAI модели: {models}")
                return models
            else:
                self.logger.warning(f"Ошибка получения OpenAI моделей: {response.status_code}")
                # Возвращаем дефолтные модели
                return ["gpt-4o", "gpt-3.5-turbo"]
                
        except Exception as e:
            self.logger.error(f"Ошибка запроса к OpenAI API: {e}")
            return ["gpt-4o", "gpt-3.5-turbo"]
    
    def get_model_info(self, model_full_id: str) -> Dict[str, str]: # Изменено: теперь принимает model_full_id
        """Возвращает информацию о модели"""
        parts = model_full_id.split(':', 1)
        if len(parts) != 2:
            # Если формат некорректный, возвращаем общую информацию
            return {
                "provider": "Unknown",
                "description": "Неизвестная модель",
                "context_length": "Unknown"
            }
        
        model_type, model_name = parts[0], parts[1]

        model_info = {
            "deepseek:deepseek-chat": { # Изменено
                "provider": "DeepSeek",
                "description": "Универсальная модель для диалогов",
                "context_length": "32k"
            },
            "deepseek:deepseek-coder": { # Изменено
                "provider": "DeepSeek", 
                "description": "Модель для программирования",
                "context_length": "16k"
            },
            "openai:gpt-4o": { # Изменено
                "provider": "OpenAI",
                "description": "Новейшая модель GPT-4 Omni",
                "context_length": "128k"
            },
            "openai:gpt-4": { # Изменено
                "provider": "OpenAI",
                "description": "Продвинутая модель GPT-4",
                "context_length": "8k"
            },
            "openai:gpt-3.5-turbo": { # Изменено
                "provider": "OpenAI",
                "description": "Быстрая модель GPT-3.5",
                "context_length": "16k"
            }
        }
        
        return model_info.get(model_full_id, { # Изменено
            "provider": "Unknown",
            "description": "Неизвестная модель",
            "context_length": "Unknown"
        })

    def generate_html_from_presentation(self, presentation_data: Dict[str, Any], 
                                       website_structure: Dict[str, Any], 
                                       telegram_contact: str = "@company_contact") -> str:
        """
        Генерирует HTML код сайта на основе данных презентации
        """
        if self.logger:
            self.logger.info("LLMService: Генерация HTML из презентации")
        
        try:
            company_name = presentation_data.get('company_name', 'Ваша компания')
            colors = presentation_data.get('colors', ['#007bff', '#6c757d'])
            primary_color = colors[0] if colors else '#007bff'
            
            sections_html = []
            
            # Генерируем HTML для каждой секции
            for section in website_structure.get('sections', []):
                section_type = section.get('type', 'section')
                title = section.get('title', '')
                content = section.get('content', '')
                
                if section_type == 'hero':
                    sections_html.append(f"""
                    <section class="hero">
                        <div class="container">
                            <h1>{title}</h1>
                            <p>{content}</p>
                            <a href="https://t.me/{telegram_contact.replace('@', '')}" class="buy-button" target="_blank">
                                Связаться в Telegram
                            </a>
                        </div>
                    </section>
                    """)
                elif section_type == 'contact':
                    sections_html.append(f"""
                    <section class="section contact">
                        <div class="container text-center">
                            <h2>{title}</h2>
                            <p>{content}</p>
                            <a href="https://t.me/{telegram_contact.replace('@', '')}" class="buy-button" target="_blank">
                                Купить в Telegram
                            </a>
                        </div>
                    </section>
                    """)
                else:
                    sections_html.append(f"""
                    <section class="section">
                        <div class="container">
                            <h2>{title}</h2>
                            <p>{content}</p>
                        </div>
                    </section>
                    """)
            
            # Собираем полный HTML
            html_template = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{company_name}</title>
                <link rel="stylesheet" href="styles.css">
            </head>
            <body>
                {''.join(sections_html)}
                
                <footer style="background: #333; color: white; text-align: center; padding: 20px 0;">
                    <div class="container">
                        <p>&copy; 2025 {company_name}. Все права защищены.</p>
                        <p>Связаться с нами: <a href="https://t.me/{telegram_contact.replace('@', '')}" 
                           style="color: {primary_color};">{telegram_contact}</a></p>
                    </div>
                </footer>
            </body>
            </html>
            """
            
            if self.logger:
                self.logger.info("LLMService: HTML успешно сгенерирован")
            
            return html_template.strip()
            
        except Exception as e:
            error_msg = f"LLMService: Ошибка генерации HTML: {e}"
            if self.logger:
                self.logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def generate_response(self, prompt: str) -> str:
        """
        Генерирует ответ от LLM на основе промпта
        """
        if self.logger:
            self.logger.info(f"LLMService: Генерация ответа для промпта (первые 100 символов): {prompt[:100]}...")
        
        try:
            if not self.current_model_type:
                raise ValueError("Не установлена текущая модель")
            
            # Формируем запрос в зависимости от провайдера
            if self.current_model_type == "openai":
                response = self._make_openai_request([
                    {"role": "user", "content": prompt}
                ])
            elif self.current_model_type == "deepseek":
                response = self._make_deepseek_request([
                    {"role": "user", "content": prompt}
                ])
            else:
                raise ValueError(f"Неподдерживаемый тип модели: {self.current_model_type}")
            
            if self.logger:
                self.logger.info("LLMService: Ответ успешно получен")
            
            return response
            
        except Exception as e:
            error_msg = f"LLMService: Ошибка генерации ответа: {e}"
            if self.logger:
                self.logger.error(error_msg)
            raise RuntimeError(error_msg) from e
