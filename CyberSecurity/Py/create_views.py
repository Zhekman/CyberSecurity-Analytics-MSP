import sqlite3

def create_views():
    conn = sqlite3.connect('CyberSecurity.db')
    cursor = conn.cursor()

    print("Створюю SQL Views для Power BI...")

    # 1. View для загального огляду безпеки (Security Overview)
    # Поєднуємо події, пристрої та відділи в одну зручну таблицю
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_security_dashboard AS
    SELECT 
        se.EventID,
        se.EventType,
        se.EventSeverity,
        se.EventTimestamp,
        se.IsBlocked,
        d.DeviceType,
        d.OS_Version,
        e.Department,
        e.Location,
        e.IsRemote
    FROM security_events se
    JOIN devices d ON se.DeviceID = d.DeviceID
    JOIN employees e ON d.EmployeeID = e.EmployeeID
    """)

    # 2. View для аналізу MFA (MFA Compliance)
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_mfa_analysis AS
    SELECT 
        m.Service,
        m.MFA_Enabled,
        e.Department,
        e.Location,
        e.FullName as EmployeeName
    FROM mfa_status m
    JOIN employees e ON m.EmployeeID = e.EmployeeID
    """)

    # 3. View для аналізу навчання (Training Impact)
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_training_status AS
    SELECT 
        t.CourseName,
        t.Status as TrainingStatus,
        t.CompletionDate,
        e.Department,
        e.FullName as EmployeeName
    FROM training_logs t
    JOIN employees e ON t.EmployeeID = e.EmployeeID
    """)

    conn.commit()
    conn.close()
    print("Успішно! Views додані в CyberSecurity.db.")

if __name__ == "__main__":
    create_views()
