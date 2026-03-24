SELECT 
    e.Location, 
    e.IsRemote, 
    COUNT(se.EventID) AS Total_Events,
    SUM(CASE WHEN se.EventSeverity IN ('High', 'Critical') THEN 1 ELSE 0 END) AS Critical_Events,
    ROUND(
        COUNT(se.EventID) * 1.0 / COUNT(DISTINCT d.DeviceID), 
        2
    ) AS Avg_Events_Per_Device
FROM employees e
JOIN devices d ON e.EmployeeID = d.EmployeeID
JOIN security_events se ON d.DeviceID = se.DeviceID
GROUP BY e.Location, e.IsRemote
ORDER BY Avg_Events_Per_Device DESC;