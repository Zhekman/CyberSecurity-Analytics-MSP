import sqlite3
import pandas as pd
import os

# Налаштування
db_name = 'CyberSecurity.db'
csv_files = {
    'employees': 'employees.csv',
    'devices': 'devices.csv',
    'security_events': 'security_events.csv',
    'mfa_status': 'mfa_status.csv',
    'training_logs': 'training_logs.csv'
}

print(f"Починаю створення бази даних {db_name}...")

# Підключення до SQLite (якщо файлу немає, він створиться)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Завантаження кожного CSV у відповідну таблицю
for table_name, csv_file in csv_files.items():
    if os.path.exists(csv_file):
        print(f"Завантажую {csv_file} у таблицю '{table_name}'...")
        df = pd.read_csv(csv_file)
        # if_exists='replace' означає, що таблиця перествориться, якщо вона вже була
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    else:
        print(f"Помилка: Файл {csv_file} не знайдено!")

# Створення індексів для швидкості (як у справжнього SQL-профі)
print("Створюю індекси для оптимізації запитів...")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_device ON security_events(DeviceID);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_device_employee ON devices(EmployeeID);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_mfa_employee ON mfa_status(EmployeeID);")

conn.commit()
conn.close()

print(f"\nГотово! База даних '{db_name}' успішно створена та готова до роботи.")
print("Тепер ви можете відкрити її в будь-якому SQLite переглядачі або робити запити через Python/Power BI.")
