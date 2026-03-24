SELECT 
    d.OS_Version, 
    COUNT(se.EventID) AS Total_Critical_Events,
    SUM(CASE WHEN se.IsBlocked = 0 THEN 1 ELSE 0 END) AS Unblocked_Events,
    ROUND(
        SUM(CASE WHEN se.IsBlocked = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(se.EventID), 
        2
    ) AS Unblocked_Percentage
FROM devices d
JOIN security_events se ON d.DeviceID = se.DeviceID
WHERE se.EventSeverity IN ('High', 'Critical')
GROUP BY d.OS_Version
ORDER BY Unblocked_Percentage DESC;