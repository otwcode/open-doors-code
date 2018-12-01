select "stories" as name,
(select count(*) from stories where imported=1) as "Imported",
(select count(*) from stories where donotimport=1) as "Do not import",
(select count(*) from stories where imported=0 and donotimport=0) as "To be imported"
UNION ALL
select "bookmarks" as name,
(select count(*) from bookmarks where imported=1) as "Imported",
(select count(*) from bookmarks where donotimport=1 or brokenlink=1) as "Do not import",
(select count(*) from bookmarks where imported=0 and donotimport=0 and brokenlink=0) as "To be imported";
