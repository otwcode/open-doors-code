USE DATABASE;

-- 1. Check the tables actually present in the database - AO3 has warnings, categories (eg: M/M), relationships, characters, 
-- fandoms and freeform additional tags
-- 2. Run and copy-paste into a Google spreadsheet for Open Doors to share with the Tag Wrangling team
SELECT DISTINCT class_id as "Original Tag Id", class_name as "Original Tag Name", "classes" as "Original Tag Type", 
'' as "Recommended AO3 Tag", '' as "Recommended AO3 Category\n(for relationships)", '' as "Original Description",
'' as "TW Notes" FROM fanfiction_classes 
UNION ALL
SELECT DISTINCT catid as "Original Tag Id", category as "Original Tag Name", "categories" as "Original Tag Type",
'' as "Recommended AO3 Tag", '' as "Recommended AO3 Category\n(for relationships)", description as "Original Description",
'' as "TW Notes" FROM fanfiction_categories
UNION ALL
SELECT DISTINCT charid as "Original Tag Id", charname as "Original Tag Name", "characters" as "Original Tag Type",
'' as "Recommended AO3 Tag", '' as "Recommended AO3 Category\n(for relationships)", '' as "Orignal Description",
'' as "TW Notes" FROM fanfiction_characters
UNION ALL
SELECT DISTINCT rid as "Original Tag Id", rating as "Original Tag Name", "ratings" as "Original Tag Type",
'' as "Recommended AO3 Tag", '' as "Recommended AO3 Category\n(for relationships)", warningtext as "Orignal Description",
'' as "TW Notes" FROM fanfiction_ratings
;