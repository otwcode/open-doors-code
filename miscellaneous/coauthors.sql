select a.id, name, email, s.id, title, authorid, coauthorid
from sp04_authors a join sp04_stories s where (a.name like '%,%' or a.name like '% and %') and s.authorid=a.id;
