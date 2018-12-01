SELECT group_concat(a.id) FROM
  `authors` a
  LEFT OUTER JOIN stories s
    ON a.id = s.authorid
  LEFT OUTER JOIN bookmarks b
    ON a.id = b.authorid
where s.id is null and b.id is null;
