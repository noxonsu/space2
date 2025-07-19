"""
Продукт: Создание презентационных сайтов по брендбуку
"""

import os
import json
import hashlib
import re
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from ..products import BaseProduct
from ..llm_service import LLMService
from ..parsing_service import ParsingService
from ..cache_service import CacheService
from ..product_data_loader import ProductDataLoader


class SitePresentationsProduct(BaseProduct):
    """Продукт для создания презентационных сайтов по брендбуку"""
    
    def __init__(self, llm_service: LLMService, parsing_service: ParsingService, cache_service: CacheService):
        # Загружаем данные из YAML-файла
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("site_presentations")
        
        super().__init__(
            product_id=self.product_data["product_id"],
            name=self.product_data["name"],
            description=self.product_data["description"]
        )
        self.llm_service = llm_service
        self.parsing_service = parsing_service
        self.cache_service = cache_service
        
        # Устанавливаем демо-данные из файла
        self.demo_data = self.product_data.get("demo_data", {})
    
    def get_product_info(self) -> Dict[str, Any]:
        """Информация о продукте для SEO-страниц"""
        product_info = self.product_data.get("product_info", {})
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "key_benefits": product_info.get("key_benefits", []),
            "target_audience": product_info.get("target_audience", []),
            "use_cases": product_info.get("use_cases", []),
            "demo_available": product_info.get("demo_available", True),
            "screenshots": product_info.get("screenshots", []),
            "pricing": product_info.get("pricing", {})
        }
    
    def get_input_interface_description(self) -> Dict[str, Any]:
        """Описывает ожидаемый формат входных данных для execute_demo"""
        return self.product_data.get("interfaces", {}).get("input", {})
    
    def get_output_interface_description(self) -> Dict[str, Any]:
        """Описывает формат выходных данных из execute_demo"""
        return self.product_data.get("interfaces", {}).get("output", {})
    
    def get_seo_keywords(self) -> List[str]:
        """Возвращает список ключевых слов для SEO"""
        return self.product_data.get("seo", {}).get("keywords", [])
    
    def get_demo_content(self) -> Dict[str, Any]:
        """Возвращает демо-контент для показа на SEO-странице"""
        return self.product_data.get("seo", {}).get("demo_content", {})
    
    def execute_demo(self, input_data: Any) -> Dict[str, Any]:
        """Выполняет создание презентационного сайта"""
        try:
            # Валидация входных данных
            is_valid, error = self._validate_input_data(input_data)
            if not is_valid:
                return {"error": error, "success": False}
            
            # Извлекаем данные
            presentation_files = input_data.get('presentation_files', [])
            telegram_contact = input_data.get('telegram_contact', '')
            company_name = input_data.get('company_name', '')
            
            # Парсим презентацию и брендбук
            presentation_data = self.parsing_service.parse_presentation(presentation_files)
            
            # Дополняем данными от пользователя
            presentation_data.update({
                'telegram_contact': self._extract_telegram_contact(telegram_contact),
                'company_name': company_name or presentation_data.get('company_name', 'Ваша компания')
            })
            
            # Генерируем структуру сайта
            website_structure = self._generate_website_structure(presentation_data)
            
            # Генерируем HTML, CSS и мета-данные
            html_content = self.llm_service.generate_html_from_presentation(
                presentation_data, 
                website_structure,
                telegram_contact=presentation_data['telegram_contact']
            )
            
            css_content = self._generate_css_from_brandbook(presentation_data)
            seo_meta = self._generate_seo_meta(presentation_data)
            
            # Объединяем HTML с SEO метаданными
            html_content = self._inject_seo_meta(html_content, seo_meta)
            
            # Сохраняем файлы и получаем URL
            website_url = self._save_website_files(
                html_content, 
                css_content, 
                presentation_data.get('assets', {})
            )
            
            return {
                "success": True,
                "website_url": website_url,
                "seo_meta": seo_meta,
                "sections_count": len(website_structure.get('sections', [])),
                "telegram_contact": presentation_data['telegram_contact'],
                "company_name": presentation_data['company_name']
            }
            
        except Exception as e:
            return {
                "error": f"Ошибка создания сайта: {str(e)}",
                "success": False
            }
    
    def _validate_input_data(self, input_data: Any) -> Tuple[bool, Optional[str]]:
        """Валидирует входные данные"""
        if not isinstance(input_data, dict):
            return False, "Входные данные должны быть в формате объекта"
        
        if not input_data.get('presentation_files'):
            return False, "Файлы презентации не предоставлены (presentation_files)"
        
        if not isinstance(input_data['presentation_files'], list):
            return False, "presentation_files должен быть массивом"
        
        if len(input_data['presentation_files']) == 0:
            return False, "Необходимо предоставить хотя бы один файл презентации"
        
        return True, None
    
    def _extract_telegram_contact(self, contact: str) -> str:
        """Извлекает и нормализует Telegram контакт"""
        if not contact:
            return "@company_contact"
        
        # Удаляем URL части если есть
        if contact.startswith('https://t.me/'):
            contact = contact.replace('https://t.me/', '@')
        elif contact.startswith('t.me/'):
            contact = contact.replace('t.me/', '@')
        
        # Добавляем @ если его нет
        if not contact.startswith('@'):
            contact = '@' + contact
        
        # Удаляем недопустимые символы
        contact = re.sub(r'[^@a-zA-Z0-9_]', '', contact)
        
        return contact
    
    def _generate_website_structure(self, presentation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует структуру сайта на основе презентации"""
        text_content = presentation_data.get('text_content', '')
        
        # Базовая структура
        structure = {
            "sections": [
                {
                    "type": "hero",
                    "title": presentation_data.get('company_name', 'Ваша компания'),
                    "content": self._extract_hero_content(text_content)
                },
                {
                    "type": "about",
                    "title": "О нас",
                    "content": self._extract_about_content(text_content)
                },
                {
                    "type": "services",
                    "title": "Услуги",
                    "content": self._extract_services_content(text_content)
                },
                {
                    "type": "contact",
                    "title": "Связаться с нами",
                    "content": f"Свяжитесь с нами в Telegram: {presentation_data.get('telegram_contact', '@company_contact')}"
                }
            ],
            "styles": {
                "colors": presentation_data.get('colors', ['#007bff', '#6c757d']),
                "fonts": presentation_data.get('fonts', ['Arial', 'sans-serif']),
                "layout": "single-page"
            }
        }
        
        return structure
    
    def _extract_hero_content(self, text: str) -> str:
        """Извлекает контент для главного блока"""
        lines = text.split('\n')
        if lines:
            return lines[0][:200] + "..." if len(lines[0]) > 200 else lines[0]
        return "Добро пожаловать в нашу компанию"
    
    def _extract_about_content(self, text: str) -> str:
        """Извлекает контент для блока 'О нас'"""
        # Ищем упоминания о компании
        keywords = ['о нас', 'компани', 'команд', 'мисси', 'ценност']
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in keywords):
                return line[:300] + "..." if len(line) > 300 else line
        
        return "Мы - профессиональная команда, готовая решить ваши задачи."
    
    def _extract_services_content(self, text: str) -> str:
        """Извлекает контент для блока услуг"""
        keywords = ['услуг', 'сервис', 'решени', 'продукт', 'предлага']
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in keywords):
                return line[:300] + "..." if len(line) > 300 else line
        
        return "Мы предлагаем широкий спектр качественных услуг."
    
    def _generate_css_from_brandbook(self, presentation_data: Dict[str, Any]) -> str:
        """Генерирует CSS стили на основе брендбука"""
        colors = presentation_data.get('colors', ['#007bff', '#6c757d'])
        fonts = presentation_data.get('fonts', ['Arial', 'sans-serif'])
        
        primary_color = colors[0] if colors else '#007bff'
        secondary_color = colors[1] if len(colors) > 1 else '#6c757d'
        font_family = fonts[0] if fonts else 'Arial'
        
        css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: '{font_family}', sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        .hero {{
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            color: white;
            padding: 100px 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}
        
        .section {{
            padding: 60px 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .buy-button {{
            display: inline-block;
            background: {primary_color};
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2rem;
            margin: 20px 0;
            transition: background 0.3s;
        }}
        
        .buy-button:hover {{
            background: {secondary_color};
        }}
        
        h2 {{
            color: {primary_color};
            margin-bottom: 20px;
        }}
        
        .text-center {{
            text-align: center;
        }}
        """
        
        return css
    
    def _generate_seo_meta(self, presentation_data: Dict[str, Any]) -> Dict[str, str]:
        """Генерирует SEO метаданные"""
        company_name = presentation_data.get('company_name', 'Компания')
        description = presentation_data.get('text_content', '')[:160]
        
        return {
            "title": f"{company_name} - Официальный сайт",
            "description": description or f"Официальный сайт компании {company_name}. Узнайте больше о наших услугах.",
            "keywords": f"{company_name}, услуги, официальный сайт, купить, заказать",
            "og:title": f"{company_name}",
            "og:description": description or f"Узнайте больше о {company_name}",
            "og:type": "website"
        }
    
    def _inject_seo_meta(self, html_content: str, seo_meta: Dict[str, str]) -> str:
        """Внедряет SEO метаданные в HTML"""
        meta_tags = []
        
        for key, value in seo_meta.items():
            if key.startswith('og:'):
                meta_tags.append(f'<meta property="{key}" content="{value}">')
            elif key == 'keywords':
                meta_tags.append(f'<meta name="{key}" content="{value}">')
            elif key == 'description':
                meta_tags.append(f'<meta name="{key}" content="{value}">')
            elif key == 'title':
                # Заменяем или добавляем title
                if '<title>' in html_content:
                    html_content = re.sub(r'<title>.*?</title>', f'<title>{value}</title>', html_content)
                else:
                    meta_tags.append(f'<title>{value}</title>')
        
        # Вставляем мета-теги в head
        if '<head>' in html_content:
            meta_string = '\n    '.join(meta_tags)
            html_content = html_content.replace('<head>', f'<head>\n    {meta_string}')
        
        return html_content
    
    def _save_website_files(self, html_content: str, css_content: str, assets: Dict[str, Any]) -> str:
        """Сохраняет файлы сайта и возвращает URL"""
        # Генерируем уникальное имя для сайта
        site_id = hashlib.md5(html_content.encode()).hexdigest()[:8]
        
        # Определяем путь для сохранения
        sites_dir = Path(__file__).parent.parent.parent.parent.parent / "public" / "sites" / site_id
        sites_dir.mkdir(parents=True, exist_ok=True)
        
        # Сохраняем HTML
        with open(sites_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Сохраняем CSS
        with open(sites_dir / "styles.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Сохраняем ассеты (изображения и т.д.)
        if assets:
            assets_dir = sites_dir / "assets"
            assets_dir.mkdir(exist_ok=True)
            
            for filename, content in assets.items():
                with open(assets_dir / filename, 'wb') as f:
                    f.write(content)
        
        # Возвращаем URL сайта
        return self._get_website_url(site_id)
    
    def _get_website_url(self, site_id: str) -> str:
        """Генерирует URL для созданного сайта"""
        # Проверяем, работаем ли в Codespaces
        codespace_name = os.getenv('CODESPACE_NAME')
        if codespace_name:
            # URL для Codespaces
            return f"https://{codespace_name}-5001.app.github.dev/sites/{site_id}/"
        else:
            # Локальный URL
            return f"http://127.0.0.1:5001/sites/{site_id}/"
