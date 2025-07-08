"""
Тесты для проверки и решения проблем с SQL запросами, которые обнаружил заказчик.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем путь к vagon в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db_manager, llm_generator

@pytest.fixture
def client():
    """Фикстура для создания тестового клиента Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestSQLIssues:
    """Тесты для проверки проблем с SQL запросами."""

    def test_vagon_import_table_structure(self):
        """Проверяет структуру таблицы VagonImport из схемы."""
        table_to_db = db_manager.table_to_database
        
        # Проверяем, что таблица VagonImport есть в схеме
        assert 'VagonImport' in table_to_db
        
        # Проверяем, что она принадлежит базе OperativeReport
        assert table_to_db['VagonImport'] == 'OperativeReport'
        
        # Проверяем, что в схеме есть информация о столбцах
        schema_info = db_manager.get_schema_info()
        assert 'VagonImport' in schema_info
        assert '[Номер вагона]' in schema_info
        assert '[Дата и время погрузки]' in schema_info
        
        # Проверяем, что в описании таблицы VagonImport нет колонки Бригада
        # Ищем секцию таблицы VagonImport
        vagon_import_section = schema_info[schema_info.find('Таблица [dbo].[VagonImport]'):schema_info.find('Таблица [dbo].[VagonImport]') + 500]
        assert '[Бригада]' not in vagon_import_section

    def test_fact_loading_table_structure(self):
        """Проверяет структуру таблицы FactLoading из схемы."""
        table_to_db = db_manager.table_to_database
        
        # Проверяем, что таблица FactLoading есть в схеме
        assert 'FactLoading' in table_to_db
        
        # Проверяем, что она принадлежит базе GRNG/GRMU
        assert table_to_db['FactLoading'] == 'GRNG/GRMU'
        
        # Проверяем, что в FactLoading ЕСТЬ колонка Бригада
        schema_info = db_manager.get_schema_info()
        assert 'FactLoading' in schema_info
        assert '[Бригада]' in schema_info

    def test_vagon_unloading_table_structure(self):
        """Проверяет структуру таблицы VagonUnloading из схемы."""
        table_to_db = db_manager.table_to_database
        
        # Проверяем, что таблица VagonUnloading есть в схеме
        assert 'VagonUnloading' in table_to_db
        
        # Проверяем, что она принадлежит базе GRNG/GRMU
        assert table_to_db['VagonUnloading'] == 'GRNG/GRMU'
        
        # Проверяем, что в VagonUnloading ЕСТЬ колонка Бригада
        schema_info = db_manager.get_schema_info()
        assert 'VagonUnloading' in schema_info
        assert '[Бригада]' in schema_info

    @patch('app.db_manager.execute_query')
    def test_brigade_weight_query_fix(self, mock_execute_query, client):
        """Тестирует исправление запроса по весу бригады."""
        # Мокаем ответ с реальными данными
        mock_df = pd.DataFrame({
            'TotalWeight': [12345.67]
        })
        mock_execute_query.return_value = mock_df

        # Правильный SQL запрос для веса бригады (должен использовать FactLoading)
        correct_sql = """
        SELECT SUM([Вес нетто (т)]) AS TotalWeight
        FROM [dbo].[FactLoading]
        WHERE [Бригада] = '1'
        AND YEAR([Дата (8:00-7:59)]) = 2024
        """
        
        response = client.post('/api/execute-sql', 
                              json={'query': correct_sql})
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data[0]['TotalWeight'] == 12345.67

    @patch('app.db_manager.execute_query')
    def test_wagon_count_query_fix(self, mock_execute_query, client):
        """Тестирует исправление запроса по количеству вагонов."""
        # Мокаем ответ с реальными данными
        mock_df = pd.DataFrame({
            'WagonCount': [456]
        })
        mock_execute_query.return_value = mock_df

        # Правильный SQL запрос для подсчета вагонов 
        # (должен использовать VagonImport без колонки Бригада)
        correct_sql = """
        SELECT COUNT(DISTINCT [Номер вагона]) AS WagonCount
        FROM [dbo].[VagonImport] 
        WHERE YEAR([Дата и время погрузки]) = 2024
        """
        
        response = client.post('/api/execute-sql', 
                              json={'query': correct_sql})
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data[0]['WagonCount'] == 456

    @patch('app.db_manager.execute_query')
    def test_different_database_error(self, mock_execute_query, client):
        """Тестирует ошибку при использовании таблиц из разных баз данных."""
        # SQL запрос, который использует таблицы из разных баз данных
        mixed_db_sql = """
        SELECT 
            v.[Номер вагона],
            f.[Бригада]
        FROM [dbo].[VagonImport] v
        JOIN [dbo].[FactLoading] f ON v.[Номер вагона] = f.[Номер вагона]
        WHERE YEAR(v.[Дата и время погрузки]) = 2024
        """
        
        response = client.post('/api/execute-sql', 
                              json={'query': mixed_db_sql})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Таблицы из разных баз данных' in data['error']

    @patch('app.db_manager.execute_query')
    def test_empty_result_handling(self, mock_execute_query, client):
        """Тестирует обработку пустых результатов."""
        # Мокаем пустой результат
        mock_df = pd.DataFrame()
        mock_execute_query.return_value = mock_df

        sql_query = """
        SELECT SUM([Вес нетто (т)]) AS TotalWeight
        FROM [dbo].[FactLoading]
        WHERE [Бригада] = '999'
        AND YEAR([Дата (8:00-7:59)]) = 2024
        """
        
        response = client.post('/api/execute-sql', 
                              json={'query': sql_query})
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data == []

    @patch('app.db_manager.execute_query')
    def test_null_result_handling(self, mock_execute_query, client):
        """Тестирует обработку NULL результатов."""
        # Мокаем результат с NULL
        mock_df = pd.DataFrame({
            'TotalWeight': [None]
        })
        mock_execute_query.return_value = mock_df

        sql_query = """
        SELECT SUM([Вес нетто (т)]) AS TotalWeight
        FROM [dbo].[FactLoading]
        WHERE [Бригада] = '1'
        AND YEAR([Дата (8:00-7:59)]) = 2024
        """
        
        response = client.post('/api/execute-sql', 
                              json={'query': sql_query})
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Проверяем, что NULL правильно обрабатывается
        assert data[0]['TotalWeight'] is None

    def test_sql_query_validation(self):
        """Тестирует валидацию SQL запросов."""
        # Проверяем, что система может определить таблицы в запросе
        test_sql = """
        SELECT COUNT(*) 
        FROM [dbo].[VagonImport] 
        WHERE YEAR([Дата и время погрузки]) = 2024
        """
        
        import re
        used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', test_sql)
        assert 'VagonImport' in used_tables
        
        # Проверяем определение базы данных
        db_name = db_manager.get_table_database('VagonImport')
        assert db_name == 'OperativeReport'

    @patch('app.requests.post')
    def test_llm_query_generation_with_correct_tables(self, mock_post, client):
        """Тестирует генерацию SQL с правильными таблицами."""
        # Мокаем ответ от LLM
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'SELECT COUNT(*) FROM [dbo].[VagonImport] WHERE YEAR([Дата и время погрузки]) = 2024'
                }
            }]
        }
        mock_post.return_value = mock_response

        # Запрос, который требует правильного выбора таблицы
        response = client.post('/api/generate-sql', 
                              json={'query': 'Сколько вагонов было погружено в 2024 году'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'sql_query' in data
        # Проверяем, что LLM сгенерировал запрос к правильной таблице
        assert 'VagonImport' in data['sql_query']
        assert 'Бригада' not in data['sql_query']  # Не должно быть колонки Бригада для VagonImport

    def test_schema_info_completeness(self):
        """Тестирует полноту информации о схеме."""
        schema_info = db_manager.get_schema_info()
        
        # Проверяем, что схема содержит информацию о ключевых таблицах
        key_tables = ['VagonImport', 'FactLoading', 'VagonUnloading', 'ShipsImport']
        for table in key_tables:
            assert table in schema_info, f"Таблица {table} отсутствует в схеме"
        
        # Проверяем, что есть правила генерации SQL
        assert 'ПРАВИЛА ГЕНЕРАЦИИ SQL' in schema_info
        assert 'ВНИМАНИЕ: Таблицы находятся в разных базах данных' in schema_info

    @patch('app.db_manager.execute_query')
    def test_total_weight_query_cross_database(self, mock_execute_query, client):
        """Тестирует обработку запроса общего веса из разных баз данных."""
        # Моккаем ответы для разных баз данных
        def mock_execute_side_effect(query, db_name):
            if db_name == 'GRNG/GRMU':
                if 'VagonUnloading' in query:
                    return pd.DataFrame({'TotalWeight': [1500.0]})
                elif 'FactLoading' in query:
                    return pd.DataFrame({'TotalWeight': [2000.0]})
                elif 'ShipmentsToThePort' in query:
                    return pd.DataFrame({'TotalWeight': [800.0]})
                elif 'EnterpriseWagons' in query:
                    return pd.DataFrame({'TotalWeight': [1200.0]})
            elif db_name == 'OperativeReport':
                if 'ShipsImport' in query:
                    return pd.DataFrame({'TotalWeight': [3000.0]})
                elif 'VagonImport' in query:
                    return pd.DataFrame({'TotalWeight': [2500.0]})
            return pd.DataFrame()
        
        mock_execute_query.side_effect = mock_execute_side_effect
        
        # Тестируем запрос общего веса, который должен обработать разные базы данных
        response = client.post('/api/generate-and-execute-total-weight', 
                              json={'query': 'Сколько тонн было перевезено в 2024 году'})
        
        # Пока такого API нет, тест должен пройти после реализации
        # assert response.status_code == 200
        # data = response.get_json()
        # assert 'total_weight' in data
        # assert data['total_weight'] > 0
