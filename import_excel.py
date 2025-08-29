import pandas as pd
from sqlalchemy import create_engine
import os

DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_financial_analysis',
    'user': 'postgres',
    'password': '123',
    'port': '5432'
}

EXCEL_FILE = r'C:\sql_projects\financial_analysis_test\asignments.xlsx'

def main():
    try:
        print("Загрузка данных из Excel...")
        df_portfolio1 = pd.read_excel(EXCEL_FILE, sheet_name=1)
        df_portfolio2 = pd.read_excel(EXCEL_FILE, sheet_name=2)
        
        print("Подключение к базе данных...")
        engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        
        print("Импорт данных в PostgreSQL...")
        df_portfolio1.to_sql('portfolio_1', engine, if_exists='replace', index=False)
        df_portfolio2.to_sql('portfolio_2', engine, if_exists='replace', index=False)
        
        print("Все операции завершены успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()