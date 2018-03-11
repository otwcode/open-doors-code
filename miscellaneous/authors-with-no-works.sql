SELECT group_concat(a.id) FROM
  `$PREFIX$_authors` a
  LEFT OUTER JOIN $PREFIX$_stories s
    ON a.id = s.authorid
  LEFT OUTER JOIN $PREFIX$_bookmarks b
    ON a.id = b.authorid
where s.id is null and b.id is null;
