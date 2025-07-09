import os
import json
import pyodbc
import pandas as pd
import requests
import re
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Для работы без GUI
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# --- Классы для работы с БД и LLM (адаптированные) ---

class DatabaseManager:
    def __init__(self):
        self.connections = {}  # Словарь для хранения подключений к разным базам данных
        self.schema_info = "" 
        self.table_to_database = {}
        self._parse_schema_from_prompt_template() # Parse schema on init

    def _parse_schema_from_prompt_template(self):
        """Парсит llm_prompt_template.txt для извлечения информации о схеме и сопоставления таблиц с базами данных."""
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm_prompt_template.txt")
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Регулярное выражение для поиска заголовков таблиц и их описаний
            # Пример: ## Таблица: [GRNG/GRMU].[dbo].[FactLoading]
            table_pattern = re.compile(r'## Таблица: \[([^\]]+?)\]\.\[dbo\]\.\[([^\]]+?)\]')
            
            matches = table_pattern.finditer(content)
            
            for match in matches:
                db_name = match.group(1)
                table_name = match.group(2)
                self.table_to_database[table_name] = db_name
                print(f"DEBUG: Mapped table {table_name} to database {db_name}") # For debugging
            
            print(f"DEBUG: Final table_to_database mapping: {self.table_to_database}") # For debugging
            
            # Извлекаем всю секцию "DATABASE SCHEMA" для schema_info
            schema_start = content.find("DATABASE SCHEMA")
            if schema_start != -1:
                self.schema_info = content[schema_start:]
            else:
                self.schema_info = "Schema information not found in prompt template."

        except Exception as e:
            print(f"Ошибка при парсинге llm_prompt_template.txt: {e}")
            self.schema_info = "Error loading schema info."
            self.table_to_database = {}

    def _build_connection_string(self, db_name):
        """Строим строку подключения к указанной базе данных"""
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
        return f"DRIVER={{{driver}}};SERVER={host},{port};DATABASE={db_name};UID={user};PWD={password};"

    def connect(self, db_name):
        """Подключение к указанной базе данных"""
        if db_name not in self.connections or not self.connections[db_name]:
            try:
                print(f"Подключение к базе данных {db_name}...")
                connection_string = self._build_connection_string(db_name)
                self.connections[db_name] = pyodbc.connect(connection_string)
                print(f"Успешное подключение к базе данных {db_name}")
            except Exception as e:
                print(f"Ошибка подключения к базе данных {db_name}: {e}")
                self.connections[db_name] = None
                env_vars = {
                    'DB_HOST': os.getenv('DB_HOST'),
                    'DB_PORT': os.getenv('DB_PORT'),
                    'DB_USER': os.getenv('DB_USER'),
                    'DB_DRIVER': os.getenv('DB_DRIVER'),
                    'DB_NAME_CURRENT_ATTEMPT': db_name
                }
                print(f"Проверьте переменные окружения: {env_vars}")
                return False
        return True

    def execute_query(self, query, db_name):
        """Выполнение SQL запроса в указанной базе данных"""
        if not self.connect(db_name):
            print(f"Не удалось подключиться к базе данных {db_name}")
            return pd.DataFrame()

        try:
            print(f"Выполнение запроса в {db_name}: {query}")
            df = pd.read_sql(query, self.connections[db_name])
            print(f"Запрос выполнен в {db_name}, получено строк: {len(df)}")
            if df.empty:
                print(f"ВНИМАНИЕ: Запрос в {db_name} вернул пустой набор данных")
            return df
        except Exception as e:
            print(f"Ошибка при выполнении запроса в {db_name}: {str(e)}")
            try:
                test_query = "SELECT TOP 1 * FROM INFORMATION_SCHEMA.TABLES"
                print(f"Выполнение диагностического запроса в {db_name}: {test_query}")
                test_df = pd.read_sql(test_query, self.connections[db_name])
                print(f"Диагностический запрос в {db_name} выполнен успешно, таблиц найдено: {len(test_df)}")
            except Exception as test_e:
                print(f"Диагностический запрос в {db_name} также не удался: {str(test_e)}")
            raise e

    def get_table_statistics(self):
        """Получение общей статистики по таблицам из всех настроенных баз данных"""
        all_stats = pd.DataFrame()
        databases_to_check = ['GRNG/GRMU', 'OperativeReport'] # Список баз данных для проверки
        
        for db_name in databases_to_check:
            try:
                query_sqlserver = f"""
                SELECT 
                    '{db_name}' AS DATABASE_NAME,
                    t.name AS TABLE_NAME,
                    p.rows AS TABLE_ROWS,
                    CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36,2)) AS SIZE_MB
                FROM 
                    sys.tables t
                INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
                INNER JOIN sys.partitions p ON i.OBJECT_ID = p.object_id AND i.index_id = p.index_id
                INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
                WHERE t.is_ms_shipped = 0 AND i.OBJECT_ID > 255
                GROUP BY t.Name, p.Rows
                ORDER BY t.Name
                """
                stats = self.execute_query(query_sqlserver, db_name)
                if not stats.empty:
                    all_stats = pd.concat([all_stats, stats], ignore_index=True)
            except Exception as e:
                print(f"Не удалось получить статистику для базы данных {db_name}: {e}")
        return all_stats

    # Removed _parse_schema_file as schema is now embedded in llm_prompt_template.txt

    def get_schema_info(self):
        """Возвращает информацию о схеме базы данных (пустая строка, так как схема теперь в промпте LLM)"""
        return self.schema_info

    def get_table_database(self, table_name):
        """Возвращает базу данных для указанной таблицы, используя предзагруженную карту."""
        db_name = self.table_to_database.get(table_name)
        if not db_name:
            print(f"ПРЕДУПРЕЖДЕНИЕ: База данных для таблицы '{table_name}' не найдена в карте. Используем 'GRNG/GRMU' по умолчанию.")
            return 'GRNG/GRMU' # Fallback to default if not found
        return db_name

