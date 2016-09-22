USE DATABASE;

-- REMOVE "mailto:" in author emails
update fanfiction_authors set email=replace(email, "mailto:", "") where email like "mailto:%";


-- RATINGS
SET sql_safe_updates = 0;
update fanfiction_stories set rating="General Audiences" where rating = '5' or rating='4';
update fanfiction_stories set rating="Teen And Up Audiences" where rating = '3';
update fanfiction_stories set rating="Mature" where rating = '2';
update fanfiction_stories set rating="Explicit" where rating = '1';

-- Add COMMAS so first and last item start and end with commas too
UPDATE `fanfiction_stories` set `categories` = concat(', ', categories, ',');
UPDATE `fanfiction_stories` set `tags` = concat(', ', tags, ',');
UPDATE `fanfiction_stories` set `warnings` = concat(', ', warnings, ',');
UPDATE `fanfiction_stories` set `characters` = concat(', ', characters, ',');
UPDATE `fanfiction_stories` set `relationships` = concat(', ', relationships, ',');

-- 

-- RENAME CATEGORIES ETC
-- generate from Tag Wrangling Google spreadsheet
-- eg: 
-- Move relationships from tags field
-- UPDATE `fanfiction_stories` set Relationships = concat(Relationships, ', CHARACTER A/CHARACTER B'), tags = replace(tags, ', A/B', '') where tags like '%, A/B%';
-- 








-- CLEAN COMMAS
UPDATE `fanfiction_stories` SET `tags` =        TRIM(BOTH ',' FROM tags);
UPDATE `fanfiction_stories` SET `categories` =  TRIM(BOTH ',' FROM categories);
UPDATE `fanfiction_stories` SET `warnings` =    TRIM(BOTH ',' FROM warnings);
UPDATE `fanfiction_stories` SET `fandoms` =     TRIM(BOTH ',' FROM fandoms);
UPDATE `fanfiction_stories` SET `relationships`=TRIM(BOTH ',' FROM relationships);

UPDATE `fanfiction_stories` SET `tags` =        TRIM(BOTH ' ' FROM tags);
UPDATE `fanfiction_stories` SET `categories` =  TRIM(BOTH ' ' FROM categories);
UPDATE `fanfiction_stories` SET `warnings` =    TRIM(BOTH ' ' FROM warnings);
UPDATE `fanfiction_stories` SET `fandoms` =     TRIM(BOTH ' ' FROM fandoms);
UPDATE `fanfiction_stories` SET `relationships`=TRIM(BOTH ' ' FROM relationships);

UPDATE `fanfiction_stories` SET `tags` = 		REPLACE(tags, ',,', ',');
UPDATE `fanfiction_stories` SET `categories` =  REPLACE(categories, ',,', ',');
UPDATE `fanfiction_stories` SET `warnings` =    REPLACE(warnings, ',,', ',');
UPDATE `fanfiction_stories` SET `fandoms` =     REPLACE(fandoms, ',,', ',');
UPDATE `fanfiction_stories` SET `relationships`=REPLACE(relationships, ',,', ',');

-- drop unwanted columns after shuffling things around!
ALTER TABLE `fanfiction_stories` 
DROP COLUMN `count`,
DROP COLUMN `reviews`,
DROP COLUMN `rating`,
DROP COLUMN `wordcount`,
DROP COLUMN `rr`,
DROP COLUMN `completed`,
DROP COLUMN `validated`,
DROP COLUMN `featured`,
DROP COLUMN `catid`,
DROP COLUMN `coauthors`,
DROP COLUMN `challenges`;