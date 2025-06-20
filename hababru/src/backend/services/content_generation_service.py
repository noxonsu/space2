import os
import yaml
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Импортируем сервисы, которые будут использоваться
from .llm_service import LLMService

class ContentGenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_all_for_keyword(self, keyword: str, slug: str, seo_page_dir: str):
        print(f"ContentGenerationService: Начинаем генерацию для '{keyword}'")
        
        # Формируем более описательный ключ для LLM промптов
        # Если в keyword уже есть "договор", не добавляем "договора"
        if "договор" in keyword.lower():
            llm_keyword_base = keyword
        else:
            llm_keyword_base = f"договора {keyword}" # This is for the contract type, e.g., "договора ипотеки"

        # Keyword for generating the contract text itself (e.g., "договор ипотеки")
        contract_generation_keyword = llm_keyword_base 
        # Keyword for SEO content generation (e.g., "проверка договора ипотеки")
        prompt_keyword_seo = f"проверка {llm_keyword_base}"


        # 1. Генерация текста договора
        contract_text = self._generate_contract_text(contract_generation_keyword)
        contract_file_path = os.path.join(seo_page_dir, 'generated_contract.txt')
        with open(contract_file_path, 'w', encoding='utf-8') as f:
            f.write(contract_text)
        print(f"Сгенерирован и сохранен договор: {contract_file_path}")

        # 2. Получение/Генерация ключевых слов
        meta_keywords, related_keywords = self._get_or_generate_keywords(prompt_keyword_seo)
        print(f"Получены/сгенерированы meta_keywords: {meta_keywords}")
        print(f"Получены/сгенерированы related_keywords: {related_keywords}")

        # 3. Генерация Meta Description
        meta_description = self._generate_meta_description(prompt_keyword_seo, meta_keywords)
        print(f"Сгенерировано meta_description: {meta_description}")

        # 4. Генерация основного текста страницы
        page_text_content = self._generate_page_text_content(prompt_keyword_seo)
        print(f"Сгенерирован основной текст страницы.")

        # 5. Сборка source.md
        self._assemble_source_md(
            seo_page_dir,
            keyword, # Используем оригинальный короткий keyword для title шаблона и main_keyword
            meta_keywords,
            meta_description,
            related_keywords,
            os.path.basename(contract_file_path), # Только имя файла
            page_text_content
        )
        print(f"Собран source.md в {seo_page_dir}")

    def _generate_contract_text(self, prompt_keyword: str) -> str:
        # Modified prompt to request a shorter contract
        prompt = f"Сгенерируй типовой текст договора, который соответствует запросу '{prompt_keyword}'. Договор должен быть юридически корректным, но упрощенным для примера. Договор должен быть кратким, содержать только основные пункты и не превышать 300 слов. Включи основные разделы: предмет договора, права и обязанности сторон, срок действия, ответственность сторон, порядок разрешения споров, реквизиты сторон. Заполни все поля договора тестовыми данными (ФИО, адреса, паспортные данные, названия компаний, суммы и т.д.) так, чтобы не было прочерков. Договор должен быть на русском языке. В начале договора добавь примечание: 'Договор (данные придуманы)'."
        response = self.llm_service.generate_text(prompt)
        return response

    def _get_or_generate_keywords(self, prompt_keyword: str):
        print(f"Генерируем ключевые слова через LLM для '{prompt_keyword}' (Яндекс.Вордстат отключен).")
        meta_keywords = self._generate_keywords_with_llm(prompt_keyword, "meta")
        related_keywords = self._generate_keywords_with_llm(prompt_keyword, "related")
        
        return meta_keywords, related_keywords

    def _generate_keywords_with_llm(self, prompt_keyword: str, type: str) -> list:
        if type == "meta":
            prompt = f"Сгенерируй 3-5 мета-ключевых слов для SEO-страницы по теме '{prompt_keyword}'. Ключевые слова должны быть релевантными, высокочастотными и фокусироваться на анализе и проверке условий договора. Перечисли их через запятую."
        elif type == "related":
            prompt = f"Сгенерируй 5-7 связанных ключевых слов для SEO-страницы по теме '{prompt_keyword}'. Эти слова должны быть смежными по смыслу, полезными для расширения семантики и фокусироваться на юридической экспертизе и консультациях по договору. Перечисли их через запятую."
        else:
            return []
        
        response = self.llm_service.generate_text(prompt)
        # Простая попытка распарсить строку с ключевыми словами
        return [k.strip() for k in response.split(',') if k.strip()]

    def _generate_meta_description(self, prompt_keyword: str, meta_keywords: list) -> str:
        keywords_string = ', '.join(meta_keywords)
        prompt = f"Сгенерируй мета-описание (до 160 символов) для SEO-страницы по теме '{prompt_keyword}'. Описание должно быть привлекательным, информативным и акцентировать внимание на онлайн проверке и анализе договора нейросетью. Включи в него ключевые слова: {keywords_string}."
        response = self.llm_service.generate_text(prompt)
        return response[:160] # Обрезаем до 160 символов

    def _generate_page_text_content(self, prompt_keyword: str) -> str:
        prompt = f"Напиши небольшой SEO-оптимизированный текст (200-300 слов) для страницы, посвященной '{prompt_keyword}'. Текст должен быть информативным, полезным для пользователя, содержать ключевое слово '{prompt_keyword}' и рассказывать о преимуществах онлайн проверки и анализа соответствующего типа договора с помощью нейросети. Он будет размещен под формой анализа договора."
        response = self.llm_service.generate_text(prompt)
        return response

    def _assemble_source_md(self, seo_page_dir: str, title: str, meta_keywords: list, 
                             meta_description: str, related_keywords: list, 
                             contract_filename: str, page_text_content: str):
        
        # Используем title как main_keyword для консистентности
        
        # Формируем новый title по шаблону
        new_title_template = "Проверка договора {keyword} онлайн нейросетью. Анализ условий и консультаця"
        # title здесь - это исходный keyword (тип договора)
        formatted_title = new_title_template.format(keyword=title.lower())


        front_matter = {
            "title": formatted_title, # Используем новый отформатированный title
            "meta_keywords": meta_keywords,
            "meta_description": meta_description,
            "related_keywords": related_keywords,
            "contract_file": contract_filename,
            "main_keyword": title # main_keyword остается исходным ключевым словом (типом договора)
        }

        md_content = f"---\n{yaml.dump(front_matter, allow_unicode=True, sort_keys=False)}---\n\n{page_text_content}"
        
        source_md_path = os.path.join(seo_page_dir, 'source.md')
        with open(source_md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
