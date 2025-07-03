import os
import pyodbc
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def get_database_schema(database_name):
    """Получение схемы базы данных"""
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    connection_string = f"DRIVER={{{driver}}};SERVER={host},{port};DATABASE={database_name};UID={user};PWD={password};"
    
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        schema_info = []
        
        # Получаем информацию о таблицах
        cursor.execute("""
            SELECT 
                TABLE_SCHEMA,
                TABLE_NAME,
                TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tables = cursor.fetchall()
        
        for table in tables:
            schema_name = table[0]
            table_name = table[1]
            
            schema_info.append(f"\n-- Таблица: {schema_name}.{table_name}")
            schema_info.append(f"-- ========================================")
            
            # Получаем структуру таблицы
            cursor.execute(f"""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    CHARACTER_MAXIMUM_LENGTH,
                    IS_NULLABLE,
                    COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            
            columns = cursor.fetchall()
            
            create_table_sql = f"CREATE TABLE [{schema_name}].[{table_name}] (\n"
            column_definitions = []
            
            for column in columns:
                col_name = column[0]
                data_type = column[1]
                max_length = column[2]
                is_nullable = column[3]
                default_value = column[4]
                
                # Формируем определение колонки
                col_def = f"    [{col_name}] {data_type}"
                
                if max_length and data_type in ['varchar', 'nvarchar', 'char', 'nchar']:
                    col_def += f"({max_length})"
                elif data_type in ['decimal', 'numeric']:
                    # Получаем точность и масштаб для числовых типов
                    cursor.execute(f"""
                        SELECT NUMERIC_PRECISION, NUMERIC_SCALE
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = '{schema_name}' 
                        AND TABLE_NAME = '{table_name}' 
                        AND COLUMN_NAME = '{col_name}'
                    """)
                    precision_scale = cursor.fetchone()
                    if precision_scale and precision_scale[0]:
                        col_def += f"({precision_scale[0]},{precision_scale[1] or 0})"
                
                if is_nullable == 'NO':
                    col_def += " NOT NULL"
                
                if default_value:
                    col_def += f" DEFAULT {default_value}"
                
                column_definitions.append(col_def)
            
            create_table_sql += ",\n".join(column_definitions)
            create_table_sql += "\n);\n"
            
            schema_info.append(create_table_sql)
            
            # Получаем информацию о первичных ключах
            cursor.execute(f"""
                SELECT 
                    kcu.COLUMN_NAME
                FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
                    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                WHERE tc.TABLE_SCHEMA = '{schema_name}'
                    AND tc.TABLE_NAME = '{table_name}'
                    AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
                ORDER BY kcu.ORDINAL_POSITION
            """)
            
            pk_columns = cursor.fetchall()
            if pk_columns:
                pk_cols = [col[0] for col in pk_columns]
                schema_info.append(f"ALTER TABLE [{schema_name}].[{table_name}] ADD CONSTRAINT PK_{table_name} PRIMARY KEY ({', '.join([f'[{col}]' for col in pk_cols])});\n")
            
            # Получаем информацию о внешних ключах
            cursor.execute(f"""
                SELECT 
                    fk.name AS FK_NAME,
                    tp.name AS parent_table,
                    cp.name AS parent_column,
                    tr.name AS referenced_table,
                    cr.name AS referenced_column
                FROM sys.foreign_keys fk
                INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
                INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
                INNER JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
                INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
                INNER JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
                WHERE tp.name = '{table_name}'
            """)
            
            fk_constraints = cursor.fetchall()
            for fk in fk_constraints:
                fk_name = fk[0]
                parent_table = fk[1]
                parent_column = fk[2]
                referenced_table = fk[3]
                referenced_column = fk[4]
                
                schema_info.append(f"ALTER TABLE [{schema_name}].[{parent_table}] ADD CONSTRAINT [{fk_name}] FOREIGN KEY ([{parent_column}]) REFERENCES [{schema_name}].[{referenced_table}] ([{referenced_column}]);\n")
        
        connection.close()
        return "\n".join(schema_info)
        
    except Exception as e:
        return f"-- Ошибка при получении схемы базы данных {database_name}: {e}\n"

def main():
    """Главная функция для извлечения схем всех баз данных"""
    databases = ['GRNG', 'GRMU', 'OperativeReport']
    
    all_schemas = []
    all_schemas.append("-- =====================================")
    all_schemas.append("-- СХЕМЫ БАЗ ДАННЫХ")
    all_schemas.append("-- =====================================")
    all_schemas.append(f"-- Сервер: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
    all_schemas.append(f"-- Пользователь: {os.getenv('DB_USER')}")
    all_schemas.append("-- =====================================\n")
    
    for db_name in databases:
        print(f"Извлекаем схему базы данных: {db_name}")
        all_schemas.append(f"\n-- =====================================")
        all_schemas.append(f"-- БАЗА ДАННЫХ: {db_name}")
        all_schemas.append(f"-- =====================================")
        
        schema = get_database_schema(db_name)
        all_schemas.append(schema)
    
    # Записываем схему в файл
    with open('/workspaces/aeroclub_repo/vagon/db_shema.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(all_schemas))
    
    print("Схема базы данных сохранена в файл db_shema.sql")

if __name__ == "__main__":
    main()
