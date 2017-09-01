SELECT a.id, a.name, a.email, COUNT(s.ID) as "stories" FROM
`$PREFIX$_authors` a LEFT OUTER JOIN $PREFIX$_stories s
ON a.id = s.authorid
GROUP BY a.id;