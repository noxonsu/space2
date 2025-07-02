import unittest
from unittest.mock import Mock, patch, mock_open
import sys
import os
import yaml

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.backend.services.seo_service import SeoService
from src.backend.services.products import product_registry
from src.backend.services.products.contract_analysis import ContractAnalysisProduct
from src.backend.services.products.news_analysis import NewsAnalysisProduct


class TestSeoServiceWithProducts(unittest.TestCase):
    def setUp(self):
        """Настройка для каждого теста"""
        # Создание мок-сервисов
        self.mock_llm_service = Mock()
        self.mock_llm_service.segment_text_into_paragraphs.return_value = ["Тестовый абзац"]
        self.mock_llm_service.analyze_paragraph_in_context.return_value = "Тестовый анализ"
        
        self.mock_parsing_service = Mock()
        self.mock_cache_service = Mock()
        self.mock_cache_service.get_cached_paragraph_analysis.return_value = None
        self.mock_cache_service._generate_hash.return_value = "test_hash"
        
        # Создание SeoService
        self.seo_service = SeoService(
            llm_service=self.mock_llm_service,
            parsing_service=self.mock_parsing_service,
            content_base_path='/test/content/seo_pages'
        )
        
        # Регистрация тестовых продуктов
        self.contract_product = ContractAnalysisProduct(
            self.mock_llm_service, 
            self.mock_parsing_service, 
            self.mock_cache_service
        )
        self.news_product = NewsAnalysisProduct(self.mock_llm_service)
        
        product_registry.register_product(self.contract_product)
        product_registry.register_product(self.news_product)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_product_for_page_from_source_md(self, mock_file_open, mock_exists):
        """Тест получения продукта из метаданных source.md"""
        mock_exists.return_value = True
        
        # Мокаем содержимое source.md для анализа новостей
        source_content = """---
title: "Мониторинг новостей ВЭД"
product_id: "news_analysis"
meta_keywords: ["мониторинг", "новости"]
---

# Содержимое страницы
"""
        mock_file_open.return_value.read.return_value = source_content
        
        # Тестируем получение продукта
        product = self.seo_service.get_product_for_page('monitoring-ved-novostey')
        
        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, 'news_analysis')
        self.assertEqual(product.name, 'Мониторинг и анализ новостей')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_product_for_page_contract_analysis(self, mock_file_open, mock_exists):
        """Тест получения продукта для анализа договоров"""
        mock_exists.return_value = True
        
        # Мокаем содержимое source.md для анализа договоров
        source_content = """---
title: "Анализ договора аренды"
product_id: "contract_analysis"
meta_keywords: ["анализ", "договор", "аренда"]
---

# Анализ договора аренды
"""
        mock_file_open.return_value.read.return_value = source_content
        
        # Тестируем получение продукта
        product = self.seo_service.get_product_for_page('arendy')
        
        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, 'contract_analysis')
        self.assertEqual(product.name, 'Анализ договоров с ИИ')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_page_data_with_product_info(self, mock_file_open, mock_exists):
        """Тест получения данных страницы с информацией о продукте"""
        mock_exists.return_value = True
        
        source_content = """---
title: "Мониторинг новостей ВЭД"
product_id: "news_analysis"
meta_description: "Автоматический мониторинг новостей"
meta_keywords: ["мониторинг", "новости", "ВЭД"]
main_keyword: "мониторинг новостей ВЭД"
related_keywords: ["анализ новостей", "ВЭД мониторинг"]
created_at: "2025-07-02"
---

# Мониторинг новостей ВЭД

Содержимое страницы о мониторинге новостей.
"""
        mock_file_open.return_value.read.return_value = source_content
        
        # Тестируем получение данных страницы
        page_data = self.seo_service.get_page_data('monitoring-ved-novostey')
        
        self.assertEqual(page_data['slug'], 'monitoring-ved-novostey')
        self.assertEqual(page_data['title'], 'Мониторинг новостей ВЭД')
        self.assertEqual(page_data['product_id'], 'news_analysis')
        self.assertIn('product_info', page_data)
        self.assertIn('demo_content', page_data)
        self.assertTrue(page_data['demo_available'])
        
        # Проверяем информацию о продукте
        product_info = page_data['product_info']
        self.assertEqual(product_info['product_id'], 'news_analysis')
        self.assertEqual(product_info['name'], 'Мониторинг и анализ новостей')

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_seo_page_with_product(self, mock_file_open, mock_makedirs):
        """Тест создания SEO-страницы с привязкой к продукту"""
        # Тестируем создание страницы для анализа новостей
        result = self.seo_service.create_seo_page_with_product(
            slug='test-news-page',
            title='Тестовая страница новостей',
            keywords=['мониторинг', 'новости', 'тест'],
            product_id='news_analysis',
            meta_description='Тестовое описание'
        )
        
        self.assertTrue(result)
        
        # Проверяем, что файл был создан
        mock_file_open.assert_called()
        
        # Проверяем содержимое файла
        written_content = mock_file_open().write.call_args[0][0]
        self.assertIn('product_id: news_analysis', written_content)
        self.assertIn('title: Тестовая страница новостей', written_content)
        self.assertIn('мониторинг', written_content)

    def test_create_seo_page_invalid_product(self):
        """Тест создания страницы с несуществующим продуктом"""
        with self.assertRaises(ValueError) as context:
            self.seo_service.create_seo_page_with_product(
                slug='test-page',
                title='Тест',
                keywords=['тест'],
                product_id='non_existent_product'
            )
        
        self.assertIn('Продукт non_existent_product не найден', str(context.exception))

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.backend.services.seo_service.render_template')
    def test_render_seo_page_template_selection(self, mock_render_template, mock_file_open, mock_exists):
        """Тест выбора правильного шаблона в зависимости от продукта"""
        mock_exists.return_value = True
        mock_render_template.return_value = "<html>Test</html>"
        
        # Тест для анализа новостей
        source_content_news = """---
title: "Мониторинг новостей"
product_id: "news_analysis"
---
Содержимое
"""
        mock_file_open.return_value.read.return_value = source_content_news
        
        self.seo_service.render_seo_page('test-news')
        
        # Проверяем, что использовался правильный шаблон
        mock_render_template.assert_called()
        call_args = mock_render_template.call_args
        template_name = call_args[0][0]
        self.assertEqual(template_name, 'news_analysis_template.html')
        
        # Сброс мока
        mock_render_template.reset_mock()
        
        # Тест для анализа договоров
        source_content_contract = """---
title: "Анализ договора"
product_id: "contract_analysis"
---
Содержимое
"""
        mock_file_open.return_value.read.return_value = source_content_contract
        
        self.seo_service.render_seo_page('test-contract')
        
        # Проверяем, что использовался правильный шаблон
        mock_render_template.assert_called()
        call_args = mock_render_template.call_args
        template_name = call_args[0][0]
        self.assertEqual(template_name, 'index_template.html')

    def tearDown(self):
        """Очистка после каждого теста"""
        product_registry._products.clear()
        product_registry._product_seo_mapping.clear()


if __name__ == '__main__':
    unittest.main()
