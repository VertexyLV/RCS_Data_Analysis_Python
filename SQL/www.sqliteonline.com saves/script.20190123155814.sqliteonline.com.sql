-- 6. excercise:
SELECT c.lastname, i.customerid, SUM(i.total) as SUM, AVG(i.total) as AVG, COUNT(i.total) AS COUNT 
FROM invoices AS i
Join customers AS c
ON c.customerid = i.customerid
GROUP BY c.customerid
ORDER BY SUM(total) DESC