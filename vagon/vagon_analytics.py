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

# Загружаем переменные окружения
load_dotenv()

class VagonAnalytics:
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
            print("Успешное подключение к базе данных!")
            return True
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return False
    
    def disconnect(self):
        """Отключение от базы данных"""
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")
    
    def execute_query(self, query, params=None):
        """Выполнение SQL запроса"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            df = pd.read_sql(query, self.connection, params=params)
            return df
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None
    
    def get_vagon_unloading_monthly(self, years=2):
        """
        1. Покажи, как менялась выгрузка вагонов в течение 2 последних лет, ежемесячно
        Используем таблицу VagonImport - данные о выгрузке вагонов
        """
        query = """
        SELECT 
            YEAR([Дата и время погрузки]) as year,
            MONTH([Дата и время погрузки]) as month,
            COUNT(*) as vagon_count,
            SUM([Вес нетто (т)]) as total_weight
        FROM [dbo].[VagonImport]
        WHERE [Дата и время погрузки] >= DATEADD(year, -?, GETDATE())
            AND [Операция] LIKE '%выгрузка%' OR [Операция] LIKE '%разгрузка%'
        GROUP BY YEAR([Дата и время погрузки]), MONTH([Дата и время погрузки])
        ORDER BY year, month
        """
        return self.execute_query(query, [years])
    
    def get_ship_loading_monthly(self, years=2):
        """
        2. Как менялся показатель среднемесячной погрузки на суда последние 2 года
        Используем таблицу ShipsImport - данные о погрузке судов
        """
        query = """
        SELECT 
            YEAR([Начальная дата подхода]) as year,
            MONTH([Начальная дата подхода]) as month,
            AVG([Вес нетто (т)]) as avg_monthly_loading,
            COUNT(*) as ship_count
        FROM [dbo].[ShipsImport]
        WHERE [Начальная дата подхода] >= DATEADD(year, -?, GETDATE())
            AND [Тип операции] LIKE '%погрузка%'
        GROUP BY YEAR([Начальная дата подхода]), MONTH([Начальная дата подхода])
        ORDER BY year, month
        """
        return self.execute_query(query, [years])
    
    def get_unloading_time_by_platform(self):
        """
        3. Как менялся показатель времени выгрузки вагона в зависимости от площадок выгрузки
        Используем таблицу VagonImport с площадками
        """
        query = """
        SELECT 
            [Площадка],
            COUNT(*) as vagon_count,
            AVG([Вес нетто (т)]) as avg_weight,
            [Род груза]
        FROM [dbo].[VagonImport]
        WHERE [Площадка] IS NOT NULL
        GROUP BY [Площадка], [Род груза]
        ORDER BY vagon_count DESC
        """
        return self.execute_query(query)
    
    def get_annual_unloading_by_cargo_type(self):
        """
        4. Как менялся показатель ежегодной выгрузки вагонов в разрезе родов груза
        """
        query = """
        SELECT 
            YEAR([Дата и время погрузки]) as year,
            [Род груза],
            COUNT(*) as vagon_count,
            SUM([Вес нетто (т)]) as total_weight
        FROM [dbo].[VagonImport]
        WHERE [Дата и время погрузки] IS NOT NULL
        GROUP BY YEAR([Дата и время погрузки]), [Род груза]
        ORDER BY year, total_weight DESC
        """
        return self.execute_query(query)
    
    def get_annual_unloading_by_sender(self):
        """
        5. Как менялся показатель ежегодной выгрузки вагонов в разрезе грузоотправителей
        """
        query = """
        SELECT 
            YEAR([Дата и время погрузки]) as year,
            [Грузоотправитель],
            COUNT(*) as vagon_count,
            SUM([Вес нетто (т)]) as total_weight
        FROM [dbo].[VagonImport]
        WHERE [Дата и время погрузки] IS NOT NULL
            AND [Грузоотправитель] IS NOT NULL
        GROUP BY YEAR([Дата и время погрузки]), [Грузоотправитель]
        ORDER BY year, total_weight DESC
        """
        return self.execute_query(query)
    
    def get_last_month_port_shipments(self):
        """
        6. Предоставь данные по отгрузкам в адрес порта за предыдущий месяц
        Используем таблицу ShipmentsToThePort
        """
        query = """
        SELECT 
            [Дата],
            [Грузовладелец],
            [Грузоотправитель],
            [Груз],
            [Вес груза отправленный(т)] as weight,
            [Железная дорога],
            [Станция дислокации],
            [Род груза]
        FROM [dbo].[ShipmentsToThePort]
        WHERE [Дата] >= DATEADD(month, -1, GETDATE())
        ORDER BY [Дата] DESC
        """
        return self.execute_query(query)
    
    def get_yesterday_unloading_by_cargo(self):
        """
        7. Сколько выгрузили вчера вагонов в разрезе рода груза
        """
        query = """
        SELECT 
            [Род груза],
            COUNT(*) as vagon_count,
            SUM([Вес нетто (т)]) as total_weight
        FROM [dbo].[VagonImport]
        WHERE CAST([Дата и время погрузки] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)
        GROUP BY [Род груза]
        ORDER BY vagon_count DESC
        """
        return self.execute_query(query)
    
    def get_enterprise_wagons_status(self):
        """
        Дополнительный запрос: Статус вагонов на предприятии
        """
        query = """
        SELECT 
            [Статус вагона],
            COUNT(*) as vagon_count,
            [Род груза],
            AVG([Вес груза принятый (т)]) as avg_weight
        FROM [dbo].[EnterpriseWagons]
        WHERE [Дата] >= DATEADD(day, -7, GETDATE())
        GROUP BY [Статус вагона], [Род груза]
        ORDER BY vagon_count DESC
        """
        return self.execute_query(query)
    
    def get_storage_fullness(self):
        """
        Дополнительный запрос: Заполненность складов
        """
        query = """
        SELECT 
            [Площадка],
            [Род груза],
            [Грузовладелец],
            SUM([Вес (т)]) as current_weight,
            SUM([Вместимость (т)]) as capacity,
            (SUM([Вес (т)]) / NULLIF(SUM([Вместимость (т)]), 0)) * 100 as fullness_percent
        FROM [dbo].[StorageFullness]
        WHERE [Дата] >= DATEADD(day, -1, GETDATE())
        GROUP BY [Площадка], [Род груза], [Грузовладелец]
        ORDER BY fullness_percent DESC
        """
        return self.execute_query(query)
    
    def create_monthly_unloading_chart(self, data):
        """Создание графика изменения выгрузки вагонов по месяцам"""
        if data is None or data.empty:
            print("Нет данных для построения графика")
            return
        
        data['date'] = pd.to_datetime(data[['year', 'month']].assign(day=1))
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Количество вагонов', 'Общий вес (тонн)'),
            vertical_spacing=0.1
        )
        
        # График количества вагонов
        fig.add_trace(
            go.Scatter(x=data['date'], y=data['vagon_count'], 
                      mode='lines+markers', name='Количество вагонов',
                      line=dict(color='blue')),
            row=1, col=1
        )
        
        # График общего веса
        fig.add_trace(
            go.Scatter(x=data['date'], y=data['total_weight'], 
                      mode='lines+markers', name='Общий вес (тонн)',
                      line=dict(color='red')),
            row=2, col=1
        )
        
        fig.update_layout(
            title_text="Изменение выгрузки вагонов по месяцам",
            height=600,
            showlegend=False
        )
        
        fig.show()
    
    def create_cargo_type_chart(self, data):
        """Создание графика выгрузки по родам груза"""
        if data is None or data.empty:
            print("Нет данных для построения графика")
            return
        
        fig = px.bar(data, x='year', y='vagon_count', color='Род груза',
                     title='Ежегодная выгрузка вагонов по родам груза',
                     labels={'vagon_count': 'Количество вагонов', 'year': 'Год'},
                     height=600)
        
        fig.show()
    
    def create_sender_chart(self, data):
        """Создание графика выгрузки по грузоотправителям"""
        if data is None or data.empty:
            print("Нет данных для построения графика")
            return
        
        # Берем топ-10 грузоотправителей
        top_senders = data.groupby('Грузоотправитель')['total_weight'].sum().nlargest(10).index
        filtered_data = data[data['Грузоотправитель'].isin(top_senders)]
        
        fig = px.bar(filtered_data, x='year', y='total_weight', color='Грузоотправитель',
                     title='Ежегодная выгрузка вагонов по грузоотправителям (Топ-10)',
                     labels={'total_weight': 'Общий вес (тонн)', 'year': 'Год'},
                     height=600)
        
        fig.show()

# Пример использования - ПРИМЕРЫ ЗАПРОСОВ
if __name__ == "__main__":
    print("🚢 ПРИМЕРЫ ЗАПРОСОВ ДЛЯ ПОРТОВОГО ТЕРМИНАЛА")
    print("=" * 60)
    
    examples = [
        {
            "description": "1. Выгрузка вагонов по месяцам за последние 2 года",
            "query": """
            SELECT 
                YEAR([Дата и время погрузки]) as year,
                MONTH([Дата и время погрузки]) as month,
                COUNT(*) as vagon_count,
                SUM([Вес нетто (т)]) as total_weight
            FROM [dbo].[VagonImport]
            WHERE [Дата и время погрузки] >= DATEADD(year, -2, GETDATE())
            GROUP BY YEAR([Дата и время погрузки]), MONTH([Дата и время погрузки])
            ORDER BY year, month
            """
        },
        {
            "description": "2. Среднемесячная погрузка на суда за 2 года",
            "query": """
            SELECT 
                YEAR([Начальная дата подхода]) as year,
                MONTH([Начальная дата подхода]) as month,
                AVG([Вес нетто (т)]) as avg_monthly_loading,
                COUNT(*) as ship_count
            FROM [dbo].[ShipsImport]
            WHERE [Начальная дата подхода] >= DATEADD(year, -2, GETDATE())
            GROUP BY YEAR([Начальная дата подхода]), MONTH([Начальная дата подхода])
            ORDER BY year, month
            """
        },
        {
            "description": "3. Статистика по площадкам выгрузки",
            "query": """
            SELECT 
                [Площадка],
                [Род груза],
                COUNT(*) as vagon_count,
                AVG([Вес нетто (т)]) as avg_weight
            FROM [dbo].[VagonImport]
            WHERE [Площадка] IS NOT NULL
            GROUP BY [Площадка], [Род груза]
            ORDER BY vagon_count DESC
            """
        },
        {
            "description": "4. Выгрузка по родам груза по годам",
            "query": """
            SELECT 
                YEAR([Дата и время погрузки]) as year,
                [Род груза],
                COUNT(*) as vagon_count,
                SUM([Вес нетто (т)]) as total_weight
            FROM [dbo].[VagonImport]
            WHERE [Дата и время погрузки] IS NOT NULL
            GROUP BY YEAR([Дата и время погрузки]), [Род груза]
            ORDER BY year, total_weight DESC
            """
        },
        {
            "description": "5. Топ грузоотправителей по годам",
            "query": """
            SELECT 
                YEAR([Дата и время погрузки]) as year,
                [Грузоотправитель],
                COUNT(*) as vagon_count,
                SUM([Вес нетто (т)]) as total_weight
            FROM [dbo].[VagonImport]
            WHERE [Дата и время погрузки] IS NOT NULL
                AND [Грузоотправитель] IS NOT NULL
            GROUP BY YEAR([Дата и время погрузки]), [Грузоотправитель]
            ORDER BY year, total_weight DESC
            """
        },
        {
            "description": "6. Отгрузки в порт за прошлый месяц",
            "query": """
            SELECT 
                [Дата],
                [Грузовладелец],
                [Грузоотправитель],
                [Груз],
                [Вес груза отправленный(т)] as weight,
                [Железная дорога],
                [Станция дислокации],
                [Род груза]
            FROM [dbo].[ShipmentsToThePort]
            WHERE [Дата] >= DATEADD(month, -1, GETDATE())
            ORDER BY [Дата] DESC
            """
        },
        {
            "description": "7. Выгрузка вчера по родам груза",
            "query": """
            SELECT 
                [Род груза],
                COUNT(*) as vagon_count,
                SUM([Вес нетто (т)]) as total_weight
            FROM [dbo].[VagonImport]
            WHERE CAST([Дата и время погрузки] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)
            GROUP BY [Род груза]
            ORDER BY vagon_count DESC
            """
        },
        {
            "description": "8. Заполненность складов",
            "query": """
            SELECT 
                [Площадка],
                [Род груза],
                [Грузовладелец],
                SUM([Вес (т)]) as current_weight,
                SUM([Вместимость (т)]) as capacity,
                CASE 
                    WHEN SUM([Вместимость (т)]) > 0 THEN 
                        (SUM([Вес (т)]) / SUM([Вместимость (т)])) * 100 
                    ELSE 0 
                END as fullness_percent
            FROM [dbo].[StorageFullness]
            WHERE [Дата] >= DATEADD(day, -1, GETDATE())
            GROUP BY [Площадка], [Род груза], [Грузовладелец]
            ORDER BY fullness_percent DESC
            """
        }
    ]
    
    for example in examples:
        print(f"\n{example['description']}")
        print("-" * 50)
        print(example['query'].strip())
        print()
    
    print("\n💡 Для использования:")
    print("1. Запустите админку: ./run_admin.sh")
    print("2. Откройте http://localhost:8501")
    print("3. Введите запрос в текстовое поле или используйте примеры")
    print("4. Нажмите 'Генерировать SQL' для автоматического создания запроса")
    print("5. Нажмите 'Выполнить запрос' для получения результатов")
