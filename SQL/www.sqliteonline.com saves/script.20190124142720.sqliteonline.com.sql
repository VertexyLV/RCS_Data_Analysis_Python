-- 8. Provide a query that shows the Invoice Total, Customer name, Country and Sale Agent name for all invoices and customers.
SELECT i.invoicedate, i.total, c.firstname, c.lastname, e.lastname AS SalesAgent
FROM invoices AS i
JOIN customers AS c
ON c.customerid = i.customerid
JOIN employees AS e
ON e.employeeid = c.supportrepid
ORDER BY c.lastname ASC