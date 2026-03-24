import sqlite3

def analyze_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"Таблиця: {table_name}")
            
            # Get column info for each table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                # col[1] is name, col[2] is type
                print(f"  - Стовпець: {col[1]} ({col[2]})")
            print("-" * 20)

        conn.close()
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == '__main__':
    analyze_db('CyberSecurity.db')
