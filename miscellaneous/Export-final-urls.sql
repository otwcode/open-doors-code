SELECT s.id as "StoryID", s.title, a.name, s.ao3url, concat("$$TEMP SITE BASE URL$$", cast(c.id as char)) as "TempURL", s.donotimport
FROM od_sgf.$$PREFIX$$_stories s join od_sgf.$$PREFIX$$_chapters c on c.storyid=s.id join od_sgf.$$PREFIX$$_authors a on s.authorid=a.id
 where c.position=0 or c.position=1;

