# open-doors-code
Scripts and miscellaneous code to aid Open Doors imports. This currently supports Automated Archive and eFiction
databases.

## High-level process


1. Copy the MySQL script and/or site backup to their local machine
1. Create a MySQL database for the processing stage (we recommend a naming format like **od_archive_name**)
1. Create an `\<archive_name\>.yml` properties file for the archive including that database name (see `example.yml`)
1. Run Stage 01 to load the metadata into the MySQL database. Verify that authors, stories and chapters (if applicable) are present. You may need to tweak the scripts of the input files to get the best possible result - don't rush this phase.
1. Run Stage 02 to extract the tags from the stories. Before you run this script, look at the story table in the database to see what fields contain tags and whether those tags are ids that reference another table, or plain text tags, as the script will prompt you for this information.
1. Run Stage 03 to export lists of authors with works, and a list of tags. Upload these to Google Spreadsheets in the Google Drive folder for the archive you're importing. These will be used in the following tasks:
    - **Open Doors** search the Archive for existing works from the list you provided.
    - **Tag Wrangling** map the tags you extracted from your database to existing approved tags on the Archive.
1. When the above processes are complete, process the resulting spreadsheets:
    - Download the Tag Wrangling spreadsheet as a comma-separated file. 
    - Generate a comma-separated list of story ids for stories which already exist in the Archive. 
1. Run Stage 04 to map the tags in your database to their AO3 equivalents. The Tag Wrangling spreadsheet is the input for this process - if necessary, amend your properties file to point to the file you downloaded from Google Drive. You may also need to tidy it up manually if tag wranglers have added notes or change column headings.
1. TBA: DNI removal
1. Run Stage 05 to create the final table for the import site. This destructively creates new tables in the output database. Note: the stories table will not contain any tags at this point.
1. Run Stage 06 to update the tags in the output database (stages 04 and 06 can be rerun without running stage 05 if there are problems with the tags).


## Parameters

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -h  | help            | show help message and exit
| -dp | db_password     | MySQL password |
| -du | db_user         | MySQL user |
| -dh | db_host         | MySQL host name and port |
| -dd | db_database     | MySQL temporary database name to use for processing (will be destroyed if it exists) |
| -dt | db_table_prefix | MySQL prefix for tables |
| -a  | archive_type    | Type of archive: AA or EF |
| -i  | db_input_file   | Full path to input file (ARCHIVE_DB.pl for AA, SQL script for eFiction)|
| -o  | output_folder   | Path for output files |
| -t  | tag_input_file  | Full path to Tag Wrangling CSV |
| -od | output_database | Name of the database the final tables should be created in (default "od_sgf") |
| -n  | archive_name    | Name of the original archive (used in export file names) |
| -cp | chapters_path   | Location of the text files containing the stories. Optional - if no path is specified, the chapter table will be copied over as is. |
| -cf | chapters_file_extensions |  File extension(s) of the text files containing the stories (eg: "txt, html"). Only required if a chapter path is specified. |
| -df | default_fandom    | Default fandom to use. Optional - the column will only be populated with fandoms from the TW sheet if this is blank. |
| -p  | properties_file | Load properties from specified file (ignores all other arguments) |

If the `-p` flag is set, these values will be read from a YAML file in same folder as the script (see `example.yml`
in the project root. This is a much simpler way of providing the parameters, but they can also be passed on the
command line using the flags specified. For example:

    python 01-Load-into-Mysql.py -dd localhost -du root -dd od_dsa -a AA -i /Users/me/Documents/ARCHIVE_DB.pl


## Scripts
The scripts should be run in the order indicated. Each stage can be rerun individually as many times as necessary (for
example, due to changes in the Tag Wrangling sheet). Do not modify the MySQL tables manually during this process, as the tables and their contents will be overwritten when you rerun a script.

All the scripts rely on the following properties being set (you will be prompted for the properties required):

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -dp | db_password     | MySQL password |
| -du | db_user         | MySQL user |
| -dh | db_host         | MySQL host name and port |
| -dd | db_database     | MySQL temporary database name to use for processing (will be destroyed if it exists) |
| -dt | db_table_prefix | MySQL prefix for tables |
| -a  | archive_type    | Type of archive: AA or EF |

The properties required only for certain scripts are detailed in the appropriate section below.

### Stage 01 - Load the original database into MySQL
This script will import the ARCHIVE_DB.pl for an Automated Archive or the MySQL dump for an eFiction database into
your MySQL server.

It relies on the following parameters:

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -i  | db_input_file   | Full path to input file (ARCHIVE_DB.pl for AA, SQL script for eFiction)|

*eFiction note*: check that the MySQL script you were given doesn't name the database when creating tables -
otherwise it may recreate the original database on import, or fail to run at all.

Note: this script destroys and recreates the database named in the `db_database` property.

### Stage 02 - Extract tags from the original stories
This script creates a table called `tags` in the temporary database and denormalises all the tags for each story.
This table is the basis for the Tag Wrangling sheet and is used to map the tags back to the story when the final
tables are created.

It relies only on the database parameters.

*eFiction note*: some eFiction versions have comma-delimited ids in the story tag fields. This script will prompt you
to say if this is the case for the database you are processing. If so, it will look up the tag text in the original
tag table.

Note: this script destroys the `tags` table and recreates it - do not edit the `tags` table manually.

### Stage 03 - Export tags, authors and stories
Before an external archive can be imported, the following two steps need to be performed:

1. the external archive's tags have to be mapped to the Archive's existing tags. This saves tag wranglers from having to
map the external tags manually to the correct ones.

2. all the stories from the original archive have to searched for on the Archive to prevent importing duplicates.

As these two processes are done manually, this step exports two CSV files which you then have to import into Google
Spreadsheet and share with the rest of the Open Doors committee.

It relies on the following parameters:

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -o  | output_folder   | Path for output files |

### Stage 04 - Reimport the Tag Wrangling sheet and map the original tags to the new AO3 tags
When Tag Wrangling have finished mapping the tags in Google Drive, export the spreadsheet as a CSV file. This script
then copies the AO3 tags from that file into the `tags` table in the temporary database.

It relies on the following parameters:

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -t  | tag_input_file  | Full path to Tag Wrangling CSV |

### Stage 05 - Create the Open Doors tables
This script creates the tables for the temporary import site and copies in the authors and stories (see below for notes
on bookmarks and chapters).

It relies on the following parameters:

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -od | output_database   | Name of the database the final tables should be created in (default "od_sgf") |
| -cp | chapters_path     | Location of the text files containing the stories. Optional - if no path is specified, the chapter table will be copied over as is. |
| -cf | chapters_file_extensions | File extension(s) of the text files containing the stories (eg: "txt, html"). Only required if a chapter path is specified. |

The temporary sites are currently all run off the same database, with the tables prefixed to distinguish them.

This script will destroy the prefixed tables for this archive before recreating them, so do not edit them manually
until you are sure you are finished with this stage.

### Stage 06 - Copy AO3 tags into the stories table
This script matches up the AO3 tags, fandoms and categories from the `tags` table with the corresponding stories. Note
that unlike the other scripts, this one does not destroy the tables before changing them.

It relies on the following parameters:

| flag | Property name    | Description |
|-----|-------------------|----------------------------------|
| -od | output_database   | Name of the database the final tables should be created in (default "od_sgf") |
| -df | default_fandom    | Default fandom to use. Optional - the column will only be populated with fandoms from the TW sheet if this is blank. |