class LLMQueryGenerator:
    def __init__(self, model_name=None):
        self.hf_token = os.getenv('HF_TOKEN')
        self.api_url = "https://router.huggingface.co/nebius/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json",
        }
        self.prompt_template_content = self._load_prompt_template()
        
        self.available_models = [
            "Qwen/Qwen3-4B-fast",
            "Qwen/Qwen2.5-Coder-7B", 
            "Qwen/Qwen2.5-Coder-0.5B-Instruct",
            "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
            "codellama/CodeLlama-7b-Instruct-hf",
            "meta-llama/Meta-Llama-3-8B-Instruct"
        ]
        
        self.current_model = model_name or os.getenv('LLM_MODEL', 'Qwen/Qwen3-4B-fast')
        
        if self.current_model not in self.available_models:
            print(f"ВНИМАНИЕ: Неизвестная модель '{self.current_model}'. Доступные модели: {self.available_models}")
            self.current_model = 'Qwen/Qwen3-4B-fast'
        
        print(f"Используется LLM модель: {self.current_model}")
        
        if not self.hf_token:
            print("ВНИМАНИЕ: Не найден токен HuggingFace. Установите переменную окружения HF_TOKEN")

    def _load_prompt_template(self):
        """Загружает шаблон промпта из файла"""
        try:
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm_prompt_template.txt")
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Ошибка при загрузке шаблона промпта: {str(e)}")
            return "" # Возвращаем пустую строку или шаблон по умолчанию

    def get_available_models(self):
        """Возвращает список доступных моделей"""
        return self.available_models

    def set_model(self, model_name):
        """Устанавливает текущую модель"""
        if model_name not in self.available_models:
            raise ValueError(f"Неизвестная модель '{model_name}'. Доступные модели: {self.available_models}")
        
        self.current_model = model_name
        print(f"Модель изменена на: {self.current_model}")
        return True

    def get_current_model(self):
        """Возвращает текущую модель"""
        return {
            "model_name": self.current_model
        }

    def _clean_sql_response(self, text):
        """Очищает ответ от лишних символов и форматирования."""
        # Удаляем теги <think> и </think> если они есть
        if "<think>" in text:
            if "</think>" in text:
                # Удаляем содержимое между <think> и </think>
                text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            else:
                # Удаляем все после <think> если нет закрывающего тега
                text = text.split("<think>")[0]
        
        # Удаляем блоки кода markdown
        if "```sql" in text:
            text = text.split("```sql")[1].split("```")[0]
        elif "```" in text:
            # Обрабатываем случай, когда есть просто ```
            parts = text.split("```")
            if len(parts) >= 3:
                text = parts[1]
        
        # Удаляем возможные префиксы
        text = text.replace("SQL:", "").replace("Query:", "").replace("sql:", "").replace("query:", "")
        
        # Удаляем начальные и конечные пробелы и точки с запятой
        return text.strip().rstrip(';')

    def _validate_sql_tables(self, sql_query): # Removed schema_info parameter
        """Проверяет, что SQL-запрос использует только существующие таблицы из схемы"""
        # This validation is now less effective as schema is not parsed.
        # Relying on LLM to generate correct tables based on its internal prompt.
        # If needed, a more robust validation would require parsing the schema from the prompt itself.
        return True # For now, always return True as schema is not parsed here

    def _generate_sql_query_internal(self, user_request): # Removed schema_info parameter
        """Внутренняя функция для генерации SQL запроса"""
        if not self.is_available():
            raise ConnectionError("HuggingFace API недоступна. Проверьте токен HF_TOKEN.")

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # The prompt_template_content now contains the full schema, so no need to format schema_info
        prompt = self.prompt_template_content.format(
            user_request=user_request,
            current_datetime=current_datetime
        )

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.current_model,
            "max_tokens": 3000,
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
            
            # Removed schema validation here as schema is not parsed by DatabaseManager
            
            return cleaned_query, prompt

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error while contacting HuggingFace API: {e}")
        except Exception as e:
            print(f"An error occurred during SQL generation: {e}")
            raise

    def generate_sql_query(self, user_request):
        """Генерация SQL запроса на основе пользовательского запроса через HuggingFace API"""
        # schema_info is no longer needed here as it's embedded in the prompt template
        cleaned_query, _ = self._generate_sql_query_internal(user_request)
        return cleaned_query

    def generate_sql_query_with_prompt(self, user_request):
        """Генерация SQL запроса с возвратом полного промпта"""
        # schema_info is no longer needed here as it's embedded in the prompt template
        cleaned_query, prompt = self._generate_sql_query_internal(user_request)
        return cleaned_query, prompt

    def is_available(self):
        """Проверка доступности HuggingFace API"""
        return self.hf_token is not None

