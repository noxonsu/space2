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
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# --- Классы для работы с БД и LLM (адаптированные) ---

class DatabaseManager:
    def __init__(self):
        self.connections = {}  # Словарь для хранения подключений к разным базам данных
        self.schema_info, self.table_to_database = self._parse_schema_file()

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
                INNER JOIN sys.partitions p ON i.OBJECT_ID = p.OBJECT_ID AND i.index_id = p.index_id
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

    def _parse_schema_file(self):
        """Загружает и обрабатывает файл схемы базы данных"""
        try:
            schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_shema.sql")
            if not os.path.exists(schema_path):
                print(f"ПРЕДУПРЕЖДЕНИЕ: Файл схемы не найден: {schema_path}")
                return "", {}
                
            with open(schema_path, 'r', encoding='utf-8') as file:
                schema_content = file.read()
                
            # Извлекаем информацию о таблицах из схемы с указанием базы данных
            table_info = {}
            table_to_database = {}  # Маппинг таблица -> база данных
            current_table = None
            current_database = None
            
            for line in schema_content.split('\n'):
                line = line.strip()
                
                # Ищем определения баз данных
                if line.startswith('-- БАЗА ДАННЫХ:'):
                    current_database = line.split('-- БАЗА ДАННЫХ:')[1].strip()
                    continue
                
                # Ищем определения таблиц
                if line.startswith('CREATE TABLE') or line.startswith('-- Таблица:'):
                    # Из строки вида "CREATE TABLE [dbo].[TableName]" извлекаем TableName
                    if 'CREATE TABLE' in line:
                        match = line.split('[dbo].[')[1].split(']')[0] if '[dbo].[' in line else None
                        if match:
                            current_table = match
                            table_info[current_table] = []
                            if current_database:
                                table_to_database[current_table] = current_database
                    elif '-- Таблица:' in line:
                        # Из строки вида "-- Таблица: dbo.TableName" извлекаем TableName
                        parts = line.split('-- Таблица: dbo.')[1] if '-- Таблица: dbo.' in line else line.split('-- Таблица: ')[1]
                        current_table = parts.strip()
                        table_info[current_table] = []
                        if current_database:
                            table_to_database[current_table] = current_database
                
                # Если мы внутри определения таблицы и нашли столбец
                elif current_table and ('[' in line or 'nvarchar' in line or 'int' in line or 'float' in line or 'date' in line):
                    if '[' in line:
                        # Извлекаем имя столбца в квадратных скобках
                        column = line.split('[')[1].split(']')[0] if '[' in line else None
                        if column:
                            table_info[current_table].append(column)
            
            # Форматируем информацию для использования в промпте LLM
            formatted_schema = "ДОСТУПНЫЕ ТАБЛИЦЫ И СТОЛБЦЫ (используйте ТОЛЬКО эти названия):\n\n"
            
            # Группируем таблицы по базам данных
            databases = {}
            for table, database in table_to_database.items():
                if database not in databases:
                    databases[database] = []
                databases[database].append(table)
            
            # Отсортируем и отформатируем по базам данных
            for database in sorted(databases.keys()):
                formatted_schema += f"=== БАЗА ДАННЫХ: {database} ===\n"
                for table in sorted(databases[database]):
                    columns = ", ".join([f"[{col}]" for col in table_info[table][:15]])  # Увеличил лимит до 15 столбцов
                    if len(table_info[table]) > 15:
                        columns += ", ..."
                    formatted_schema += f"Таблица [dbo].[{table}]:\n   Столбцы: {columns}\n\n"
                formatted_schema += "\n"
            
            formatted_schema += """
ПРАВИЛА ГЕНЕРАЦИИ SQL:
- Используйте ТОЛЬКО таблицы и столбцы, перечисленные выше
- Формат таблицы: [dbo].[ИмяТаблицы] 
- Формат столбца: [ИмяСтолбца]
- Для подсчета используйте COUNT(*)
- Для ограничения результатов используйте TOP N (не LIMIT)
- Для дат используйте GETDATE(), DATEADD(), YEAR(), MONTH()
- ВНИМАНИЕ: Таблицы находятся в разных базах данных, но всегда используйте только [dbo].[ИмяТаблицы]

ПРИМЕРЫ КОРРЕКТНЫХ ЗАПРОСОВ:
- SELECT COUNT(*) FROM [dbo].[EnterpriseWagons]
- SELECT TOP 5 [Груз] FROM [dbo].[VagonImport]
- SELECT [Род груза], COUNT(*) FROM [dbo].[VagonImport] GROUP BY [Род груза]
"""
            
            print(f"Схема базы данных успешно загружена из {schema_path}")
            print(f"Найдено таблиц: {len(table_info)}")
            print(f"Найдено баз данных: {len(databases)}")
            return formatted_schema, table_to_database
            
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
""", {}

    def get_schema_info(self):
        """Возвращает информацию о схеме базы данных"""
        return self.schema_info

    def get_table_database(self, table_name):
        """Возвращает базу данных для указанной таблицы"""
        return self.table_to_database.get(table_name)

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
                import re
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

    def _validate_sql_tables(self, sql_query, schema_info):
        """Проверяет, что SQL-запрос использует только существующие таблицы из схемы"""
        available_tables = []
        # Extract table names from the schema_info string
        for line in schema_info.split('\n'):
            if line.strip().startswith('Таблица [dbo].['):
                table_name = line.split('[dbo].[')[1].split(']')[0]
                available_tables.append(table_name)
        
        import re
        used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', sql_query)
        
        for used_table in used_tables:
            if used_table not in available_tables:
                raise Exception(f"LLM использовал несуществующую таблицу: {used_table}. Доступные таблицы: {', '.join(available_tables)}")
        
        return True

    def _generate_sql_query_internal(self, user_request, schema_info):
        """Внутренняя функция для генерации SQL запроса"""
        if not self.is_available():
            raise ConnectionError("HuggingFace API недоступна. Проверьте токен HF_TOKEN.")

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Используем загруженный шаблон промпта
        prompt = self.prompt_template_content.format(
            schema_info=schema_info,
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

    def generate_sql_query(self, user_request):
        """Генерация SQL запроса на основе пользовательского запроса через HuggingFace API"""
        schema_info = db_manager.get_schema_info() # Get schema dynamically
        cleaned_query, _ = self._generate_sql_query_internal(user_request, schema_info)
        return cleaned_query

    def generate_sql_query_with_prompt(self, user_request):
        """Генерация SQL запроса с возвратом полного промпта"""
        schema_info = db_manager.get_schema_info() # Get schema dynamically
        cleaned_query, prompt = self._generate_sql_query_internal(user_request, schema_info)
        return cleaned_query, prompt

    def is_available(self):
        """Проверка доступности HuggingFace API"""
        return self.hf_token is not None

class ChartGenerator:
    def __init__(self):
        # Настройка matplotlib для русского языка
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
    def create_chart(self, data, chart_type='line', title='График', x_label='X', y_label='Y'):
        """
        Создает график на основе данных
        
        Args:
            data: DataFrame с данными
            chart_type: тип графика ('line', 'bar', 'pie')
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
            
            # Определяем тип графика
            if chart_type == 'line':
                self._create_line_chart(ax, data, title, x_label, y_label)
            elif chart_type == 'bar':
                self._create_bar_chart(ax, data, title, x_label, y_label)
            elif chart_type == 'pie':
                self._create_pie_chart(ax, data, title)
            else:
                # По умолчанию линейный график
                self._create_line_chart(ax, data, title, x_label, y_label)
            
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
    
    def _create_line_chart(self, ax, data, title, x_label, y_label):
        """Создает линейный график"""
        if len(data.columns) >= 2:
            x_col = data.columns[0]
            y_col = data.columns[1]
            
            # Если есть даты, конвертируем их
            if any(keyword in x_col.lower() for keyword in ['дата', 'месяц', 'год', 'время']):
                try:
                    # Пытаемся конвертировать в даты
                    if data[x_col].dtype == 'object':
                        # Если это строки, пытаемся парсить
                        data[x_col] = pd.to_datetime(data[x_col], errors='coerce')
                    
                    ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, markersize=6)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
                    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                except:
                    ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, markersize=6)
            else:
                ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, markersize=6)
            
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
    
    def _create_bar_chart(self, ax, data, title, x_label, y_label):
        """Создает столбчатый график"""
        if len(data.columns) >= 2:
            x_col = data.columns[0]
            y_col = data.columns[1]
            
            bars = ax.bar(data[x_col], data[y_col], color='skyblue', alpha=0.8)
            
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
            if len(data) > 5:
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _create_pie_chart(self, ax, data, title):
        """Создает круговую диаграмму"""
        if len(data.columns) >= 2:
            labels_col = data.columns[0]
            values_col = data.columns[1]
            
            # Берем только топ-10 значений для читаемости
            top_data = data.nlargest(10, values_col)
            
            colors = plt.cm.Set3(range(len(top_data)))
            wedges, texts, autotexts = ax.pie(top_data[values_col], 
                                            labels=top_data[labels_col],
                                            autopct='%1.1f%%',
                                            colors=colors,
                                            startangle=90)
            
            ax.set_title(title, fontsize=14, fontweight='bold')
            
            # Улучшаем читаемость
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
    
    def detect_chart_type(self, data, user_query):
        """
        Определяет подходящий тип графика на основе данных и запроса пользователя
        """
        query_lower = user_query.lower()
        
        # Круговая диаграмма - для разбивки по категориям
        if any(keyword in query_lower for keyword in ['разрез', 'доля', 'процент', 'распределение']):
            return 'pie'
        
        # Столбчатая диаграмма - для сравнения значений
        elif any(keyword in query_lower for keyword in ['сравни', 'топ', 'больше', 'меньше']):
            return 'bar'
        
        # Линейный график - для временных рядов
        elif any(keyword in query_lower for keyword in ['динамика', 'менял', 'тренд', 'время', 'год', 'месяц']):
            return 'line'
        
        # По умолчанию - линейный график
        return 'line'
    
    def generate_chart_title(self, data, user_query):
        """Генерирует заголовок для графика"""
        query_lower = user_query.lower()
        
        if 'выгрузка' in query_lower:
            return 'Динамика выгрузки вагонов'
        elif 'погрузка' in query_lower:
            return 'Динамика погрузки'
        elif 'род груза' in query_lower:
            return 'Распределение по роду груза'
        elif 'грузоотправитель' in query_lower:
            return 'Распределение по грузоотправителям'
        else:
            return 'График данных'

