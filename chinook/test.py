import sqlite3

# Підключаємося до файлу бази даних
# Переконайтеся, що файл Chinook_Sqlite.sqlite лежить у тій самій папці, що і цей скрипт
connection = sqlite3.connect('Chinook_Sqlite.sqlite')
cursor = connection.cursor()

# Пишемо SQL-запит (той самий, що ми тренували в DBeaver)
query = "SELECT Name FROM Artist LIMIT 10;"

# Виконуємо запит
cursor.execute(query)

# Отримуємо результати
results = cursor.fetchall()

print("--- Список перших 10 артистів ---")
for row in results:
    print(f"Виконавець: {row[0]}")

# Закриваємо з'єднання
connection.close()