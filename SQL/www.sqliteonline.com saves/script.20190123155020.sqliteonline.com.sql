-- 6. excercise:
SELECT DISTINCT c.lastname, billingcity, i.billingcountry, i.invoicedate
FROM invoices AS i 
JOIN customers AS c
ON c.customerid = i.customerid
ORDER By billingcountry DESC