# --- Инициализация Flask и классов ---

app = Flask(__name__)
db_manager = DatabaseManager()
llm_generator = LLMQueryGenerator()
chart_generator = ChartGenerator()

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
        
        # Определяем базу данных автоматически по таблицам в запросе
        import re
        used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', sql_query)
        
        if not used_tables:
            return jsonify({"error": "Не удалось определить таблицы в SQL запросе"}), 400
        
        # Берем первую таблицу для определения базы данных
        first_table = used_tables[0]
        db_name = db_manager.get_table_database(first_table)
        
        if not db_name:
            # Если база данных не найдена, пробуем стандартные базы
            db_name = 'GRNG/GRMU'  # База данных по умолчанию
            print(f"ПРЕДУПРЕЖДЕНИЕ: Не найдена база данных для таблицы {first_table}, используем {db_name}")
        
        print(f"Используется база данных: {db_name} для таблицы: {first_table}")
        
        # Проверяем, что все таблицы в запросе из одной базы данных
        for table in used_tables:
            table_db = db_manager.get_table_database(table)
            if table_db and table_db != db_name:
                return jsonify({"error": f"Ошибка: Таблицы из разных баз данных в одном запросе. Таблица {table} из базы {table_db}, а {first_table} из базы {db_name}"}), 400
        
        # Проверяем соединение с БД перед выполнением
        if not db_manager.connect(db_name):
            return jsonify({"error": f"Не удалось подключиться к базе данных {db_name}"}), 500
        
        result_df = db_manager.execute_query(sql_query, db_name)
        
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
                            alt_df = db_manager.execute_query(alt_query, db_name)
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

