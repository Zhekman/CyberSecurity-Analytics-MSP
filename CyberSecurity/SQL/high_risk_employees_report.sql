SELECT 
    em.Department, 
    count (em.EmployeeID) as At_Risk_Employees_Count
 from employees em 
 JOIN mfa_status mf on em.EmployeeID = mf.EmployeeID 
 JOIN training_logs tr on em.EmployeeID = tr.EmployeeID
 where tr.Status = 'Overdue' 
 and mf.MFA_Enabled = '0'
 AND mf.Service = 'Email'
 GROUP by em.Department
 order by At_Risk_Employees_Count DESC;
 