class ChartGenerator:
    def __init__(self):
        # Настройка matplotlib для русского языка
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
    def create_chart(self, data, chart_type='bar', title='График', x_label='X', y_label='Y'):
        """
        Создает гистограмму (столбчатый график) на основе данных
        
        Args:
            data: DataFrame с данными
            chart_type: тип графика (всегда 'bar' - только гистограммы)
            title: заголовок графика
            x_label: подпись оси X
            y_label: подпись оси Y
        
        Returns:
            base64 строка с изображением графика
        """
        try:
            if data.empty:
                return None
            
            # Создаем фигуру
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Создаем только гистограмму
            self._create_bar_chart(ax, data, title, x_label, y_label)
            
            # Сохраняем в base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            
            # Конвертируем в base64
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            
            # Очищаем память
            plt.close(fig)
            
            return img_base64
            
        except Exception as e:
            print(f"Ошибка при создании графика: {e}")
            return None
    
    def _create_bar_chart(self, ax, data, title, x_label, y_label):
        """Создает столбчатый график"""
        if data.empty or len(data.columns) < 2:
            return

        # Проверяем наличие колонок 'Год' и 'Месяц'
        if 'Год' in data.columns and 'Месяц' in data.columns:
            try:
                # Создаем комбинированную метку для оси X
                data['Год-Месяц'] = data['Год'].astype(str) + '-' + data['Месяц'].astype(str).str.zfill(2)
                data = data.sort_values(['Год', 'Месяц'])
                x_col_plot = 'Год-Месяц'
                
                # Находим колонку со значениями (не 'Год', не 'Месяц', не 'Год-Месяц')
                value_cols = [col for col in data.columns if col not in ['Год', 'Месяц', 'Год-Месяц']]
                if value_cols:
                    y_col = value_cols[0] # Берем первую найденную колонку как значение
                else:
                    # Fallback если не найдено других колонок
                    y_col = data.columns[0] if len(data.columns) > 0 else None
                    if y_col in ['Год', 'Месяц', 'Год-Месяц'] and len(data.columns) > 1:
                        y_col = data.columns[1]
                    elif y_col in ['Год', 'Месяц', 'Год-Месяц'] and len(data.columns) == 1:
                        print("ПРЕДУПРЕЖДЕНИЕ: Недостаточно колонок для построения графика.")
                        return # Не можем построить график без колонки значений
            except Exception as e:
                print(f"Ошибка при создании Год-Месяц для столбчатого графика: {e}")
                # Fallback to original columns
                x_col_plot = data.columns[0]
                y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0]
        else:
            x_col_plot = data.columns[0]
            y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0]

        if y_col is None: # Дополнительная проверка на случай, если y_col не был определен
            return

        # Если слишком много уникальных значений на оси X, лучше использовать линейный график
        if len(data[x_col_plot].unique()) > 15:
            print(f"DEBUG: Too many unique X values ({len(data[x_col_plot].unique())}) for bar chart. Consider line chart.")
            # Можно добавить логику для автоматического переключения на линейный график
            # или просто предупредить и продолжить строить bar chart
            # For now, we'll just proceed with bar chart, but log the warning.

        bars = ax.bar(data[x_col_plot], data[y_col], color='skyblue', alpha=0.8)

        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}',
                    ha='center', va='bottom')

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Поворачиваем подписи на оси X если их много
        if len(data[x_col_plot].unique()) > 5:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    def detect_chart_type(self, data, user_query):
        """
        Определяет подходящий тип графика на основе данных и запроса пользователя
        Всегда возвращает 'bar' так как поддерживаются только гистограммы
        """
        # Всегда возвращаем 'bar' для гистограмм
        print(f"DEBUG: Using 'bar' chart type for query: {user_query}")
        return 'bar'
    
    def generate_chart_title(self, data, user_query):
        """Генерирует заголовок для гистограммы"""
        query_lower = user_query.lower()
        
        if 'выгрузка' in query_lower:
            return 'Гистограмма выгрузки вагонов'
        elif 'погрузка' in query_lower:
            return 'Гистограмма погрузки'
        elif 'род груза' in query_lower:
            return 'Гистограмма по роду груза'
        elif 'грузоотправитель' in query_lower:
            return 'Гистограмма по грузоотправителям'
        elif 'бригада' in query_lower:
            return 'Гистограмма по бригадам'
        else:
            return 'Гистограмма данных'