@app.route('/api/models')
def get_models():
    """Получение списка доступных моделей"""
    try:
        models = llm_generator.get_available_models()
        current_model = llm_generator.get_current_model()
        return jsonify({
            'models': models,
            'current_model': current_model['model_name']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/set', methods=['POST'])
def set_model():
    """Установка текущей модели"""
    try:
        data = request.get_json()
        model_name = data.get('model_name')
        
        if not model_name:
            return jsonify({'error': 'model_name is required'}), 400
        
        llm_generator.set_model(model_name)
        return jsonify({'success': True, 'current_model': model_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/execute-sql-with-chart', methods=['POST'])
def execute_sql_with_chart():
    """API для выполнения SQL с созданием графика"""
    data = request.json
    sql_query = data.get('query')
    user_query = data.get('user_query', '')
    create_chart = data.get('create_chart', False)
    
    if not sql_query:
        return jsonify({"error": "SQL query is required"}), 400

    try:
        # Проверяем и добавляем схему dbo, если она не указана
        if "FROM " in sql_query and "[dbo]." not in sql_query and "dbo." not in sql_query:
            # Находим имена таблиц после FROM и JOIN
            tables = re.findall(r'FROM\s+([^\s,;()]+)|JOIN\s+([^\s,;()]+)', sql_query, re.IGNORECASE)
            # Объединяем все найденные группы и удаляем пустые значения
            tables = [t for group in tables for t in group if t]
            
            # Добавляем префикс [dbo]. к таблицам, если их еще нет
            for table in tables:
                if not table.startswith('[dbo].') and not table.startswith('dbo.'):
                    # Заменяем, только если это не подзапрос
                    sql_query = sql_query.replace(f"FROM {table}", f"FROM [dbo].[{table}]")
                    sql_query = sql_query.replace(f"JOIN {table}", f"JOIN [dbo].[{table}]")
        
        print(f"Выполняется запрос: {sql_query}")
        
        # Определяем базу данных автоматически по таблицам в запросе
        used_tables = re.findall(r'\[dbo\]\.\[([^\]]+)\]', sql_query)
        
        if not used_tables:
            return jsonify({"error": "Не удалось определить таблицы в SQL запросе"}), 400
        
        # Берем первую таблицу для определения базы данных
        first_table = used_tables[0]
        db_name = db_manager.get_table_database(first_table)
        
        if not db_name:
            # Если база данных не найдена, пробуем стандартные базы
            db_name = 'GRNG/GRMU'  # База данных по умолчанию
            print(f"ПРЕДУПРЕЖДЕНИЕ: Не найдена база данных для таблицы {first_table}, используем {db_name}")
        
        print(f"Используется база данных: {db_name} для таблицы: {first_table}")
        
        # Проверяем, что все таблицы в запросе из одной базы данных
        for table in used_tables:
            table_db = db_manager.get_table_database(table)
            if table_db and table_db != db_name:
                return jsonify({"error": f"Ошибка: Таблицы из разных баз данных в одном запросе. Таблица {table} из базы {table_db}, а {first_table} из базы {db_name}"}), 400
        
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
                result_df[col] = result_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        results = result_df.to_dict(orient='records')
        
        # Создаем график если запрошено
        chart_base64 = None
        if create_chart and len(result_df) > 0:
            chart_type = chart_generator.detect_chart_type(result_df, user_query)
            chart_title = chart_generator.generate_chart_title(result_df, user_query)
            
            # Определяем подписи осей
            x_label = result_df.columns[0] if len(result_df.columns) > 0 else 'X'
            y_label = result_df.columns[1] if len(result_df.columns) > 1 else 'Y'
            
            chart_base64 = chart_generator.create_chart(
                result_df, chart_type, chart_title, x_label, y_label
            )
        
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
    print(f"Доступно по адресу: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
