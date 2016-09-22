set sql_safe_updates=0;
use DATABASE;
UPDATE KEY_stories set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE KEY_bookmarks set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE KEY_authors set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE KEY_stories set Ao3Url=null where Ao3Url is not null;
UPDATE KEY_bookmarks set Ao3Url=null where Ao3Url is not null;
UPDATE archiveconfig 
	set imported=0, 
    NotImported = (select count(*) from KEY_stories),
    `SendEmail`='1'
    where `key`= KEY;

