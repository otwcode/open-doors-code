SELECT a.id, a.name, a.email, COUNT(s.ID) as "stories" FROM
`authors` a LEFT OUTER JOIN stories s
ON a.id = s.authorid
GROUP BY a.id;
