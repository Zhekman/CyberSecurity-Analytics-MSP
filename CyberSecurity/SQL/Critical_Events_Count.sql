SELECT 
    d.deviceID,
    d.DeviceType, 
    d.OS_Version,
    count (se.EventID) AS Critical_Events_Count
    FROM devices d
JOIN security_events se on d.DeviceID = se.DeviceID
WHERE d.AntivirusStatus != 'Active' 
AND se.EventSeverity in  ('High', 'Critical')
GROUP by d.DeviceID, d.DeviceType, d.OS_Version
ORDER by Critical_Events_Count DESC
limit 10;
 