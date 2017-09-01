-- Duplicate author and give it a new number as many times as 
-- will split the number of works

SET @ORIGINAL = 1;
SET @NEW1 = 50001;

USE od_sgf;
UPDATE  tqp_stories
SET     authorid = @NEW1
WHERE   authorid = @ORIGINAL
ORDER BY id
LIMIT 150;
SELECT authorid, count(*) FROM tqp_stories WHERE authorid=@NEW1;

SELECT authorid, count(*) FROM tqp_stories WHERE authorid=@ORIGINAL;