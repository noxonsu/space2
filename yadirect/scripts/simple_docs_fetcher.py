#!/usr/bin/env python3
"""
Альтернативный скрипт для скачивания документации Яндекс.Директ с помощью requests
"""

import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import re

class SimpleDocsFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls = set()
        self.base_url = 'https://yandex.ru'
        
    def fetch_page(self, url):
        """Скачивание одной страницы"""
        try:
            print(f"Скачиваю: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Ошибка при скачивании {url}: {e}")
            return None
    
    def html_to_markdown(self, html, url, title):
        """Простое преобразование HTML в Markdown"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Убираем ненужные элементы
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        markdown = f"# {title}\n\n"
        markdown += f"**Источник:** {url}\n\n"
        markdown += f"**Дата скачивания:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += "---\n\n"
        
        # Ищем основной контент
        content_areas = [
            soup.find('div', class_='content'),
            soup.find('main'),
            soup.find('article'),
            soup.find('div', class_='documentation'),
            soup.find('div', class_='doc-content'),
            soup.find('body')
        ]
        
        content = None
        for area in content_areas:
            if area:
                content = area
                break
        
        if not content:
            content = soup
        
        # Преобразуем в markdown
        for element in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(element.name[1])
            text = element.get_text().strip()
            if text:
                markdown += f"{'#' * level} {text}\n\n"
        
        for element in content.find_all('p'):
            text = element.get_text().strip()
            if text:
                markdown += f"{text}\n\n"
        
        for element in content.find_all('ul'):
            for li in element.find_all('li'):
                text = li.get_text().strip()
                if text:
                    markdown += f"- {text}\n"
            markdown += "\n"
        
        for element in content.find_all(['code', 'pre']):
            text = element.get_text().strip()
            if text:
                if '\n' in text:
                    markdown += f"```\n{text}\n```\n\n"
                else:
                    markdown += f"`{text}`\n\n"
        
        return markdown
    
    def save_page(self, url, html):
        """Сохранение страницы в файл"""
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        title_text = title.get_text() if title else 'Untitled'
        title_text = re.sub(r'[^\w\s-]', '', title_text).strip()[:50]
        
        # Создаем имя файла
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        
        if not path_parts:
            filename = 'index.md'
        else:
            filename = f"{'_'.join(path_parts[-2:])}.md"
        
        filename = re.sub(r'[^\w\s.-]', '_', filename)
        
        # Создаем markdown контент
        markdown_content = self.html_to_markdown(html, url, title_text)
        
        # Сохраняем файл
        os.makedirs('docs/yandex_direct', exist_ok=True)
        filepath = f'docs/yandex_direct/{filename}'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Сохранен: {filepath}")
        return filepath
    
    def find_doc_links(self, html, base_url):
        """Поиск ссылок на документацию"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if ('/dev/direct' in full_url and 
                'yandex.ru' in full_url and 
                full_url not in self.visited_urls):
                links.append(full_url)
        
        return links
    
    def fetch_docs(self, start_url):
        """Основная функция скачивания документации"""
        urls_to_process = [start_url]
        processed = 0
        max_pages = 50  # Ограничение для безопасности
        
        while urls_to_process and processed < max_pages:
            url = urls_to_process.pop(0)
            
            if url in self.visited_urls:
                continue
            
            self.visited_urls.add(url)
            
            html = self.fetch_page(url)
            if not html:
                continue
            
            # Сохраняем страницу
            self.save_page(url, html)
            processed += 1
            
            # Ищем новые ссылки
            new_links = self.find_doc_links(html, url)
            urls_to_process.extend(new_links)
            
            # Задержка между запросами
            time.sleep(1)
        
        print(f"Обработано страниц: {processed}")

def main():
    """Основная функция"""
    print("Запуск альтернативного скрипта скачивания документации...")
    
    # Список основных страниц документации
    start_urls = [
        'https://yandex.ru/dev/direct/doc/ru/intro',
        'https://yandex.ru/dev/direct/doc/ru/concepts/auth',
        'https://yandex.ru/dev/direct/doc/ru/concepts/methods',
        'https://yandex.ru/dev/direct/doc/ru/concepts/errors',
        'https://yandex.ru/dev/direct/doc/ru/reference/',
    ]
    
    fetcher = SimpleDocsFetcher()
    
    for url in start_urls:
        try:
            print(f"\nОбрабатываю раздел: {url}")
            fetcher.fetch_docs(url)
        except Exception as e:
            print(f"Ошибка при обработке {url}: {e}")
    
    print("\nСкачивание завершено!")

if __name__ == "__main__":
    main()
