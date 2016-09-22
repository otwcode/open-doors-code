use DATABASE;
SELECT a.uid as "Author id", a.penname as "Author", a.email as "Email", s.sid as "Story id", s.title as "Title", s.summary as "Summary"
FROM fanfiction_authors as a 
join fanfiction_stories as s on s.uid = a.uid;