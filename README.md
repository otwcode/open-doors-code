# open-doors-code
Scripts and miscellaneous code to aid Open Doors imports

## Temporary Site schema
To simplify imports, the contents of a site to be imported must be loaded into a set of MySQL with a standardised structure.

## eFiction Scripts
eFiction sites already use a MySQL database.

1. Load the eFiction database into your local MySQL instance. We recommend importing it twice so you have a backup you can 
easily refer to if something goes wrong with the conversion.
1. Edit the scripts to match the exact structure of the database you're converting
1. Run the scripts one by one to convert the eFiction database into the format for the temporary site

## Automated Archive
AA sites use a file called ARCHIVE_DB.pl which contains a Perl hashmap.

1. Edit and run the provided Python script to feed the metadata into your local MySQL database

## Copying chapter content into MySQL
Chapter content needs to imported into the chapter table in the temporary site.

1. Edit and run the provided Python script to copy the chapter file contents into the corresponding chapter entry.
