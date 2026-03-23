-- 1. MFA Adoption Rate (Відсоток ввімкненого MFA за сервісами)
-- Це показує, які сервіси найбільш вразливі
SELECT 
    Service,
    COUNT(*) as Total_Users,
    SUM(CASE WHEN MFA_Enabled = 1 THEN 1 ELSE 0 END) as MFA_Active,
    ROUND(CAST(SUM(CASE WHEN MFA_Enabled = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as Adoption_Percentage
FROM mfa_status
GROUP BY Service;

-- 2. Patch Compliance (Кількість застарілих пристроїв за відділами)
-- Пристрої, що не оновлювалися понад 30 днів
SELECT 
    e.Department,
    COUNT(d.DeviceID) as Outdated_Devices
FROM devices d
JOIN employees e ON d.EmployeeID = e.EmployeeID
WHERE d.LastPatchDate < date('now', '-30 days')
GROUP BY e.Department
ORDER BY Outdated_Devices DESC;

-- 3. Top Risk Departments (Відділи з найбільшою кількістю фішингових кліків)
SELECT 
    e.Department,
    COUNT(se.EventID) as Phishing_Clicks
FROM security_events se
JOIN devices d ON se.DeviceID = d.DeviceID
JOIN employees e ON d.EmployeeID = e.EmployeeID
WHERE se.EventType = 'Phishing Link Clicked'
GROUP BY e.Department
ORDER BY Phishing_Clicks DESC;

-- 4. Effectiveness of Security Systems (Скільки атак було заблоковано)
SELECT 
    EventType,
    COUNT(*) as Total_Attempts,
    SUM(IsBlocked) as Blocked_By_System,
    ROUND(CAST(SUM(IsBlocked) AS FLOAT) / COUNT(*) * 100, 2) as Prevention_Rate
FROM security_events
GROUP BY EventType;

-- 5. Training Status vs Security Incidents
-- Чи менше інцидентів у тих, хто пройшов навчання?
SELECT 
    t.Status as Training_Status,
    COUNT(DISTINCT e.EmployeeID) as Employee_Count,
    COUNT(se.EventID) as Total_Incidents,
    ROUND(CAST(COUNT(se.EventID) AS FLOAT) / COUNT(DISTINCT e.EmployeeID), 2) as Incidents_Per_Employee
FROM employees e
JOIN training_logs t ON e.EmployeeID = t.EmployeeID
LEFT JOIN devices d ON e.EmployeeID = d.EmployeeID
LEFT JOIN security_events se ON d.DeviceID = se.DeviceID
GROUP BY t.Status;
