import os
import json
from datetime import datetime
from ..services.llm_service import LLMService # Используем существующий LLMService

class SeoPromptService:
    def __init__(self, llm_service: LLMService, content_base_path: str):
        self.llm_service = llm_service
        self.content_base_path = content_base_path
        # self.output_base_path = os.path.join(content_base_path, '..', 'llm_results') # Старая директория для результатов LLM
        # Новая логика: результаты сохраняются в поддиректории SEO-страницы
        # Директория для результатов будет определяться динамически в run_openai_prompt_for_page
        
        # Убедимся, что базовая директория контента существует
        os.makedirs(self.content_base_path, exist_ok=True)

    def _get_logger(self):
        from flask import current_app
        return current_app.logger if current_app else None

    def run_openai_prompt_for_page(self, slug: str, prompt_template: str, output_filename_prefix: str, page_data: dict) -> dict:
        logger = self._get_logger()
        
        page_dir = os.path.join(self.content_base_path, slug)
        contract_file_path = os.path.join(page_dir, page_data.get("contract_file", "generated_contract.txt"))

        contract_text = ""
        if os.path.exists(contract_file_path):
            try:
                with open(contract_file_path, 'r', encoding='utf-8') as f:
                    contract_text = f.read()
                if logger:
                    logger.info(f"SeoPromptService: Текст договора для {slug} загружен (длина: {len(contract_text)}).")
            except Exception as e:
                if logger:
                    logger.error(f"SeoPromptService: Ошибка при чтении файла договора {contract_file_path} для {slug}: {e}", exc_info=True)
                contract_text = "" # Сбрасываем текст, если есть ошибка чтения
        else:
            if logger:
                logger.warning(f"SeoPromptService: Файл договора не найден для SEO-страницы {slug}: {contract_file_path}")

        # Заменяем заполнители в промпте
        # Убедимся, что page_data содержит все необходимые ключи, предоставляя пустые строки по умолчанию
        page_title = page_data.get("title", "")
        page_keywords = ", ".join(page_data.get("meta_keywords", []))
        page_description = page_data.get("meta_description", "")

        formatted_prompt = prompt_template.replace("{{PAGE_TITLE}}", page_title) \
                                          .replace("{{PAGE_KEYWORDS}}", page_keywords) \
                                          .replace("{{PAGE_DESCRIPTION}}", page_description) \
                                          .replace("{{CONTRACT_TEXT}}", contract_text)

        if logger:
            logger.info(f"SeoPromptService: Запуск промпта для страницы '{slug}'.")
            logger.info(f"SeoPromptService: Данные страницы: Title='{page_title}', Keywords='{page_keywords}', Description='{page_description}'")
            logger.info(f"SeoPromptService: Длина текста договора: {len(contract_text)}")
            logger.debug(f"SeoPromptService: Исходный промпт: {prompt_template[:500]}...")
            logger.debug(f"SeoPromptService: Сформатированный промпт (первые 500): {formatted_prompt[:500]}...")

        llm_output = ""
        try:
            llm_output = self.llm_service.generate_text(formatted_prompt) # Исправлено: get_completion на generate_text
            if not llm_output:
                logger.warning(f"SeoPromptService: LLM вернул пустой ответ для страницы '{slug}'.")
                llm_output = "LLM вернул пустой ответ."
        except Exception as e:
            logger.error(f"SeoPromptService: Ошибка при получении ответа от LLM для страницы '{slug}': {e}", exc_info=True)
            llm_output = f"Ошибка при получении ответа от LLM: {e}"
            raise # Перебрасываем исключение, чтобы оно было поймано в seo_tools.py

        # Сохраняем результат в папке SEO-страницы
        output_dir = os.path.join(self.content_base_path, slug)
        os.makedirs(output_dir, exist_ok=True) # Убедимся, что директория SEO-страницы существует

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{output_filename_prefix}_{timestamp}.txt" # Имя файла без слага, так как он уже в пути
        output_file_path = os.path.join(output_dir, output_filename)

        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(f"--- Metadata ---\n")
                f.write(f"Page Slug: {slug}\n")
                f.write(f"Page Title: {page_data.get('title', '')}\n")
                f.write(f"Prompt Used:\n{prompt_template}\n")
                f.write(f"Formatted Prompt:\n{formatted_prompt}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"--- LLM Output ---\n")
                f.write(llm_output)
            
            if logger:
                logger.info(f"SeoPromptService: Результат для страницы '{slug}' сохранен в: {output_file_path}")
        except Exception as e:
            logger.error(f"SeoPromptService: Ошибка при сохранении результата для страницы '{slug}': {e}", exc_info=True)
            raise # Перебрасываем исключение

        return {
            "llm_output": llm_output,
            "output_file_path": output_file_path
        }