# --- Инициализация Flask и классов ---

app = Flask(__name__)
app.secret_key = os.getenv('ADMIN_PASS', 'default-secret-key')
db_manager = DatabaseManager()
llm_generator = LLMQueryGenerator()
chart_generator = ChartGenerator()

# --- Маршруты Flask ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.getenv('ADMIN_PASS'):
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверный пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Выход"""
    session.pop('authenticated', None)
    return redirect(url_for('login'))

def require_auth():
    """Проверка аутентификации"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return None

@app.route('/')
def index():
    """Главная страница"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
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
    
    try:
        sql_query = llm_generator.generate_sql_query(user_query)
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
    
    try:
        sql_query, full_prompt = llm_generator.generate_sql_query_with_prompt(user_query)
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
    user_query = data.get('user_query', '')  # Добавляем user_query
    create_chart = data.get('create_chart', False)  # Добавляем create_chart
    if not sql_query:
        return jsonify({"error": "SQL query is required"}), 400

    try:
        # Инициализируем chart_type
        chart_type = None
        
        print(f"Выполняется запрос: {sql_query}")  # Добавляем логирование запроса
        
        # Определяем базу данных автоматически по таблицам в запросе
        # Извлекаем имя таблицы из запроса, предполагая формат [db].[dbo].[Table] или [dbo].[Table]
        # Если LLM генерирует [OperativeReport].[dbo].[EnterpriseWagons], то table_name будет EnterpriseWagons
        # Если LLM генерирует [dbo].[EnterpriseWagons], то table_name будет EnterpriseWagons
        match = re.search(r'FROM\s+(?:\[[^\]]+\]\.)?\[dbo\]\.\[([^\]]+)\]', sql_query, re.IGNORECASE)
        if not match:
            # Если не удалось найти таблицу в формате [dbo].[Table], пробуем найти просто [Table]
            match = re.search(r'FROM\s+\[([^\]]+)\]', sql_query, re.IGNORECASE)
            if not match:
                return jsonify({"error": "Не удалось определить таблицы в SQL запросе"}), 400
        
        first_table = match.group(1)
        db_name = db_manager.get_table_database(first_table)
        
        if not db_name:
            return jsonify({"error": f"Не удалось определить базу данных для таблицы {first_table}"}), 400
        
        print(f"Используется база данных: {db_name} для таблицы: {first_table}")
        
        # Проверяем, содержит ли запрос UNION ALL
        if "UNION ALL" in sql_query.upper():
            print("Обнаружен UNION ALL запрос. Разделяем и выполняем по частям.")
            sub_queries = [s.strip() for s in re.split(r'UNION ALL', sql_query, flags=re.IGNORECASE) if s.strip()]
            
            combined_df = pd.DataFrame()
            errors = []
            
            for sub_q in sub_queries:
                try:
                    sub_match = re.search(r'FROM\s+(?:\[[^\]]+\]\.)?\[dbo\]\.\[([^\]]+)\]', sub_q, re.IGNORECASE)
                    if not sub_match:
                        sub_match = re.search(r'FROM\s+\[([^\]]+)\]', sub_q, re.IGNORECASE)
                        if not sub_match:
                            errors.append(f"Не удалось определить таблицы в подзапросе: {sub_q}")
                            continue
                    
                    sub_first_table = sub_match.group(1)
                    sub_db_name = db_manager.get_table_database(sub_first_table)
                    
                    if not sub_db_name:
                        sub_db_name = 'GRNG/GRMU' # Fallback
                        print(f"ПРЕДУПРЕЖДЕНИЕ: Не найдена база данных для таблицы {sub_first_table} в подзапросе, используем {sub_db_name}")
                    
                    print(f"Выполнение подзапроса в {sub_db_name}: {sub_q}")
                    sub_result_df = db_manager.execute_query(sub_q, sub_db_name)
                    
                    if not sub_result_df.empty:
                        combined_df = pd.concat([combined_df, sub_result_df], ignore_index=True)
                    
                except Exception as sub_e:
                    errors.append(f"Ошибка при выполнении подзапроса '{sub_q}': {str(sub_e)}")
            
            if errors:
                return jsonify({"error": "Произошли ошибки при выполнении некоторых подзапросов: " + "; ".join(errors)}), 500
            
            result_df = combined_df
            
        else:
            # Оригинальная логика для запросов без UNION ALL
            # Проверяем, что все таблицы в запросе из одной базы данных
            # (Этот блок может быть упрощен, так как get_table_database теперь более точен)
            # used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', sql_query) # Re-extract all tables for cross-db check
            # for table in used_tables:
            #     table_db = db_manager.get_table_database(table)
            #     if table_db and table_db != db_name:
            #         return jsonify({"error": f"Ошибка: Таблицы из разных баз данных в одном запросе. Таблица {table} из базы {table_db}, а {first_table} из базы {db_name}"}), 400
            
            # Проверяем соединение с БД перед выполнением
            if not db_manager.connect(db_name):
                return jsonify({"error": f"Не удалось подключиться к базе данных {db_name}"}), 500
            
            result_df = db_manager.execute_query(sql_query, db_name)
        
        if result_df is None or result_df.empty:
            print("Запрос вернул пустой результат")
            return jsonify({"data": [], "chart": None}), 200
            
        # Преобразуем типы данных, которые не сериализуются в JSON
        for col in result_df.columns:
            if pd.api.types.is_datetime64_any_dtype(result_df[col]):
                # Проверяем, есть ли в колонке время, отличное от полуночи
                if not result_df[col].dt.time.eq(datetime.min.time()).all():
                    result_df[col] = result_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    result_df[col] = result_df[col].dt.strftime('%Y-%m-%d')
        
        results = result_df.to_dict(orient='records')
        
        # Создаем график если запрошено
        chart_base64 = None
        if create_chart and len(result_df) > 0:
            # Всегда используем гистограмму (bar chart)
            chart_type = 'bar'
            print(f"DEBUG: Using 'bar' chart type for query: {user_query}")
            
            chart_title = chart_generator.generate_chart_title(result_df, user_query)
            
            # Определяем подписи осей
            if 'Год' in result_df.columns and 'Месяц' in result_df.columns:
                x_label = 'Отчетный период' # Reporting Period
                # Находим колонку со значениями для y_label
                value_cols = [col for col in result_df.columns if col not in ['Год', 'Месяц']]
                y_label = value_cols[0] if value_cols else 'Y'
            else:
                x_label = result_df.columns[0] if len(result_df.columns) > 0 else 'X'
                y_label = result_df.columns[1] if len(result_df.columns) > 1 else 'Y'
            
            chart_base64 = chart_generator.create_chart(
                result_df, chart_type, chart_title, x_label, y_label
            )
        
        print(f"DEBUG: Sending chart_type: {chart_type} in API response for query: {user_query}")
        return jsonify({
            "data": results,
            "chart": chart_base64,
            "chart_type": chart_type if create_chart else None
        })
        
    except Exception as e:
        error_msg = f"Ошибка при выполнении SQL запроса: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500

@app.route('/api/execute-sql-with-chart', methods=['POST'])
def execute_sql_with_chart():
    """API для выполнения SQL с автоматическим созданием графика"""
    data = request.json
    sql_query = data.get('query')
    user_query = data.get('user_query', '')
    
    if not sql_query:
        return jsonify({"error": "SQL query is required"}), 400
    
    # Автоматически включаем создание графика
    data['create_chart'] = True
    
    # Вызываем основную функцию execute_sql
    try:
        # Инициализируем chart_type
        chart_type = None
        
        print(f"Выполняется запрос: {sql_query}")  # Добавляем логирование запроса
        
        # Определяем базу данных автоматически по таблицам в запросе
        match = re.search(r'FROM\s+(?:\[[^\]]+\]\.)?\[dbo\]\.\[([^\]]+)\]', sql_query, re.IGNORECASE)
        if not match:
            match = re.search(r'FROM\s+\[([^\]]+)\]', sql_query, re.IGNORECASE)
            if not match:
                return jsonify({"error": "Не удалось определить таблицы в SQL запросе"}), 400
        
        first_table = match.group(1)
        db_name = db_manager.get_table_database(first_table)
        
        if not db_name:
            return jsonify({"error": f"Не удалось определить базу данных для таблицы {first_table}"}), 400
        
        print(f"Используется база данных: {db_name} для таблицы: {first_table}")
        
        # Проверяем, есть ли UNION ALL в запросе
        if 'UNION ALL' in sql_query.upper():
            # Обрабатываем запрос с UNION ALL
            sub_queries = [s.strip() for s in re.split(r'UNION ALL', sql_query, flags=re.IGNORECASE) if s.strip()]
            
            combined_df = pd.DataFrame()
            errors = []
            
            for sub_q in sub_queries:
                try:
                    sub_match = re.search(r'FROM\s+(?:\[[^\]]+\]\.)?\[dbo\]\.\[([^\]]+)\]', sub_q, re.IGNORECASE)
                    if not sub_match:
                        sub_match = re.search(r'FROM\s+\[([^\]]+)\]', sub_q, re.IGNORECASE)
                        if not sub_match:
                            errors.append(f"Не удалось определить таблицы в подзапросе: {sub_q}")
                            continue
                    
                    sub_first_table = sub_match.group(1)
                    sub_db_name = db_manager.get_table_database(sub_first_table)
                    
                    if not sub_db_name:
                        sub_db_name = 'GRNG/GRMU' # Fallback
                        print(f"ПРЕДУПРЕЖДЕНИЕ: Не найдена база данных для таблицы {sub_first_table} в подзапросе, используем {sub_db_name}")
                    
                    print(f"Выполнение подзапроса в {sub_db_name}: {sub_q}")
                    sub_result_df = db_manager.execute_query(sub_q, sub_db_name)
                    
                    if not sub_result_df.empty:
                        combined_df = pd.concat([combined_df, sub_result_df], ignore_index=True)
                    
                except Exception as sub_e:
                    errors.append(f"Ошибка при выполнении подзапроса '{sub_q}': {str(sub_e)}")
            
            if errors:
                return jsonify({"error": "Произошли ошибки при выполнении некоторых подзапросов: " + "; ".join(errors)}), 500
            
            result_df = combined_df
            
        else:
            # Оригинальная логика для запросов без UNION ALL
            # used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', sql_query) # Re-extract all tables for cross-db check
            # for table in used_tables:
            #     table_db = db_manager.get_table_database(table)
            #     if table_db and table_db != db_name:
            #         return jsonify({"error": f"Ошибка: Таблицы из разных баз данных в одном запросе. Таблица {table} из базы {table_db}, а {first_table} из базы {db_name}"}), 400
            
            # Проверяем соединение с БД перед выполнением
            if not db_manager.connect(db_name):
                return jsonify({"error": f"Не удалось подключиться к базе данных {db_name}"}), 500
            
            # Выполняем запрос
            result_df = db_manager.execute_query(sql_query, db_name)
        
        if result_df.empty:
            return jsonify({"data": [], "chart": None, "chart_type": None})
        
        # Преобразуем datetime в строку для JSON
        for col in result_df.columns:
            if pd.api.types.is_datetime64_any_dtype(result_df[col]):
                # Проверяем, есть ли в колонке время, отличное от полуночи
                if not result_df[col].dt.time.eq(datetime.min.time()).all():
                    result_df[col] = result_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    result_df[col] = result_df[col].dt.strftime('%Y-%m-%d')
        
        results = result_df.to_dict(orient='records')
        
        # Создаем график - всегда, так как это эндпоинт с графиком
        chart_base64 = None
        create_chart = True  # Принудительно включаем создание графика
        
        if create_chart and len(result_df) > 0:
            # Всегда используем гистограмму (bar chart)
            chart_type = 'bar'
            print(f"DEBUG: Using 'bar' chart type for query: {user_query}")
            
            chart_title = chart_generator.generate_chart_title(result_df, user_query)
            
            # Определяем подписи осей
            if 'Год' in result_df.columns and 'Месяц' in result_df.columns:
                x_label = 'Отчетный период' # Reporting Period
                # Находим колонку со значениями для y_label
                value_cols = [col for col in result_df.columns if col not in ['Год', 'Месяц']]
                y_label = value_cols[0] if value_cols else 'Y'
            else:
                x_label = result_df.columns[0] if len(result_df.columns) > 0 else 'X'
                y_label = result_df.columns[1] if len(result_df.columns) > 1 else 'Y'
            
            chart_base64 = chart_generator.create_chart(
                result_df, chart_type, chart_title, x_label, y_label
            )
        
        print(f"DEBUG: Sending chart_type: {chart_type} in API response for query: {user_query}")
        return jsonify({
            "data": results,
            "chart": chart_base64,
            "chart_type": chart_type if create_chart else None
        })
    except Exception as e:
        error_msg = f"Ошибка при выполнении SQL запроса: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    print("Запуск Flask приложения...")
    print(f"Доступно по адресу: http://127.0.0.1:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
