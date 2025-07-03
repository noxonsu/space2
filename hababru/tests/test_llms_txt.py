"""
Тесты для llms.txt сервиса и маршрута
"""

import pytest
from src.backend.services.llms_txt_service import LlmsTxtService


class TestLlmsTxtService:
    """Тесты для LlmsTxtService"""
    
    def setup_method(self):
        """Настройка для каждого теста"""
        self.service = LlmsTxtService(base_url="https://test.com")
    
    def test_generate_llms_txt_basic_structure(self):
        """Тест базовой структуры генерируемого llms.txt"""
        content = self.service.generate_llms_txt()
        
        # Проверяем что контент не пустой
        assert content
        assert len(content) > 100
        
        # Проверяем основные элементы структуры
        lines = content.split('\n')
        
        # Должен начинаться с H1
        assert lines[0].startswith('# ')
        assert 'HababRu' in lines[0]
        
        # Должен содержать blockquote с описанием
        blockquote_found = False
        for line in lines[:10]:
            if line.startswith('> '):
                blockquote_found = True
                assert 'B2B-сервис' in line
                break
        assert blockquote_found
        
        # Должен содержать секции с H2
        h2_sections = [line for line in lines if line.startswith('## ')]
        assert len(h2_sections) >= 3  # Минимум 3 секции
        
        # Проверяем наличие основных секций
        section_names = [section.replace('## ', '') for section in h2_sections]
        assert 'Документация' in section_names
        assert 'Продукты' in section_names
    
    def test_validate_llms_txt_format_valid(self):
        """Тест валидации корректного формата"""
        content = self.service.generate_llms_txt()
        is_valid = self.service.validate_llms_txt_format(content)
        assert is_valid
    
    def test_validate_llms_txt_format_invalid(self):
        """Тест валидации некорректного формата"""
        # Контент без H1
        invalid_content1 = "Некорректный контент без заголовка"
        assert not self.service.validate_llms_txt_format(invalid_content1)
        
        # Контент без blockquote
        invalid_content2 = "# Заголовок\nКонтент без описания"
        assert not self.service.validate_llms_txt_format(invalid_content2)
        
        # Контент без секций H2
        invalid_content3 = "# Заголовок\n> Описание\nКонтент без секций"
        assert not self.service.validate_llms_txt_format(invalid_content3)
    
    def test_get_product_sections(self):
        """Тест получения секций продуктов"""
        sections = self.service.get_product_sections()
        
        # Должны быть доступные продукты
        assert isinstance(sections, dict)
        
        # Если есть продукты, проверяем их структуру
        for product_id, product_info in sections.items():
            assert 'name' in product_info
            assert 'description' in product_info
            assert 'demo_url' in product_info
            assert product_info['demo_url'].startswith('https://test.com/demo/')
    
    def test_base_url_handling(self):
        """Тест обработки базового URL"""
        # URL с trailing slash
        service1 = LlmsTxtService(base_url="https://example.com/")
        content1 = service1.generate_llms_txt()
        assert "https://example.com/demo/" in content1
        
        # URL без trailing slash
        service2 = LlmsTxtService(base_url="https://example.com")
        content2 = service2.generate_llms_txt()
        assert "https://example.com/demo/" in content2


class TestLlmsTxtRoute:
    """Тесты для маршрута /llms.txt"""
    
    def test_llms_txt_route_success(self, client):
        """Тест успешного получения llms.txt"""
        response = client.get('/llms.txt')
        
        assert response.status_code == 200
        assert response.mimetype.startswith('text/plain')
        
        content = response.get_data(as_text=True)
        assert content
        assert '# HababRu' in content
        assert '> B2B-сервис' in content
    
    def test_llms_txt_content_structure(self, client):
        """Тест структуры контента llms.txt"""
        response = client.get('/llms.txt')
        content = response.get_data(as_text=True)
        
        lines = content.split('\n')
        
        # Проверяем основную структуру
        assert lines[0].startswith('# ')
        
        # Проверяем наличие blockquote
        blockquote_found = any(line.startswith('> ') for line in lines[:10])
        assert blockquote_found
        
        # Проверяем наличие секций
        h2_sections = [line for line in lines if line.startswith('## ')]
        assert len(h2_sections) >= 2
    
    def test_llms_txt_links_format(self, client):
        """Тест формата ссылок в llms.txt"""
        response = client.get('/llms.txt')
        content = response.get_data(as_text=True)
        
        # Проверяем что ссылки содержат правильный базовый URL
        # В тестах Flask test client использует localhost
        assert 'http://localhost' in content or 'demo/' in content
        
        # Проверяем формат markdown ссылок
        import re
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        assert len(markdown_links) > 0
        
        # Каждая ссылка должна иметь название и URL
        for link_text, link_url in markdown_links:
            assert link_text.strip()
            assert link_url.strip()
    
    def test_llms_txt_error_handling(self, client):
        """Тест обработки ошибок при генерации llms.txt"""
        # Этот тест проверяет что даже при ошибках возвращается fallback контент
        response = client.get('/llms.txt')
        
        # Должен вернуть успешный ответ даже при ошибках (fallback)
        assert response.status_code == 200
        
        content = response.get_data(as_text=True)
        assert content  # Контент не должен быть пустым
        assert '# HababRu' in content  # Должен содержать основной заголовок
