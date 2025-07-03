import os
import json
import pyodbc
import pandas as pd
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# --- Классы для работы с БД и LLM (адаптированные) ---

class DatabaseManager:
    def __init__(self):
        self.connection_string = self._build_connection_string()
        self.connection = None
        self.schema_info = self._parse_schema_file()  # Добавлено: загрузка схемы при инициализации

    def _build_connection_string(self):
        """Строим строку подключения к базе данных OperativeReport"""
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME_OPERATIVE', 'OperativeReport')
        driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
        return f"DRIVER={{{driver}}};SERVER={host},{port};DATABASE={database};UID={user};PWD={password};"

    def connect(self):
        """Подключение к базе данных"""
        try:
            # Убрана проверка self.connection.connected, так как она некорректна для pyodbc
            if not self.connection:
                print("Подключение к базе данных...")
                self.connection = pyodbc.connect(self.connection_string)
                print("Успешное подключение к базе данных")
            return True
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            self.connection = None
            # Проверяем переменные окружения (без вывода пароля)
            env_vars = {
                'DB_HOST': os.getenv('DB_HOST'),
                'DB_PORT': os.getenv('DB_PORT'),
                'DB_USER': os.getenv('DB_USER'),
                'DB_NAME_OPERATIVE': os.getenv('DB_NAME_OPERATIVE'),
                'DB_DRIVER': os.getenv('DB_DRIVER')
            }
            print(f"Проверьте переменные окружения: {env_vars}")
            return False # Не пробрасываем исключение, чтобы приложение не падало полностью

    def execute_query(self, query):
        """Выполнение SQL запроса"""
        try:
            # Вызываем connect() и проверяем результат
            if not self.connect():
                print("Не удалось подключиться к базе данных")
                return pd.DataFrame()  # Возвращаем пустой DataFrame вместо None
                
            print(f"Выполнение запроса: {query}")
            df = pd.read_sql(query, self.connection)
            print(f"Запрос выполнен, получено строк: {len(df)}")
            
            # Если результат запроса пуст, выведем предупреждение
            if df.empty:
                print("ВНИМАНИЕ: Запрос вернул пустой набор данных")
                
            return df
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {str(e)}")
            # Пробуем выполнить проверочный запрос для диагностики
            try:
                test_query = "SELECT TOP 1 * FROM INFORMATION_SCHEMA.TABLES"
                print(f"Выполнение диагностического запроса: {test_query}")
                test_df = pd.read_sql(test_query, self.connection)
                print(f"Диагностический запрос выполнен успешно, таблиц найдено: {len(test_df)}")
            except Exception as test_e:
                print(f"Диагностический запрос также не удался: {str(test_e)}")
                
            raise e  # Пробрасываем исключение для обработки в API

    def get_table_statistics(self):
        """Получение общей статистики по таблицам (SQL Server)"""
        query_sqlserver = """
        SELECT 
            t.name AS TABLE_NAME,
            p.rows AS TABLE_ROWS,
            CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36,2)) AS SIZE_MB
        FROM 
            sys.tables t
        INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
        INNER JOIN sys.partitions p ON i.OBJECT_ID = p.OBJECT_ID AND i.index_id = p.index_id
        INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
        WHERE t.is_ms_shipped = 0 AND i.OBJECT_ID > 255
        GROUP BY t.Name, p.Rows
        ORDER BY t.Name
        """
        return self.execute_query(query_sqlserver)

    def _parse_schema_file(self):
        """Загружает и обрабатывает файл схемы базы данных"""
        try:
            schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_shema.sql")
            if not os.path.exists(schema_path):
                print(f"ПРЕДУПРЕЖДЕНИЕ: Файл схемы не найден: {schema_path}")
                return ""
                
            with open(schema_path, 'r', encoding='utf-8') as file:
                schema_content = file.read()
                
            # Извлекаем информацию о таблицах из схемы
            table_info = {}
            current_table = None
            
            for line in schema_content.split('\n'):
                line = line.strip()
                # Ищем определения таблиц
                if line.startswith('CREATE TABLE') or line.startswith('-- Таблица:'):
                    # Из строки вида "CREATE TABLE [dbo].[TableName]" извлекаем TableName
                    if 'CREATE TABLE' in line:
                        match = line.split('[dbo].[')[1].split(']')[0] if '[dbo].[' in line else None
                        if match:
                            current_table = match
                            table_info[current_table] = []
                    elif '-- Таблица:' in line:
                        # Из строки вида "-- Таблица: dbo.TableName" извлекаем TableName
                        parts = line.split('-- Таблица: dbo.')[1] if '-- Таблица: dbo.' in line else line.split('-- Таблица: ')[1]
                        current_table = parts.strip()
                        table_info[current_table] = []
                
                # Если мы внутри определения таблицы и нашли столбец
                elif current_table and ('[' in line or 'nvarchar' in line or 'int' in line or 'float' in line or 'date' in line):
                    if '[' in line:
                        # Извлекаем имя столбца в квадратных скобках
                        column = line.split('[')[1].split(']')[0] if '[' in line else None
                        if column:
                            table_info[current_table].append(column)
            
            # Форматируем информацию для использования в промпте LLM
            formatted_schema = "ДОСТУПНЫЕ ТАБЛИЦЫ И СТОЛБЦЫ (используйте ТОЛЬКО эти названия):\n\n"
            
            # Отсортируем таблицы по алфавиту для удобства
            for table in sorted(table_info.keys()):
                columns = ", ".join([f"[{col}]" for col in table_info[table][:15]])  # Увеличил лимит до 15 столбцов
                if len(table_info[table]) > 15:
                    columns += ", ..."
                formatted_schema += f"Таблица [dbo].[{table}]:\n   Столбцы: {columns}\n\n"
            
            formatted_schema += """
ПРАВИЛА ГЕНЕРАЦИИ SQL:
- Используйте ТОЛЬКО таблицы и столбцы, перечисленные выше
- Формат таблицы: [dbo].[ИмяТаблицы] 
- Формат столбца: [ИмяСтолбца]
- Для подсчета используйте COUNT(*)
- Для ограничения результатов используйте TOP N (не LIMIT)
- Для дат используйте GETDATE(), DATEADD(), YEAR(), MONTH()

ПРИМЕРЫ КОРРЕКТНЫХ ЗАПРОСОВ:
- SELECT COUNT(*) FROM [dbo].[EnterpriseWagons]
- SELECT TOP 5 [Груз] FROM [dbo].[VagonImport]
- SELECT [Род груза], COUNT(*) FROM [dbo].[VagonImport] GROUP BY [Род груза]
"""
            
            print(f"Схема базы данных успешно загружена из {schema_path}")
            print(f"Найдено таблиц: {len(table_info)}")
            return formatted_schema
            
        except Exception as e:
            print(f"Ошибка при загрузке файла схемы: {str(e)}")
            return """
Пример схемы (используется, т.к. файл db_shema.sql не найден или содержит ошибку):
Таблица [dbo].[TableName1]:
   Столбцы: [Column1], [Column2], [Column3]

Таблица [dbo].[TableName2]:
   Столбцы: [ColumnA], [ColumnB], [ColumnC]

ПРАВИЛА:
- Используйте формат [dbo].[ИмяТаблицы]
- Используйте формат [ИмяСтолбца]
- Для подсчета используйте COUNT(*)
"""

    def get_schema_info(self):
        """Возвращает информацию о схеме базы данных"""
        return self.schema_info

