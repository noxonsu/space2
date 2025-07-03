import os
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import json

# Загружаем переменные окружения
load_dotenv()

class DatabaseAdmin:
    def __init__(self):
        self.connection_string = self._build_connection_string()
        self.connection = None
        
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
            self.connection = pyodbc.connect(self.connection_string)
            print(f"✅ Успешное подключение к базе данных OperativeReport!")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            return False
    
    def disconnect(self):
        """Отключение от базы данных"""
        if self.connection:
            self.connection.close()
            print("🔌 Соединение с базой данных закрыто")
    
    def execute_query(self, query, params=None):
        """Выполнение SQL запроса"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            df = pd.read_sql(query, self.connection, params=params)
            return df
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None
    
    def get_table_statistics(self):
        """Получение статистики по всем таблицам"""
        query = """
        SELECT 
            t.TABLE_NAME as 'Таблица',
            p.rows as 'Количество записей',
            (p.reserved * 8) as 'Размер (KB)',
            CAST((p.reserved * 8.0 / 1024) as DECIMAL(10,2)) as 'Размер (MB)',
            c.column_count as 'Количество столбцов'
        FROM INFORMATION_SCHEMA.TABLES t
        LEFT JOIN (
            SELECT 
                i.name,
                SUM(p.rows) as rows,
                SUM(a.total_pages) as reserved
            FROM sys.tables i
            INNER JOIN sys.partitions p ON i.object_id = p.object_id
            INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            GROUP BY i.name
        ) p ON t.TABLE_NAME = p.name
        LEFT JOIN (
            SELECT 
                TABLE_NAME,
                COUNT(*) as column_count
            FROM INFORMATION_SCHEMA.COLUMNS
            GROUP BY TABLE_NAME
        ) c ON t.TABLE_NAME = c.TABLE_NAME
        WHERE t.TABLE_TYPE = 'BASE TABLE'
        ORDER BY p.rows DESC
        """
        return self.execute_query(query)
    
    def get_table_details(self, table_name):
        """Получение детальной информации о таблице"""
        query = f"""
        SELECT 
            COLUMN_NAME as 'Столбец',
            DATA_TYPE as 'Тип данных',
            CHARACTER_MAXIMUM_LENGTH as 'Максимальная длина',
            IS_NULLABLE as 'Может быть NULL',
            COLUMN_DEFAULT as 'Значение по умолчанию'
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        return self.execute_query(query)
    
    def get_table_sample_data(self, table_name, limit=10):
        """Получение примера данных из таблицы"""
        query = f"SELECT TOP {limit} * FROM [{table_name}]"
        return self.execute_query(query)
    
    def get_date_range_analysis(self):
        """Анализ диапазонов дат в таблицах с датами"""
        tables_with_dates = {
            'EnterpriseWagons': '[Дата]',
            'ShipmentsToThePort': '[Дата]',
            'ContainerStorage': '[Дата]',
            'PlanShipsIlsar': '[Дата]',
            'ShipsImport': '[Начальная дата подхода]',
            'SSP': '[Дата]',
            'VagonImport': '[Дата]',
            'WagonsOnTheWay': '[Дата]',
            'WagonsPresence': '[Дата]'
        }
        
        results = []
        for table, date_column in tables_with_dates.items():
            query = f"""
            SELECT 
                '{table}' as 'Таблица',
                MIN({date_column}) as 'Минимальная дата',
                MAX({date_column}) as 'Максимальная дата',
                DATEDIFF(day, MIN({date_column}), MAX({date_column})) as 'Диапазон (дни)',
                COUNT(*) as 'Записей с датами'
            FROM [{table}]
            WHERE {date_column} IS NOT NULL
            """
            df = self.execute_query(query)
            if df is not None and not df.empty:
                results.append(df)
        
        if results:
            return pd.concat(results, ignore_index=True)
        return pd.DataFrame()
    
    def get_cargo_statistics(self):
        """Статистика по родам груза"""
        query = """
        SELECT 
            'EnterpriseWagons' as 'Таблица',
            [Род груза],
            COUNT(*) as 'Количество записей',
            SUM([Вес груза принятый (т)]) as 'Общий вес (т)'
        FROM [EnterpriseWagons]
        WHERE [Род груза] IS NOT NULL
        GROUP BY [Род груза]
        
        UNION ALL
        
        SELECT 
            'ShipmentsToThePort' as 'Таблица',
            [Род груза],
            COUNT(*) as 'Количество записей',
            SUM([Вес груза отправленный(т)]) as 'Общий вес (т)'
        FROM [ShipmentsToThePort]
        WHERE [Род груза] IS NOT NULL
        GROUP BY [Род груза]
        
        UNION ALL
        
        SELECT 
            'VagonImport' as 'Таблица',
            [Род груза],
            COUNT(*) as 'Количество записей',
            SUM([Вес нетто (т)]) as 'Общий вес (т)'
        FROM [VagonImport]
        WHERE [Род груза] IS NOT NULL
        GROUP BY [Род груза]
        
        ORDER BY [Общий вес (т)] DESC
        """
        return self.execute_query(query)
    
    def get_monthly_activity(self):
        """Активность по месяцам за последний год"""
        query = """
        SELECT 
            'EnterpriseWagons' as 'Таблица',
            YEAR([Дата]) as 'Год',
            MONTH([Дата]) as 'Месяц',
            COUNT(*) as 'Количество записей'
        FROM [EnterpriseWagons]
        WHERE [Дата] >= DATEADD(year, -1, GETDATE())
        GROUP BY YEAR([Дата]), MONTH([Дата])
        
        UNION ALL
        
        SELECT 
            'ShipmentsToThePort' as 'Таблица',
            YEAR([Дата]) as 'Год',
            MONTH([Дата]) as 'Месяц',
            COUNT(*) as 'Количество записей'
        FROM [ShipmentsToThePort]
        WHERE [Дата] >= DATEADD(year, -1, GETDATE())
        GROUP BY YEAR([Дата]), MONTH([Дата])
        
        UNION ALL
        
        SELECT 
            'VagonImport' as 'Таблица',
            YEAR([Дата]) as 'Год',
            MONTH([Дата]) as 'Месяц',
            COUNT(*) as 'Количество записей'
        FROM [VagonImport]
        WHERE [Дата] >= DATEADD(year, -1, GETDATE())
        GROUP BY YEAR([Дата]), MONTH([Дата])
        
        ORDER BY Год, Месяц
        """
        return self.execute_query(query)
    
    def create_dashboard_html(self):
        """Создание HTML дашборда с статистикой"""
        if not self.connect():
            return None
        
        # Получаем все статистики
        table_stats = self.get_table_statistics()
        date_analysis = self.get_date_range_analysis()
        cargo_stats = self.get_cargo_statistics()
        monthly_activity = self.get_monthly_activity()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Администрирование БД OperativeReport</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1, h2 {{
                    color: #333;
                    border-bottom: 2px solid #4CAF50;
                    padding-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .stats-card {{
                    background-color: #e8f5e8;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border-left: 5px solid #4CAF50;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left-color: #ffc107;
                }}
                .info {{
                    background-color: #d1ecf1;
                    border-left-color: #17a2b8;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🗄️ Администрирование БД OperativeReport</h1>
                <div class="stats-card info">
                    <strong>Время генерации отчета:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
        """
        
        # Добавляем статистику по таблицам
        if table_stats is not None and not table_stats.empty:
            total_records = table_stats['Количество записей'].sum()
            total_size_mb = table_stats['Размер (MB)'].sum()
            
            html_content += f"""
                <div class="stats-card">
                    <h3>📊 Общая статистика</h3>
                    <p><strong>Всего таблиц:</strong> {len(table_stats)}</p>
                    <p><strong>Всего записей:</strong> {total_records:,}</p>
                    <p><strong>Общий размер:</strong> {total_size_mb:.2f} MB</p>
                </div>
                
                <h2>📋 Статистика по таблицам</h2>
                <table>
                    <tr>
                        <th>Таблица</th>
                        <th>Записей</th>
                        <th>Размер (MB)</th>
                        <th>Столбцов</th>
                    </tr>
            """
            
            for _, row in table_stats.iterrows():
                html_content += f"""
                    <tr>
                        <td><strong>{row['Таблица']}</strong></td>
                        <td>{row['Количество записей']:,}</td>
                        <td>{row['Размер (MB)']:.2f}</td>
                        <td>{row['Количество столбцов']}</td>
                    </tr>
                """
            html_content += "</table>"
        
        # Добавляем анализ диапазонов дат
        if date_analysis is not None and not date_analysis.empty:
            html_content += """
                <h2>📅 Анализ временных диапазонов</h2>
                <table>
                    <tr>
                        <th>Таблица</th>
                        <th>Минимальная дата</th>
                        <th>Максимальная дата</th>
                        <th>Диапазон (дни)</th>
                        <th>Записей с датами</th>
                    </tr>
            """
            
            for _, row in date_analysis.iterrows():
                html_content += f"""
                    <tr>
                        <td><strong>{row['Таблица']}</strong></td>
                        <td>{row['Минимальная дата']}</td>
                        <td>{row['Максимальная дата']}</td>
                        <td>{row['Диапазон (дни)']:,}</td>
                        <td>{row['Записей с датами']:,}</td>
                    </tr>
                """
            html_content += "</table>"
        
        # Добавляем статистику по грузам
        if cargo_stats is not None and not cargo_stats.empty:
            html_content += """
                <h2>📦 Топ-20 родов груза по весу</h2>
                <table>
                    <tr>
                        <th>Таблица</th>
                        <th>Род груза</th>
                        <th>Записей</th>
                        <th>Общий вес (т)</th>
                    </tr>
            """
            
            for _, row in cargo_stats.head(20).iterrows():
                weight = row['Общий вес (т)'] if pd.notna(row['Общий вес (т)']) else 0
                html_content += f"""
                    <tr>
                        <td><strong>{row['Таблица']}</strong></td>
                        <td>{row['Род груза']}</td>
                        <td>{row['Количество записей']:,}</td>
                        <td>{weight:,.2f}</td>
                    </tr>
                """
            html_content += "</table>"
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Сохраняем HTML файл
        with open('/workspaces/aeroclub_repo/vagon/admin_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("📊 HTML дашборд создан: admin_dashboard.html")
        self.disconnect()
        return html_content
    
    def print_full_statistics(self):
        """Вывод полной статистики в консоль"""
        if not self.connect():
            return
        
        print("=" * 80)
        print("🗄️  АДМИНИСТРИРОВАНИЕ БД OperativeReport")
        print("=" * 80)
        
        # Статистика по таблицам
        print("\n📋 СТАТИСТИКА ПО ТАБЛИЦАМ:")
        print("-" * 80)
        table_stats = self.get_table_statistics()
        if table_stats is not None and not table_stats.empty:
            print(table_stats.to_string(index=False))
            
            total_records = table_stats['Количество записей'].sum()
            total_size_mb = table_stats['Размер (MB)'].sum()
            print(f"\n📊 ИТОГО: {len(table_stats)} таблиц, {total_records:,} записей, {total_size_mb:.2f} MB")
        
        # Анализ диапазонов дат
        print("\n📅 АНАЛИЗ ВРЕМЕННЫХ ДИАПАЗОНОВ:")
        print("-" * 80)
        date_analysis = self.get_date_range_analysis()
        if date_analysis is not None and not date_analysis.empty:
            print(date_analysis.to_string(index=False))
        
        # Статистика по грузам
        print("\n📦 ТОП-15 РОДОВ ГРУЗА ПО ВЕСУ:")
        print("-" * 80)
        cargo_stats = self.get_cargo_statistics()
        if cargo_stats is not None and not cargo_stats.empty:
            print(cargo_stats.head(15).to_string(index=False))
        
        # Месячная активность
        print("\n📈 АКТИВНОСТЬ ПО МЕСЯЦАМ (последний год):")
        print("-" * 80)
        monthly_activity = self.get_monthly_activity()
        if monthly_activity is not None and not monthly_activity.empty:
            print(monthly_activity.to_string(index=False))
        
        self.disconnect()

# Основная функция для запуска
def main():
    admin = DatabaseAdmin()
    
    print("Выберите действие:")
    print("1. Показать статистику в консоли")
    print("2. Создать HTML дашборд")
    print("3. Оба варианта")
    
    choice = input("Введите номер (1-3): ").strip()
    
    if choice in ['1', '3']:
        admin.print_full_statistics()
    
    if choice in ['2', '3']:
        admin.create_dashboard_html()
        print("\n🌐 Для просмотра дашборда откройте файл admin_dashboard.html в браузере")

if __name__ == "__main__":
    main()
