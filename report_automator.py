import pandas as pd
import os
import datetime
import sqlite3

# --- Шаг 1: Подготовка SQL-запроса ---
# Вся сложная логика по обработке данных вынесена в один SQL-запрос.
# Это позволяет выполнить все тяжелые вычисления (JOIN, GROUP BY) на стороне 
# быстрой и эффективной базы данных, а не в памяти с помощью Pandas.
sql_query = """
SELECT
    p.Category,
    SUM(s.Revenue) AS TotalRevenue,
    ad.AdSpend,
    -- Расчет ROAS: отношение общей выручки к затратам на рекламу.
    ROUND(SUM(s.Revenue) / ad.AdSpend, 2) AS ROAS
FROM
    -- Основа - таблица продаж.
    daily_sales AS s
    -- Используем LEFT JOIN, чтобы гарантировать, что мы не потеряем ни одной продажи,
    -- даже если для нее по ошибке не найдется информации о продукте или рекламе.
    LEFT JOIN
    product_info AS p 
	ON s.ProductID = p.ProductID
    LEFT JOIN
    ad_spend AS ad 
	ON p.Category = ad.Category
GROUP BY
    -- Группируем по категории и затратам, чтобы подготовить данные для агрегации.
    p.Category,
    ad.AdSpend
ORDER BY
    -- Сортируем по убыванию ROAS, чтобы самые эффективные категории были сверху.
    ROAS DESC;
"""

# --- Шаг 2: Выполнение запроса и получение данных ---
# Основной блок: подключаемся к БД, выполняем наш SQL и забираем результат в DataFrame.
# Оборачиваем в try...except на случай вохникновения ошибок: отсутствия файла БД,
# синтаксических ошибок в SQL или отсутствия таблиц.
print("[1/3] Подключение к базе данных и выполнение SQL-запроса...")

DB_FILE = 'analytics.db'

try:
    conn = sqlite3.connect(DB_FILE) 
    final_df = pd.read_sql_query(sql_query, conn)
    conn.close()
    print("      > Расчеты успешно выполнены на стороне базы данных.")

except Exception as e:
    print(f"ОШИБКА: Не удалось выполнить SQL-запрос. {e}")
    exit()

# --- Шаг 3: Сохранение результата в Excel ---
# Финальный этап: сохраняем полученный DataFrame в Excel-файл 
# с динамическим именем, включающим текущую дату.
print("[2/3] Сохранение финального отчета...")
if not os.path.exists('output'):
    os.makedirs('output')

today_str = datetime.date.today().strftime('%Y-%m-%d')
output_filename = f'daily_marketing_summary_{today_str}.xlsx'
output_path = os.path.join('output', output_filename)

# index=False удаляет из финального Excel-файла служебный индекс
# строк Pandas, делая отчет чистым и готовым для пользователя.
final_df.to_excel(output_path, index=False)
print("[3/3] --- УСПЕХ! ---")
print(f"Финальный отчет сохранен: {output_filename}")

# Выводим результат на экран для быстрой проверки.
print("\n--- Итоговый отчет ---")
print(final_df.to_string())
