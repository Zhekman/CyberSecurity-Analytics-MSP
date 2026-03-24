-- 1. Представлення для головного дашборду (Security Overview)
-- Тут ми поєднуємо події, пристрої та працівників в одну таблицю для Power BI.
DROP VIEW IF EXISTS v_security_dashboard;
CREATE VIEW v_security_dashboard AS
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
JOIN employees e ON d.EmployeeID = e.EmployeeID;

-- 2. Представлення для аналізу MFA (Compliance)
DROP VIEW IF EXISTS v_mfa_analysis;
CREATE VIEW v_mfa_analysis AS
SELECT 
    m.Service,
    m.MFA_Enabled,
    e.Department,
    e.Location,
    e.FullName as EmployeeName
FROM mfa_status m
JOIN employees e ON m.EmployeeID = e.EmployeeID;

-- 3. Представлення для аналізу навчання (Training Status)
DROP VIEW IF EXISTS v_training_status;
CREATE VIEW v_training_status AS
SELECT 
    t.CourseName,
    t.Status as TrainingStatus,
    t.CompletionDate,
    e.Department,
    e.FullName as EmployeeName
FROM training_logs t
JOIN employees e ON t.EmployeeID = e.EmployeeID;
