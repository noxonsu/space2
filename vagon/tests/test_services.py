import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import requests

# Добавляем путь к проекту, чтобы можно было импортировать app и его классы
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import DatabaseManager, LLMQueryGenerator

# --- Тесты для DatabaseManager ---

@pytest.fixture
def db_manager():
    """Фикстура для создания экземпляра DatabaseManager с моком pyodbc."""
    with patch('app.pyodbc') as mock_pyodbc:
        # Мокаем до инициализации, чтобы не было реального вызова
        manager = DatabaseManager()
        manager.connection = MagicMock()
        mock_pyodbc.connect.return_value = manager.connection
        yield manager

@patch.dict(os.environ, {
    'DB_HOST': 'testhost',
    'DB_PORT': '1234',
    'DB_USER': 'testuser',
    'DB_PASSWORD': 'testpass',
    'DB_NAME_OPERATIVE': 'TestDB',
    'DB_DRIVER': 'TestDriver'
})
def test_db_connection_string_builds_correctly():
    """Тест: строка подключения создается правильно из переменных окружения."""
    manager = DatabaseManager()
    expected_string = "DRIVER={TestDriver};SERVER=testhost,1234;DATABASE=TestDB;UID=testuser;PWD=testpass;"
    assert manager.connection_string == expected_string

def test_db_execute_query_success(db_manager):
    """Тест: успешное выполнение запроса."""
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
    with patch('pandas.read_sql', return_value=mock_df) as mock_read_sql:
        result = db_manager.execute_query("SELECT * FROM test")
        mock_read_sql.assert_called_once_with("SELECT * FROM test", db_manager.connection)
        assert result.equals(mock_df)

def test_db_connect_failure():
    """Тест: ошибка подключения к БД."""
    with patch('app.pyodbc.connect', side_effect=Exception("Connection Error")) as mock_connect:
        with pytest.raises(Exception, match="Connection Error"):
            manager = DatabaseManager()
            manager.connect()

# --- Тесты для LLMQueryGenerator ---

@patch.dict(os.environ, {"HF_TOKEN": "fake-token"})
@patch('app.requests.post')
def test_llm_is_available(mock_post):
    """Тест: проверка доступности LLM API."""
    generator = LLMQueryGenerator()
    assert generator.is_available() is True

@patch.dict(os.environ, {}, clear=True)
@patch('huggingface_hub.InferenceClient')
def test_llm_is_not_available(mock_inference_client):
    """Тест: проверка недоступности LLM API при отсутствии токена."""
    generator = LLMQueryGenerator()
    assert generator.is_available() is False
    mock_inference_client.assert_not_called()

@patch.dict(os.environ, {"HF_TOKEN": "fake-token"})
@patch('app.requests.post')
def test_llm_generate_sql_query_success(mock_post):
    """Тест: успешная генерация SQL запроса."""
    # Настраиваем мок клиента
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "SELECT * FROM VagonImport;"
            }
        }]
    }
    mock_post.return_value = mock_response

    generator = LLMQueryGenerator()
    user_request = "show all wagons"
    schema_info = "schema"
    sql_query = generator.generate_sql_query(user_request, schema_info)

    mock_post.assert_called_once()
    assert sql_query == "SELECT * FROM VagonImport"

@patch.dict(os.environ, {"HF_TOKEN": "fake-token"})
@patch('app.requests.post')
def test_llm_generate_sql_query_api_error(mock_post):
    """Тест: ошибка при обращении к API HuggingFace."""
    mock_post.side_effect = requests.exceptions.RequestException("API Error")

    generator = LLMQueryGenerator()
    with pytest.raises(ConnectionError, match="Network error while contacting HuggingFace API: API Error"):
        generator.generate_sql_query("test request", "schema")

def test_llm_generates_sql_with_mock_client(mocker):
    """Тест: генерация SQL с использованием мок-клиента."""
    # Мокаем requests.post
    mock_post = mocker.patch('app.requests.post')
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "SELECT * FROM mock_table;"
            }
        }]
    }
    mock_post.return_value = mock_response

    generator = LLMQueryGenerator()
    user_request = "покажи все из mock_table"
    schema_info = "schema"
    result = generator.generate_sql_query(user_request, schema_info)

    mock_post.assert_called_once()
    assert "SELECT" in result.upper()

def test_llm_fails_with_specific_query(mocker):
    """
    Тест для воспроизведения ошибки 500 при определенном запросе.
    """
    # Мокаем InferenceClient
    mock_client_instance = mocker.MagicMock()
    # Симулируем ответ от API, который может вызывать проблемы
    mock_post = mocker.patch('app.requests.post')
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "SELECT weight, received_date FROM cargoes ORDER BY weight DESC LIMIT 5;"
            }
        }]
    }
    mock_post.return_value = mock_response

    # Мокаем DatabaseManager, чтобы не делать реальных запросов к БД
    mock_db_manager = mocker.MagicMock()
    mock_db_manager.get_schema_description.return_value = "Table: cargoes, columns: id, name, weight, received_date"

    # Создаем экземпляр LLMQueryGenerator
    llm_generator = LLMQueryGenerator()

    # Проблемный запрос
    query = "покажи 5 самых тяжелых грузов в этом месяце"

    # Вызываем метод
    result = llm_generator.generate_sql_query(query, "schema")

    # Проверяем, что результат - это корректный SQL
    assert isinstance(result, str)
    assert "SELECT" in result.upper()
    assert "LIMIT 5" in result.upper()
