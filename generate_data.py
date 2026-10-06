import pandas as pd
import os
import sqlite3

# Этот скрипт выполняет две задачи:
# 1. Основная: Создает и наполняет базу данных 'analytics.db',
# чтобы основному скрипту было с чем работать.
# 2. Дополнительная: Сохраняет исходные данные в CSV для удобной проверки.

# --- Шаг 1: Данные о продажах ---
# Создаем таблицу с несколькими продажами за один день.
sales_data = {
    'Date': ['2026-10-06', '2026-10-06', '2026-10-06', '2026-10-06', '2026-10-06'],
    'ProductID': [101, 102, 201, 101, 201],
    'UnitsSold': [5, 3, 10, 2, 5],
    'Revenue': [500.0, 150.0, 200.0, 200.0, 100.0]
}
sales_df = pd.DataFrame(sales_data)

# --- Шаг 2: Данные о товарах ---
# Таблица, где каждому ProductID соответствует название и категория.
product_data = {
    'ProductID': [101, 102, 201, 301],
    'ProductName': ['Умные часы Pro', 'Кожаный кошелек', 'Фитнес-бутылка', 'Беспроводные наушники'],
    'Category': ['Электроника', 'Аксессуары', 'Спорт и отдых', 'Электроника']
}
product_df = pd.DataFrame(product_data)

# --- Шаг 3: Данные о расходах на рекламу ---
# Таблица с затратами на рекламу для каждой категории.
ad_data = {
    'Date': ['2026-10-06', '2026-10-06', '2026-10-06'],
    'Category': ['Электроника', 'Аксессуары', 'Спорт и отдых'],
    'AdSpend': [150.0, 25.0, 10.0]
}
ad_df = pd.DataFrame(ad_data)

# --- Шаг 4: Создание и наполнение базы данных ---
DB_FILE = 'analytics.db'

print(f"--- Создание и наполнение базы данных '{DB_FILE}' ---")
try:
    conn = sqlite3.connect(DB_FILE)
    
    sales_df.to_sql('daily_sales', conn, if_exists='replace', index=False)
    product_df.to_sql('product_info', conn, if_exists='replace', index=False)
    ad_df.to_sql('ad_spend', conn, if_exists='replace', index=False)
    
    conn.close()
    
    print(f"> База данных '{DB_FILE}' успешно создана и наполнена.")
    
except Exception as e:
    print(f"ОШИБКА: Не удалось создать базу данных. {e}")

# --- Шаг 3: Сохранение CSV-файлов ---
print("\n--- Сохранение исходных данных в CSV ---")
if not os.path.exists('data'):
    os.makedirs('data')

sales_df.to_csv('data/daily_sales.csv', index=False)
product_df.to_csv('data/product_info.csv', index=False)
ad_df.to_csv('data/ad_spend.csv', index=False)

print("> Файлы .csv успешно сохранены в папку 'data'.")
