import sqlite3

def analyze():
    conn = sqlite3.connect('Chinook_Sqlite.sqlite')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("### Chinook Database Structure ###\n")
    for table_name in [t[0] for t in tables]:
        print(f"--- Table: {table_name} ---")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]}){' [PK]' if col[5] else ''}")
        print()
    
    conn.close()

if __name__ == '__main__':
    analyze()
