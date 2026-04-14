SELECT a.MMSI as ship1, b.MMSI as ship2, a.T, ST_Distance(a.Geom::geography, b.Geom::geography) 
AS dist
FROM AISInputFiltered a
JOIN AISInputFiltered b ON a.T = b.T
AND a.MMSI < b.MMSI
WHERE ST_DWithin(a.Geom::geography, b.Geom::geography, 5)
AND a.T BETWEEN '2024-11-20 10:00:00' AND '2024-11-20 10:30:00'
LIMIT 20;
