SELECT group_concat(a.id) FROM
  `authors` a
  LEFT OUTER JOIN stories s
    ON a.id = s.author_id
  LEFT OUTER JOIN bookmarks b
    ON a.id = b.author_id
where s.id is null and b.id is null;
