WITH My10Ships AS (
    SELECT MMSI, T, Geom
    FROM AISInputFiltered
    
    WHERE MMSI IN (
        232047253, 219005887, 2190071, 2190068, 219015127,
        219015579, 111219515, 219026147, 219006284, 219007401
    )
    AND T BETWEEN '2024-11-20 10:00:00' AND '2024-11-20 10:30:00'
)
SELECT a.MMSI as ship1, b.MMSI as ship2, a.T, 
       ST_Distance(a.Geom::geography, b.Geom::geography) AS dist
FROM My10Ships a
JOIN My10Ships b ON a.T = b.T AND a.MMSI < b.MMSI
WHERE ST_DWithin(a.Geom::geography, b.Geom::geography, 50) 
ORDER BY dist ASC;
