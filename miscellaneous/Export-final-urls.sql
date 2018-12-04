SELECT s.id as "StoryID",
	s.title as "Title",
	a.name as "Author 1",
	s.ao3url as "AO3 URL",
	replace(replace(replace(s.ao3url, "://archiveofourown.org/works/", ""), "https", "http"), "http", "") as "AO3 id",
	concat("$$TEMP SITE BASE URL$$", cast(c.id as char)) as "URL Imported From",
	"" as "Original URL"
FROM od_sgf.stories s
	join od_sgf.chapters c on c.story_id=s.id
	join od_sgf.authors a on s.author_id=a.id
where c.position=0 or c.position=1;
