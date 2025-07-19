import io
import os
import re
import json
from typing import Dict, List, Any
from markitdown import MarkItDown
from flask import current_app # Для логирования

from .llm_service import LLMService # Импортируем LLMService

class ParsingService:
    def __init__(self, llm_service: LLMService): # Изменено на llm_service
        self.llm_service = llm_service # Изменено на llm_service

    def _get_logger(self):
        return current_app.logger if current_app else None

    def parse_document_to_markdown(self, file_stream, filename: str) -> str:
        """
        Конвертирует документ (PDF, DOC, DOCX) в Markdown с помощью MarkItDown.
        :param file_stream: Поток байтов файла.
        :param filename: Имя файла (для определения типа, если необходимо).
        :return: Текст в формате Markdown или None в случае ошибки.
        """
        logger = self._get_logger()
        if logger:
            logger.info(f"ParsingService: Попытка конвертации файла '{filename}' в Markdown.")
        try:
            converter = MarkItDown()
            markdown_result = converter.convert_stream(file_stream, filename=filename)
            if logger:
                logger.info(f"ParsingService: Файл '{filename}' успешно сконвертирован в Markdown.")
            return markdown_result.markdown
        except Exception as e:
            if logger:
                logger.error(f"ParsingService: Ошибка при конвертации файла '{filename}' в Markdown с помощью MarkItDown: {e}")
            else:
                print(f"Ошибка при конвертации файла '{filename}' в Markdown с помощью MarkItDown: {e}")
            return None

    def segment_text_into_paragraphs(self, text: str) -> list:
        """
        Разбивает текст на пункты/абзацы, используя DeepSeekService.
        :param text: Входной текст.
        :return: Список пунктов/абзацев.
        """
        logger = self._get_logger()
        if logger:
            logger.info(f"ParsingService: Сегментация текста на пункты с помощью LLMService (первые 250 символов): '{text[:250]}...'")
        
        if not text:
            return []

        try:
            paragraphs = self.llm_service.segment_text_into_paragraphs(text) # Изменено на llm_service
            if logger:
                logger.info(f"ParsingService: Сегментация текста завершена, получено {len(paragraphs)} пунктов.")
            return paragraphs
        except Exception as e:
            error_msg = f"ParsingService: Ошибка при сегментации текста на пункты с LLMService: {e}" # Изменено на LLMService
            if logger:
                logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def parse_presentation(self, presentation_files: List[str]) -> Dict[str, Any]:
        """
        Парсит файлы презентации и извлекает контент для создания сайта.
        :param presentation_files: Список путей к файлам презентации
        :return: Словарь с извлеченными данными
        """
        logger = self._get_logger()
        if logger:
            logger.info(f"ParsingService: Начинаем парсинг презентации из {len(presentation_files)} файлов")
        
        result = {
            "text_content": "",
            "company_name": "",
            "colors": [],
            "fonts": [],
            "assets": {},
            "design_elements": [],
            "structure": []
        }
        
        try:
            all_text_content = []
            
            for file_path in presentation_files:
                if logger:
                    logger.info(f"ParsingService: Обрабатываем файл {file_path}")
                
                # Симуляция чтения файла (в реальности здесь будет чтение из uploaded files)
                file_content = self._extract_content_from_file(file_path)
                
                if file_content:
                    all_text_content.append(file_content)
            
            # Объединяем весь текстовый контент
            combined_text = "\n\n".join(all_text_content)
            result["text_content"] = combined_text
            
            # Извлекаем данные с помощью LLM
            extracted_data = self._extract_presentation_data_with_llm(combined_text)
            result.update(extracted_data)
            
            if logger:
                logger.info(f"ParsingService: Презентация обработана успешно")
            
            return result
            
        except Exception as e:
            error_msg = f"ParsingService: Ошибка при парсинге презентации: {e}"
            if logger:
                logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def _extract_content_from_file(self, file_path: str) -> str:
        """Извлекает текстовый контент из файла"""
        logger = self._get_logger()
        
        try:
            # Для демо версии возвращаем пример контента
            # В продакшене здесь будет реальное чтение файлов
            if "presentation" in file_path.lower():
                return """
                Компания InnovateTech
                
                О нас:
                Мы - команда экспертов в области разработки инновационных решений.
                Наша миссия - помочь бизнесу достичь новых высот с помощью технологий.
                
                Наши услуги:
                - Разработка веб-приложений
                - Мобильная разработка
                - Консалтинг по цифровой трансформации
                - Автоматизация бизнес-процессов
                
                Контакты:
                Telegram: @innovatetech_bot
                """
            elif "brandbook" in file_path.lower():
                return """
                Брендбук компании:
                Основные цвета: #2E86AB, #A23B72, #F18F01
                Шрифты: Montserrat, Open Sans
                Логотип: logo_main.svg
                """
            else:
                return "Дополнительная информация о компании"
                
        except Exception as e:
            if logger:
                logger.error(f"ParsingService: Ошибка извлечения контента из {file_path}: {e}")
            return ""
    
    def _extract_presentation_data_with_llm(self, text: str) -> Dict[str, Any]:
        """Извлекает структурированные данные из текста презентации с помощью LLM"""
        logger = self._get_logger()
        
        try:
            # Формируем промпт для LLM
            prompt = f"""
            Проанализируй следующий текст презентации и извлеки:
            1. Название компании
            2. Цвета из брендбука (в формате HEX)
            3. Шрифты
            4. Структуру контента
            
            Верни результат в JSON формате:
            {{
                "company_name": "название компании",
                "colors": ["#color1", "#color2"],
                "fonts": ["Font1", "Font2"],
                "structure": ["раздел1", "раздел2"]
            }}
            
            Текст презентации:
            {text}
            """
            
            # Получаем ответ от LLM
            llm_response = self.llm_service.generate_response(prompt)
            
            if logger:
                logger.info(f"ParsingService: Получен ответ от LLM для извлечения данных")
            
            # Пытаемся парсить JSON ответ
            try:
                extracted_data = json.loads(llm_response)
            except json.JSONDecodeError:
                # Если не удалось парсить JSON, извлекаем данные вручную
                extracted_data = self._extract_data_fallback(text)
            
            return extracted_data
            
        except Exception as e:
            if logger:
                logger.error(f"ParsingService: Ошибка извлечения данных с LLM: {e}")
            # Возвращаем fallback данные
            return self._extract_data_fallback(text)
    
    def _extract_data_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback метод для извлечения данных без LLM"""
        # Извлекаем название компании
        company_name = "Ваша компания"
        lines = text.split('\n')
        for line in lines[:5]:  # Проверяем первые 5 строк
            line = line.strip()
            if line and len(line) < 50 and not line.startswith(('О нас', 'Услуги', 'Контакты')):
                company_name = line
                break
        
        # Извлекаем цвета (ищем HEX коды)
        colors = re.findall(r'#[0-9A-Fa-f]{6}', text)
        if not colors:
            colors = ["#007bff", "#6c757d"]  # Дефолтные цвета
        
        # Извлекаем шрифты
        fonts = re.findall(r'(?:шрифт|font)[:\s]*([A-Za-z\s]+)', text, re.IGNORECASE)
        if not fonts:
            fonts = ["Arial", "sans-serif"]  # Дефолтные шрифты
        
        return {
            "company_name": company_name,
            "colors": colors[:3],  # Берем первые 3 цвета
            "fonts": fonts[:2],    # Берем первые 2 шрифта
            "structure": ["hero", "about", "services", "contact"]
        }
