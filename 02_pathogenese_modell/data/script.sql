SELECT version();

SELECT
  name,
  SUM(pgsize) AS bytes,
  ROUND(SUM(pgsize) / 1024.0, 1) AS kb,
  COUNT(*) AS pages
FROM dbstat
GROUP BY name
ORDER BY bytes DESC;

--sqlite
SELECT * FROM "dbstat" ;

SELECT name ,SUM(pgsize)/1024 table_size  FROM "dbstat" GROUP BY name ORDER BY table_size desc;

SELECT
      name,
      (page_count * page_size) as size_bytes
  FROM (
      SELECT
          name,
          (SELECT page_count FROM pragma_page_count) as page_count,
          (SELECT page_size FROM pragma_page_size) as page_size
      FROM sqlite_master
      WHERE type='table'
  )
  ORDER BY size_bytes DESC;

SELECT
      name,
      printf('%.2f MB', (page_count * page_size) / 1024.0 / 1024.0) as size_mb,
      (page_count * page_size) as size_bytes
  FROM (
      SELECT
          name,
          (SELECT page_count FROM pragma_page_count) as page_count,
          (SELECT page_size FROM pragma_page_size) as page_size
      FROM sqlite_master
      WHERE type='table'
  )
  ORDER BY size_bytes DESC;
 
 VACUUM;

SELECT 
  (date_trunc('day', timestamp_ms_at + INTERVAL '12 hours'))::date as shifted_day,
  COUNT(*) as minutes_per_day
FROM "HRV_MINUTE_AGGREGATED" 
WHERE 
  timestamp_ms_at >= NOW() - INTERVAL '3 months'
  AND "B7B8_OFF" < 0.2
  AND "RMSSD_MS" < 45
GROUP BY date_trunc('day', timestamp_ms_at + INTERVAL '12 hours')
ORDER BY shifted_day;




