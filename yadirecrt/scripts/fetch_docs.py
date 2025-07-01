#!/usr/bin/env python3
"""
Скрипт для скачивания документации Яндекс.Директ
"""

import scrapy
from scrapy.crawler import CrawlerProcess
import os
import requests
from urllib.parse import urljoin, urlparse
import time
import re

class DirectSpider(scrapy.Spider):
    name = 'direct_spider'
    allowed_domains = ['yandex.ru']
    start_urls = ['https://yandex.ru/dev/direct/doc/ru/intro']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def __init__(self):
        self.visited_urls = set()
        self.base_url = 'https://yandex.ru'
        
    def parse(self, response):
        # Проверяем, что URL еще не был обработан
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)
        
        # Извлекаем заголовок страницы
        title = response.css('title::text').get() or 'Untitled'
        title = re.sub(r'[^\w\s-]', '', title).strip()[:50]
        
        # Создаем имя файла на основе URL
        parsed_url = urlparse(response.url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        
        if not path_parts:
            filename = 'index.md'
        else:
            filename = f"{'_'.join(path_parts[-2:])}.md"
        
        # Убираем недопустимые символы из имени файла
        filename = re.sub(r'[^\w\s.-]', '_', filename)
        
        # Извлекаем основной контент
        content_selectors = [
            '.content-wrapper',
            '.main-content', 
            '.documentation-content',
            '.doc-content',
            'main',
            'article',
            '.content'
        ]
        
        content = None
        for selector in content_selectors:
            content = response.css(selector)
            if content:
                break
        
        if not content:
            # Если не найден основной контент, берем body
            content = response.css('body')
        
        # Преобразуем в текст с сохранением структуры
        markdown_content = self.html_to_markdown(content, response.url, title)
        
        # Создаем директорию и сохраняем файл
        os.makedirs('docs/yandex_direct', exist_ok=True)
        filepath = f'docs/yandex_direct/{filename}'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        self.logger.info(f'Сохранен файл: {filepath}')
        
        # Ищем ссылки на другие страницы документации
        for href in response.css('a::attr(href)').getall():
            if href:
                # Преобразуем относительные ссылки в абсолютные
                full_url = urljoin(response.url, href)
                
                # Проверяем, что это ссылка на документацию Директа
                if ('/dev/direct' in full_url and 
                    'yandex.ru' in full_url and 
                    full_url not in self.visited_urls):
                    yield scrapy.Request(full_url, callback=self.parse)

    def html_to_markdown(self, content_selector, url, title):
        """Простое преобразование HTML в Markdown"""
        
        markdown = f"# {title}\n\n"
        markdown += f"**Источник:** {url}\n\n"
        markdown += f"**Дата скачивания:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += "---\n\n"
        
        # Извлекаем текст с базовым форматированием
        if content_selector:
            # Заголовки
            for h in content_selector.css('h1, h2, h3, h4, h5, h6'):
                level = int(h.root.tag[1])
                text = h.css('::text').getall()
                if text:
                    clean_text = ' '.join(text).strip()
                    markdown += f"{'#' * level} {clean_text}\n\n"
            
            # Параграфы
            for p in content_selector.css('p'):
                text = ' '.join(p.css('::text').getall()).strip()
                if text:
                    markdown += f"{text}\n\n"
            
            # Списки
            for ul in content_selector.css('ul'):
                for li in ul.css('li'):
                    text = ' '.join(li.css('::text').getall()).strip()
                    if text:
                        markdown += f"- {text}\n"
                markdown += "\n"
            
            # Код
            for code in content_selector.css('code, pre'):
                text = ' '.join(code.css('::text').getall()).strip()
                if text:
                    if '\n' in text:
                        markdown += f"```\n{text}\n```\n\n"
                    else:
                        markdown += f"`{text}`\n\n"
            
            # Таблицы (простое преобразование)
            for table in content_selector.css('table'):
                markdown += "\n| Столбец 1 | Столбец 2 |\n|-----------|----------|\n"
                for tr in table.css('tr'):
                    cells = tr.css('td, th')
                    if len(cells) >= 2:
                        cell1 = ' '.join(cells[0].css('::text').getall()).strip()
                        cell2 = ' '.join(cells[1].css('::text').getall()).strip()
                        markdown += f"| {cell1} | {cell2} |\n"
                markdown += "\n"
        
        return markdown

def run_spider():
    """Запуск паука для скачивания документации"""
    print("Начинаем скачивание документации Яндекс.Директ...")
    
    # Создаем директорию для документации
    os.makedirs('docs/yandex_direct', exist_ok=True)
    
    # Настройки для Scrapy
    process = CrawlerProcess({
        'USER_AGENT': 'YandexDirectDocsFetcher/1.0',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 1,
        'LOG_LEVEL': 'INFO'
    })
    
    process.crawl(DirectSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
