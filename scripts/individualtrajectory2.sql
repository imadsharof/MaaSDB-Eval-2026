SELECT ST_Length(ST_MakeLine(Geom ORDER BY T) :: geography) AS total_distance_meters
FROM AISInputFiltered
WHERE MMSI = 219005887
AND T BETWEEN '2024-11-20 10:00:00' AND '2024-11-20 10:30:00';
