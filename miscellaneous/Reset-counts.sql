set sql_safe_updates=0;
use $DATABASE$;
UPDATE $PREFIX$_stories set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE $PREFIX$_bookmarks set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE $PREFIX$_authors set doNotImport=0, imported=0 where donotimport=1 or imported=1;
UPDATE $PREFIX$_stories set Ao3Url=null where Ao3Url is not null;
UPDATE $PREFIX$_bookmarks set Ao3Url=null where Ao3Url is not null;
UPDATE archiveconfig
	set imported=0,
    NotImported = (select count(*) from $PREFIX$_stories),
    `SendEmail`='1'
    where `key`= "$PREFIX$";

