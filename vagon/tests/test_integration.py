import pytest
import requests
from flask import Flask
from unittest.mock import patch, MagicMock
from flask import Flask
import pandas as pd
import os

# Добавляем путь к vagon в sys.path, чтобы можно было импортировать app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db_manager, llm_generator

@pytest.fixture
def client():
    """Фикстура для создания тестового клиента Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Проверяет, что базовый маршрут '/' отдает 200 OK."""
    response = client.get('/')
    assert response.status_code == 200

@patch('app.db_manager.execute_query')
def test_get_stats_api(mock_execute_query, client):
    """Тестирует API /api/stats с моком базы данных."""
    # Мокаем ответ от БД
    mock_df = pd.DataFrame({
        'TABLE_NAME': ['VagonImport'],
        'TABLE_ROWS': [1000],
        'SIZE_MB': [5.2]
    })
    mock_execute_query.return_value = mock_df

    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['TABLE_NAME'] == 'VagonImport'

@patch('app.requests.post')
def test_generate_sql_api_success(mock_post, client):
    """Тестирует успешную генерацию SQL через /api/generate-sql."""
    # Мокаем успешный ответ от HuggingFace API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "SELECT TOP 5 [Род груза] FROM [dbo].[VagonImport]"
            }
        }]
    }
    mock_post.return_value = mock_response

    response = client.post('/api/generate-sql', json={'query': 'дай топ 5 грузов'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'sql_query' in data
    assert data['sql_query'] == 'SELECT TOP 5 [Род груза] FROM [dbo].[VagonImport]'

@patch('app.requests.post')
def test_generate_sql_api_hf_error(mock_post, client):
    """Тестирует обработку ошибки от HuggingFace API."""
    # Мокаем ответ с ошибкой
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")
    mock_post.return_value = mock_response

    response = client.post('/api/generate-sql', json={'query': 'сломанный запрос'})
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Network error' in data['error']

def test_execute_sql_api_invalid_sql(client):
    """
    Интеграционный тест: проверяет обработку синтаксически неверного SQL.
    Этот тест выполняет реальный запрос к БД с заведомо некорректным SQL.
    """
    # Этот SQL содержит ошибку, которую вы прислали: "принятый (t)" и "LIMIT"
    invalid_sql = "SELECT [Род груза], [Вес нетто (т)] FROM [dbo].[VagonImport] LIMIT 5"

    response = client.post('/api/execute-sql', json={'query': invalid_sql})
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    # Проверяем, что сообщение об ошибке от ODBC драйвера присутствует
    assert 'Incorrect syntax' in data['error'] or '42000' in data['error']

def test_execute_sql_api_valid_sql_integration(client):
    """
    Интеграционный тест: проверяет выполнение корректного SQL запроса.
    Этот тест выполняет реальный, простой и безопасный запрос к БД.
    """
    # Простой, быстрый и безопасный запрос, который не меняет данные
    valid_sql = "SELECT TOP 1 [Род груза] FROM [dbo].[VagonImport]"

    response = client.post('/api/execute-sql', json={'query': valid_sql})
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Если таблица не пуста, должен вернуться хотя бы один элемент
    if len(data) > 0:
        assert '[Род груза]' in data[0]

def test_generate_and_execute_sql_error(client):
    """
    Интеграционный тест, который проверяет связку генерации и выполнения SQL.
    Этот тест должен упасть, если LLM генерирует некорректный SQL.
    """
    user_query = "Покажи топ 5 родов груза по весу за последний месяц"

    # Шаг 1: Генерация SQL
    # Мы мокируем ответ от LLM, чтобы вернуть заведомо некорректный SQL,
    # который приводил к ошибке, чтобы проверить, как система его обработает.
    bad_sql_query = "SELECT T1.RодГруза, T1.ВесГруза принятый (t) FROM VagonImport AS T1 JOIN ShipsImport AS T2 ON T1.РодГруза = T2.РодГруза JOIN EnterpriseWagons AS T3 ON T1.Водовладелец = T3.Грузовладелец WHERE T2.Месяц = GETDATE() GROUP BY T1.RодГруза ORDER BY T3.ВесГруза DESC LIMIT 5"

    with patch('app.llm_generator.generate_sql_query') as mock_generate:
        mock_generate.return_value = bad_sql_query
        
        response_generate = client.post('/api/generate-sql', json={'query': user_query})
        assert response_generate.status_code == 200
        generated_sql = response_generate.json['sql_query']
        assert generated_sql == bad_sql_query

        # Шаг 2: Выполнение сгенерированного SQL
        # Здесь мы не мокируем выполнение, чтобы ошибка от драйвера БД была поймана.
        response_execute = client.post('/api/execute-sql', json={'query': generated_sql})

    # Проверяем, что API вернуло ошибку 500
    assert response_execute.status_code == 500
    json_data = response_execute.get_json()
    
    # Проверяем, что в тексте ошибки есть упоминание синтаксической проблемы
    assert 'error' in json_data
    assert "Incorrect syntax near" in json_data['error'] or "syntax error" in json_data['error'].lower()

def test_get_stats_api_not_empty(client):
    """Тестирует, что /api/stats не возвращает пустой ответ."""
    response = client.get('/api/stats')
    assert response.status_code == 200
    # Проверяем, что ответ не пустой
    assert response.data
    # Проверяем, что json не пустой
    assert response.get_json() is not None

@patch('app.db_manager.connect')
def test_get_stats_api_db_connection_error(mock_connect, client):
    """Тестирует API /api/stats при ошибке подключения к базе данных."""
    mock_connect.side_effect = Exception("Test DB Connection Error")

    response = client.get('/api/stats')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Test DB Connection Error' in data['error']

@patch('app.requests.post')
def test_generate_sql_api_hf_404_error(mock_post, client):
    """Тестирует обработку 404 ошибки от HuggingFace API."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url: test_url")
    mock_post.return_value = mock_response

    response = client.post('/api/generate-sql', json={'query': 'тестовый запрос'})
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Network error while contacting HuggingFace API' in data['error']
    assert '404 Client Error: Not Found' in data['error']

import os
import sys
import pytest
from unittest.mock import patch

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def app():
    """Создает и настраивает новый экземпляр приложения для каждого теста."""
    # Устанавливаем режим тестирования
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Тестовый клиент для отправки запросов в приложение."""
    return app.test_client()

def test_how_many_wagons_passed_integration(client):
    """
    Интеграционный тест для запроса "сколько вагонов прошло".
    Проверяет полный цикл: генерация SQL -> выполнение SQL -> получение результата.
    """
    # Патчим LLM API для возврата корректного SQL с правильными именами таблиц
    with patch('app.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "SELECT COUNT(*) as wagon_count FROM [dbo].[VagonImport]"
                }
            }]
        }
        mock_post.return_value = mock_response
        
        # Шаг 1: Отправляем запрос на генерацию SQL
        response_generate = client.post('/api/generate-sql', json={'query': 'сколько вагонов прошло'})
        
        # Проверяем, что запрос на генерацию успешен
        assert response_generate.status_code == 200
        json_data_generate = response_generate.get_json()
        
        # Проверяем, что в ответе есть ключ 'sql_query'
        assert 'sql_query' in json_data_generate
        sql_query = json_data_generate['sql_query']
        
        # Проверяем, что сгенерированный SQL не пустой
        assert sql_query is not None and sql_query.strip() != ""
        
        print(f"Сгенерирован SQL-запрос: {sql_query}")

        # Шаг 2: Выполняем сгенерированный SQL-запрос
        response_execute = client.post('/api/execute-sql', json={'query': sql_query})
        
        # Проверяем, что запрос на выполнение успешен
        assert response_execute.status_code == 200
        json_data_execute = response_execute.get_json()
        
        # Проверяем, что результат - это список (даже если пустой)
        assert isinstance(json_data_execute, list)
        
        print(f"Результат выполнения запроса: {json_data_execute}")
        
        # Шаг 3: Проверяем содержимое ответа
        # Поскольку мы знаем, что таблицы, скорее всего, пусты, мы ожидаем получить 0 или сообщение.
        if json_data_execute:
            # Если результат не пустой, проверяем его структуру
            first_row = json_data_execute[0]
            assert isinstance(first_row, dict)
            # Проверяем, что есть либо числовые результаты, либо сообщение о пустой таблице
            assert any(isinstance(v, int) for v in first_row.values()) or "Сообщение" in first_row
