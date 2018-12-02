-- Duplicate author and give it a new number as many times as 
-- will split the number of works

SET @ORIGINAL = 147;
SET @NEW1 = 20147;

USE od_sgf;
INSERT INTO nl_authors SELECT @NEW1, name, email, imported, donotimport from nl_authors where id = @ORIGINAL;

UPDATE  nl_stories
SET     authorid = @NEW1
WHERE   authorid = @ORIGINAL
ORDER BY id
LIMIT 75;
SELECT authorid, count(*) FROM nl_stories WHERE authorid=@NEW1;

SELECT authorid, count(*) FROM nl_stories WHERE authorid=@ORIGINAL;
