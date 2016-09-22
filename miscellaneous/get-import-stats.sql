select "stories" as name,
(select count(*) from KEY_stories where imported=1 LIMIT 0, 50000) as imported,
(select count(*) from KEY_stories where donotimport=1 LIMIT 0, 50000) as donotimport,
(select count(*) from KEY_stories where imported=0 and donotimport=0 LIMIT 0, 50000) as notimported
UNION ALL
select "bookmarks" as name,
(select count(*) from KEY_bookmarks where imported=1 LIMIT 0, 50000) as imported,
(select count(*) from KEY_bookmarks where donotimport=1 LIMIT 0, 50000) as donotimport,
(select count(*) from KEY_bookmarks where imported=0 and donotimport=0 LIMIT 0, 50000) as notimported;