class LLMQueryGenerator:
    def __init__(self):
        self.hf_token = os.getenv('HF_TOKEN')
        #https://router.huggingface.co/featherless-ai/v1/chat/completions не менять до 2026 года!!!!!
        self.api_url = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json",
        }
        if not self.hf_token:
            print("ВНИМАНИЕ: Не найден токен HuggingFace. Установите переменную окружения HF_TOKEN")

    def _clean_sql_response(self, text):
        """Очищает ответ от лишних символов и форматирования."""
        # Удаляем блоки кода markdown
        if "```sql" in text:
            text = text.split("```sql")[1].split("```")[0]
        # Удаляем начальные и конечные пробелы и точки с запятой
        return text.strip().rstrip(';')



    def _validate_sql_tables(self, sql_query, schema_info):
        """Проверяет, что SQL-запрос использует только существующие таблицы из схемы"""
        # Извлекаем список доступных таблиц из схемы
        available_tables = []
        for line in schema_info.split('\n'):
            if line.strip().startswith('Таблица [dbo].['):
                table_name = line.split('[dbo].[')[1].split(']')[0]
                available_tables.append(table_name)
        
        # Ищем использованные таблицы в SQL
        import re
        used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', sql_query)
        
        # Проверяем, что все использованные таблицы существуют в схеме
        for used_table in used_tables:
            if used_table not in available_tables:
                raise Exception(f"LLM использовал несуществующую таблицу: {used_table}. Доступные таблицы: {', '.join(available_tables)}")
        
        return True

    def generate_sql_query(self, user_request, schema_info):
        """Генерация SQL запроса на основе пользовательского запроса через HuggingFace API"""
        if not self.is_available():
            raise ConnectionError("HuggingFace API недоступна. Проверьте токен HF_TOKEN.")

        prompt = f"""
        <|system|>
        You are an expert SQL Server database analyst. Your task is to generate ONLY valid SQL queries based on the provided database schema.

        CRITICAL RULES - FOLLOW EXACTLY OR RETURN ERROR:
        1. Use ONLY table names and column names from the provided schema below
        2. NEVER invent or guess table names - only use what is explicitly listed
        3. Always use [dbo].[TableName] format for tables
        4. Always use [ColumnName] format for columns
        5. Use SQL Server syntax (not MySQL LIMIT - use TOP instead)
        6. For date operations use SQL Server functions: GETDATE(), DATEADD(), YEAR(), MONTH()
        7. Return ONLY the SQL query without explanations or markdown

        DATABASE SCHEMA (USE ONLY THESE TABLES AND COLUMNS):
        {schema_info}

        VALIDATION STEPS - FOLLOW BEFORE GENERATING SQL:
        1. Read the user request carefully
        2. Scan the schema above for relevant tables
        3. Verify the table name exists in the schema
        4. Verify the column names exist in the chosen table
        5. If ANY table or column name is not found in the schema above, return: "ERROR: No suitable tables found in schema for this request"

        EXAMPLES OF CORRECT MAPPING:
        - "страны назначения" → Look for [Страна назначения] column → Found in [dbo].[ShipsPlan] table
        - "типы судов" → Look for [Судно] column → Found in [dbo].[ShipsImport], [dbo].[ShipsPlan] tables
        - "операции импорта вагонов" → Look for import/wagon tables → Found in [dbo].[VagonImport], [dbo].[UploadWagonsImport]

        <|user|>
        USER REQUEST: {user_request}
        
        First, verify that appropriate tables exist in the schema. Then generate SQL query using ONLY the tables and columns from the schema above:
        <|assistant|>
        """

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "Qwen/Qwen2.5-Coder-32B",
            "max_tokens": 500,
            "temperature": 0,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            
            response_data = response.json()

            if "error" in response_data:
                error_details = response_data.get('error_description', response_data['error'])
                raise Exception(f"HuggingFace API Error: {error_details}")

            if not response_data.get("choices"):
                 raise Exception(f"HuggingFace API Error: No choices in response - {response_data}")

            sql_query = response_data["choices"][0]["message"]["content"]
            cleaned_query = self._clean_sql_response(sql_query)
            
            # Дополнительная проверка: если LLM вернул ошибку о несоответствии схеме
            if "ERROR: No suitable tables found" in cleaned_query:
                raise Exception(f"LLM could not map user request to available database schema. Request: {user_request}")
            
            # Валидируем, что SQL использует только существующие таблицы
            try:
                self._validate_sql_tables(cleaned_query, schema_info)
            except Exception as validation_error:
                raise Exception(f"SQL validation failed: {str(validation_error)}")
            
            return cleaned_query

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error while contacting HuggingFace API: {e}")
        except Exception as e:
            print(f"An error occurred during SQL generation: {e}")
            raise

    def generate_sql_query_with_prompt(self, user_request, schema_info):
        """Генерация SQL запроса с возвратом полного промпта"""
        if not self.is_available():
            raise ConnectionError("HuggingFace API недоступна. Проверьте токен HF_TOKEN.")

        prompt = f"""
        <|system|>
        You are an expert SQL Server database analyst. Your task is to generate ONLY valid SQL queries based on the provided database schema.

        CRITICAL RULES - FOLLOW EXACTLY OR RETURN ERROR:
        1. Use ONLY table names and column names from the provided schema below
        2. NEVER invent or guess table names - only use what is explicitly listed
        3. Always use [dbo].[TableName] format for tables
        4. Always use [ColumnName] format for columns
        5. Use SQL Server syntax (not MySQL LIMIT - use TOP вместо)
        6. Для операций с датами используйте функции SQL Server: GETDATE(), DATEADD(), YEAR(), MONTH()
        7. Возвращайте ТОЛЬКО SQL-запрос без объяснений или markdown

        СХЕМА БАЗЫ ДАННЫХ (ИСПОЛЬЗУЙТЕ ТОЛЬКО ЭТИ ТАБЛИЦЫ И СТОЛБЦЫ):
        {schema_info}

        ШАГИ ВАЛИДАЦИИ - СЛЕДУЙТЕ ПЕРЕД ГЕНЕРАЦИЕЙ SQL:
        1. Внимательно прочитайте запрос пользователя
        2. Просканируйте схему выше на наличие соответствующих таблиц
        3. Убедитесь, что имя таблицы существует в схеме
        4. Убедитесь, что имена столбцов существуют в выбранной таблице
        5. Если ЛЮБОЕ имя таблицы или столбца не найдено в схеме выше, верните: "ERROR: No suitable tables found in schema for this request"

        ПРИМЕРЫ ПРАВИЛЬНОГО СООТВЕТСТВИЯ:
        - "страны назначения" → Найдите столбец [Страна назначения] → Найдено в таблице [dbo].[ShipsPlan]
        - "типы судов" → Найдите столбец [Судно] → Найдено в таблицах [dbo].[ShipsImport], [dbo].[ShipsPlan]
        - "операции импорта вагонов" → Найдите таблицы импорта/вагонов → Найдено в таблицах [dbo].[VagonImport], [dbo].[UploadWagonsImport]

        <|user|>
        ЗАПРОС ПОЛЬЗОВАТЕЛЯ: {user_request}
        
        Сначала проверьте, существуют ли в схеме соответствующие таблицы. Затем сгенерируйте SQL-запрос, используя ТОЛЬКО таблицы и столбцы из схемы выше:
        <|assistant|>
        """

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "Qwen/Qwen2.5-Coder-32B",
            "max_tokens": 500,
            "temperature": 0,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            
            response_data = response.json()

            if "error" in response_data:
                error_details = response_data.get('error_description', response_data['error'])
                raise Exception(f"HuggingFace API Error: {error_details}")

            if not response_data.get("choices"):
                 raise Exception(f"HuggingFace API Error: No choices in response - {response_data}")

            sql_query = response_data["choices"][0]["message"]["content"]
            cleaned_query = self._clean_sql_response(sql_query)
            
            # Дополнительная проверка: если LLM вернул ошибку о несоответствии схеме
            if "ERROR: No suitable tables found" in cleaned_query:
                raise Exception(f"LLM could not map user request to available database schema. Request: {user_request}")
            
            # Валидируем, что SQL использует только существующие таблицы
            try:
                self._validate_sql_tables(cleaned_query, schema_info)
            except Exception as validation_error:
                raise Exception(f"SQL validation failed: {str(validation_error)}")
            
            return cleaned_query, prompt

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error while contacting HuggingFace API: {e}")
        except Exception as e:
            print(f"An error occurred during SQL generation: {e}")
            raise

    def is_available(self):
        """Проверка доступности HuggingFace API"""
        return self.hf_token is not None

