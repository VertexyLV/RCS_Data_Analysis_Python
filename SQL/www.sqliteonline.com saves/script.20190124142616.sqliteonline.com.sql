-- 8. Provide a query that shows the Invoice Total, Customer name, Country and Sale Agent name for all invoices and customers.
SELECT i.invoicedate, i.total, c.firstname, c.lastname, ii.trackid, ii.unitprice, ii.quantity, e.lastname AS SalesAgent
FROM invoices AS i
Join invoice_items AS ii
ON i.invoiceid = ii.invoiceid
JOIN customers AS c
ON c.customerid = i.customerid
JOIN employees AS e
ON e.employeeid = c.supportrepid
