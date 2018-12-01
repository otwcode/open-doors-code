set sql_safe_updates=0;
use $DATABASE$;
UPDATE stories set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE bookmarks set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE authors set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE stories set Ao3Url=null, importNotes='' where Ao3Url is not null or importNotes is not null;
UPDATE bookmarks set Ao3Url=null, importNotes='' where Ao3Url is not null or importNotes is not null;

UPDATE archiveconfig
	set imported=0,
    NotImported = (select count(*) from stories where imported=0 and doNotImport=0) + (select count(*) from bookmarks where imported=0 and doNotImport=0) ,
    `SendEmail`='1';