# --- Инициализация Flask и классов ---

app = Flask(__name__)
db_manager = DatabaseManager()
llm_generator = LLMQueryGenerator()

# --- Маршруты Flask ---

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """API для получения статистики по таблицам"""
    try:
        stats = db_manager.get_table_statistics()
        return jsonify(stats.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-schema')
def get_schema():
    """API для получения схемы базы данных"""
    try:
        schema_info = db_manager.get_schema_info()
        return jsonify({"schema": schema_info})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-sql', methods=['POST'])
def generate_sql():
    """API для генерации SQL"""
    if not llm_generator.is_available():
        return jsonify({"error": "LLM service is not available"}), 503

    data = request.json
    user_query = data.get('query')
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    print(f"Received user query: {user_query}") # Добавлено логирование

    # Получаем схему из DatabaseManager вместо хардкода
    schema_info = db_manager.get_schema_info()
    print(f"Используем схему БД из файла db_shema.sql")
    
    try:
        sql_query = llm_generator.generate_sql_query(user_query, schema_info)
        return jsonify({"sql_query": sql_query})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-sql-with-prompt', methods=['POST'])
def generate_sql_with_prompt():
    """API для генерации SQL с показом полного промпта"""
    if not llm_generator.is_available():
        return jsonify({"error": "LLM service is not available"}), 503

    data = request.json
    user_query = data.get('query')
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    print(f"Received user query: {user_query}")

    # Получаем схему из DatabaseManager
    schema_info = db_manager.get_schema_info()
    print(f"Используем схему БД из файла db_shema.sql")
    
    try:
        sql_query, full_prompt = llm_generator.generate_sql_query_with_prompt(user_query, schema_info)
        return jsonify({
            "sql_query": sql_query,
            "full_prompt": full_prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/execute-sql', methods=['POST'])
def execute_sql():
    """API для выполнения SQL"""
    data = request.json
    sql_query = data.get('query')
    if not sql_query:
        return jsonify({"error": "SQL query is required"}), 400

    try:
        # Проверяем и добавляем схему dbo, если она не указана
        if "FROM " in sql_query and "[dbo]." not in sql_query and "dbo." not in sql_query:
            # Находим имена таблиц после FROM и JOIN
            import re
            tables = re.findall(r'FROM\s+([^\s,;()]+)|JOIN\s+([^\s,;()]+)', sql_query, re.IGNORECASE)
            # Объединяем все найденные группы и удаляем пустые значения
            tables = [t for group in tables for t in group if t]
            
            # Добавляем префикс [dbo]. к таблицам, если их еще нет
            for table in tables:
                if not table.startswith('[dbo].') and not table.startswith('dbo.'):
                    # Заменяем, только если это не подзапрос
                    sql_query = sql_query.replace(f"FROM {table}", f"FROM [dbo].[{table}]")
                    sql_query = sql_query.replace(f"JOIN {table}", f"JOIN [dbo].[{table}]")
        
        print(f"Выполняется запрос: {sql_query}")  # Добавляем логирование запроса
        
        # Проверяем соединение с БД перед выполнением
        db_manager.connect()
        
        result_df = db_manager.execute_query(sql_query)
        
        if result_df is None or result_df.empty:
            print("Запрос вернул пустой результат")
            
            # Если это запрос COUNT(*), то добавляем пояснение
            if "COUNT(*)" in sql_query.upper():
                # Находим имя таблицы
                import re
                table_match = re.search(r'FROM\s+\[dbo\]\.\[([^\]]+)\]', sql_query)
                if table_match:
                    table_name = table_match.group(1)
                    
                    # Проверяем другие таблицы с вагонами, если запрос о вагонах вернул 0
                    if table_name == "VagonImport" and any(word in sql_query.lower() for word in ["count", "количество"]):
                        print("Проверка альтернативных таблиц с данными о вагонах...")
                        try:
                            alt_query = """
                            SELECT 
                                (SELECT COUNT(*) FROM [dbo].[EnterpriseWagons]) AS EnterpriseWagons,
                                (SELECT COUNT(*) FROM [dbo].[ShipmentsToThePort]) AS ShipmentsToThePort,
                                (SELECT COUNT(*) FROM [dbo].[WagonsOnTheWay]) AS WagonsOnTheWay
                            """
                            alt_df = db_manager.execute_query(alt_query)
                            if not alt_df.empty:
                                # Добавляем пояснение в ответ
                                return jsonify([{
                                    "Сообщение": f"Таблица {table_name} пуста. Проверьте другие таблицы с данными о вагонах:",
                                    **alt_df.iloc[0].to_dict()
                                }]), 200
                        except Exception as alt_e:
                            print(f"Ошибка при проверке альтернативных таблиц: {alt_e}")
            
            return jsonify([]), 200  # Возвращаем пустой список вместо ошибки
            
        # Преобразуем типы данных, которые не сериализуются в JSON
        for col in result_df.columns:
            if pd.api.types.is_datetime64_any_dtype(result_df[col]):
                result_df[col] = result_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        results = result_df.to_dict(orient='records')
        return jsonify(results)
    except Exception as e:
        error_msg = f"Ошибка при выполнении SQL запроса: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
