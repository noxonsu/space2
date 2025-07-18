"""
Тесты для проверки исправлений в генерации SQL запросов
связанных с использованием LIKE вместо = и корректной работой с датами.
"""
import pytest
from unittest.mock import patch, MagicMock
from app import LLMQueryGenerator


class TestSQLQueryFixes:
    """Тестирует исправления в генерации SQL запросов."""
    
    def setup_method(self):
        """Настройка для каждого теста."""
        self.llm_generator = LLMQueryGenerator()
    
    @patch('app.requests.post')
    def test_company_search_uses_like_operator(self, mock_post):
        """Тест проверяет, что LLM теперь использует LIKE для поиска компаний."""
        # Мокаем ответ LLM с исправленным запросом
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": """SELECT COUNT(*) AS [Количество вагонов]
FROM [GRNG/GRMU].[dbo].[VagonUnloading]
WHERE [Грузовладелец] LIKE '%Еврохим%'
  AND [Дата (8:00-7:59)] >= CAST(DATEADD(month, -1, GETDATE()) AS DATE)
  AND [Дата (8:00-7:59)] < CAST(GETDATE() AS DATE)"""
                }
            }]
        }
        mock_post.return_value = mock_response
        
        # Тестируем запрос "Какое количество вагонов компании Еврохим было выгружено за последний месяц"
        user_request = "Какое количество вагонов компании Еврохим было выгружено за последний месяц"
        
        sql_query = self.llm_generator.generate_sql_query(user_request)
        
        # Проверяем, что используется LIKE вместо =
        assert "LIKE '%Еврохим%'" in sql_query
        assert "[Грузовладелец] = 'Еврохим'" not in sql_query
        
        # Проверяем корректную работу с датами
        assert "CAST(DATEADD(month, -1, GETDATE()) AS DATE)" in sql_query
        assert "CAST(GETDATE() AS DATE)" in sql_query
        # Проверяем, что нет некорректной конструкции
        assert "CAST(DATEADD(month, -1, GETDATE()) AS DATE) + 1" not in sql_query
    
    @patch('app.requests.post')
    def test_date_range_logic_correction(self, mock_post):
        """Тест проверяет корректную логику работы с датовыми диапазонами."""
        # Мокаем ответ LLM с правильной логикой дат
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": """SELECT 
    [Груз],
    COUNT(*) AS [Количество вагонов]
FROM [GRNG/GRMU].[dbo].[VagonUnloading]
WHERE [Дата (8:00-7:59)] >= CAST(DATEADD(week, -1, GETDATE()) AS DATE)
  AND [Дата (8:00-7:59)] < CAST(GETDATE() AS DATE)
GROUP BY [Груз]
ORDER BY [Количество вагонов] DESC"""
                }
            }]
        }
        mock_post.return_value = mock_response
        
        user_request = "Показать выгрузку вагонов по типам грузов за последнюю неделю"
        
        sql_query = self.llm_generator.generate_sql_query(user_request)
        
        # Проверяем корректную работу с датовыми диапазонами
        assert "CAST(DATEADD(week, -1, GETDATE()) AS DATE)" in sql_query
        assert "< CAST(GETDATE() AS DATE)" in sql_query
        
        # Проверяем, что нет проблемной конструкции с + 1
        assert "+ 1" not in sql_query
    
    @patch('app.requests.post')
    def test_partial_text_search_examples_in_prompt(self, mock_post):
        """Тест проверяет, что промпт содержит правильные примеры для частичного поиска."""
        # Получаем содержимое промпта
        prompt_content = self.llm_generator.prompt_template_content
        
        # Проверяем, что в промпте есть правила для текстового поиска
        assert "Text Search Rules" in prompt_content
        assert "LIKE operator for partial matching" in prompt_content
        assert "WHERE [Грузовладелец] LIKE '%Еврохим%'" in prompt_content
        
        # Проверяем наличие примера с правильным использованием LIKE
        assert "Еврохим" in prompt_content
        assert "LIKE '%Еврохим%'" in prompt_content
    
    @patch('app.requests.post')
    def test_date_range_rules_in_prompt(self, mock_post):
        """Тест проверяет, что промпт содержит правильные правила для работы с датами."""
        # Получаем содержимое промпта
        prompt_content = self.llm_generator.prompt_template_content
        
        # Проверяем наличие правил для работы с датовыми диапазонами
        assert "Date Range Rules" in prompt_content
        assert "last month" in prompt_content
        assert "CAST(GETDATE() AS DATE)" in prompt_content
        
        # Проверяем, что есть предупреждение против некорректных конструкций
        assert "NEVER" in prompt_content
        assert "type clash errors" in prompt_content
    
    def test_prompt_contains_corrected_examples(self):
        """Тест проверяет, что промпт содержит исправленные примеры."""
        prompt_content = self.llm_generator.prompt_template_content
        
        # Проверяем наличие Example 3 с исправленным поиском компании
        assert "Example 3: Company search using LIKE" in prompt_content
        assert "Use LIKE for company names to catch variations" in prompt_content
        
        # Проверяем наличие корректного примера с датами
        assert "< CAST(GETDATE() AS DATE)" in prompt_content
        
        # Проверяем, что есть правильные правила (важно, что есть объяснения что НЕ делать)
        assert "Date Range Rules" in prompt_content
        assert "Text Search Rules" in prompt_content
    
    @patch('app.requests.post')  
    def test_llm_receives_updated_prompt(self, mock_post):
        """Тест проверяет, что LLM получает обновленный промпт с новыми правилами."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "SELECT 1"
                }
            }]
        }
        mock_post.return_value = mock_response
        
        self.llm_generator.generate_sql_query("тестовый запрос")
        
        # Проверяем, что в вызове API есть обновленные правила
        called_payload = mock_post.call_args[1]['json']
        prompt_sent = called_payload['messages'][0]['content']
        
        # Проверяем наличие новых правил в отправленном промпте
        assert "Text Search Rules" in prompt_sent
        assert "Date Range Rules" in prompt_sent
        assert "LIKE operator for partial matching" in prompt_sent
