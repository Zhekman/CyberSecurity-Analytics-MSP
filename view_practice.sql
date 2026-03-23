DROP VIEW IF EXISTS View_CustomerInvoices;

CREATE VIEW View_CustomerInvoices AS
SELECT 
    c.FirstName AS CustomerName,
    c.LastName AS CustomerLastname,
    COUNT(i.InvoiceId) AS InvoiceTotalCount,
    SUM(i.Total) AS TotalAmountSpent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.FirstName, c.LastName;

SELECT * FROM View_CustomerInvoices;