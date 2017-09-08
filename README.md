# open-doors-code
Scripts and miscellaneous code to aid Open Doors imports. This currently supports Automated Archive (AA) and eFiction (EF)
databases, and with some manual work, can also be used to process any type of archive.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [open-doors-code](#open-doors-code)
  - [Process](#process)
    - [Set up your system and the Open Doors scripts](#set-up-your-system-and-the-open-doors-scripts)
    - [Prepare the archive backup for local processing](#prepare-the-archive-backup-for-local-processing)
    - [Step 01 - Load the original database into MySQL](#step-01---load-the-original-database-into-mysql)
      - [Notes on specific archives](#notes-on-specific-archives)
        - [eFiction](#efiction)
        - [Automated Archive](#automated-archive)
        - [Custom archives](#custom-archives)
    - [Step 02 - Extract tags from the original stories](#step-02---extract-tags-from-the-original-stories)
      - [Notes on specific archives](#notes-on-specific-archives-1)
        - [eFiction](#efiction-1)
    - [Step 03 - Export tags, authors and stories](#step-03---export-tags-authors-and-stories)
    - [Step 04 - Reimport the Tag Wrangling sheet and map the original tags to the new AO3 tags](#step-04---reimport-the-tag-wrangling-sheet-and-map-the-original-tags-to-the-new-ao3-tags)
    - [Step 05 - Create the Open Doors tables](#step-05---create-the-open-doors-tables)
    - [Step 06 - Copy AO3 tags into the stories table](#step-06---copy-ao3-tags-into-the-stories-table)
    - [Stage 07 - Load Chapters into the Open Doors chapters table](#stage-07---load-chapters-into-the-open-doors-chapters-table)
  - [Other Scripts](#other-scripts)
    - [Remove DNI from Open Doors tables](#remove-dni-from-open-doors-tables)
  - [Parameters](#parameters)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Process

### Set up your system and the Open Doors scripts

You will need the following installed before you start (consult the tools' documentation for installation instructions 
for your operating system):
- MySQL server 5.7 or higher
- Python 2.7 (the scripts have not been tested with Python 3)

Some general tools you will find useful:
- A text editor which can open and save files with different encodings, and perform regular expression replacing across
files in a directory. For example: Sublime Text (on MacOS) or Notepad++ (on Windows)
- A MySQL client that allows you to view tables side-by-side. For example: Sequel Pro (MacOS) or MySQL Workbench (all 
operating systems) 

1. Either clone the repository at https://github.com/otwcode/open-doors-code, or download the code as a zip file. 
(Note that if you download the code, you will need to download it again when changes are made) 
1. Run `pip install -r requirements.txt` from the root folder of the project to install required dependencies


### Prepare the archive backup for local processing
1. Copy the archive backup to your local machine. You will need the following files:
    1. The story metadata (authors, titles, summaries, tags etc.)
        - For Automated Archive, this is in a Perl file called ARCHIVE_DB.pl. 
        - For eFiction, it will typically be a MySQL dump in a `.sql` file. 
        - Other archive types may store their metadata in a custom database, or in flat HTML files. These archives will 
        need bespoke handling for step 01, but are handled as AA from step 02 onward. 
    1. The story files. 
        - For AA, this is usually in a folder called `archive`. 
        - For EF, the folder is usually called `stories`.
        - Other archives may store their story contents elsewhere, for instance, in the database itself or as flat HTML files.
    
1. Make a copy of `example.yml`, give it a simple name related to the archive you're processing, and fill it in. 
See [Parameters](#parameters) for the list of properties. You will be prompted for any property you didn't include in 
the file if it is needed for a given stage.


### Step 01 - Load the original database into MySQL

    python 01-Load-into-Mysql.py -p <archive name>.yml
   
This imports the database file specified in the `db_input_file` into the `temp_db_database` on your MySQL server 
using the `db_host`, `db_user` and `db_password` properties. The destination database will be destroyed and recreated
every time you run the script, so you can safely rerun it as often as needed.

#### Notes on specific archives
##### eFiction
Dumps from eFiction sometimes include commands to recreate and use the database name from the original archive. This script should skip the command to use the original's archive name, but if it doesn't, make sure to edit `temp_db_database` to match the original archive's database name as later steps will fail otherwise.

##### Automated Archive
*Import problems*: Some ARCHIVE_DB.pl files contain formatting that breaks the import. Common problems include, but are not limited to:
- unescaped single quotes
- irregular indents
- line breaks within fields
- characters incompatible with UTF-8
- HTML entities
You will get a Python error when something breaks the import; this will include a snippet of the record that could not 
be processed, so use that to find the record in the ARCHIVE_DB.pl and look for problems like the above. You will have 
to manually edit the file in your text editor to resolve these issues.

*Tag fields*: As the metadata in AA files is customisable, you can use the `tag_fields`, `character_fields`,
`relationship_fields` and `fandom_fields` properties to map fields in the ARCHIVE_DB.pl to the right columns in the 
temporary database table. 

##### Custom archives
The step 01 script can't be used with archive which do not use Automated Archive or eFiction. The metadata for custom 
archives which are needs to be loaded manually or using custom scripts into `authors`, `bookmarks`, `chapters` 
and `stories` tables matching [the Open Doors table schema](shared_python/create-open-doors-tables.sql) in the 
`temp_db_database`. 

These archives are then treated as Automated Archive archives by all the scripts from step 02 onward. 


### Step 02 - Extract tags from the original stories

    python 02-Extract-Tags-From-Stories.py -p <archive name>.yml

This script creates a table called `tags` in the temporary database and denormalises all the tags for every story.
This table is the basis for the Tag Wrangling sheet and is used to map the tags back to the story when the final
tables are created. Do not edit the `tags` table manually - it will be destroyed and recreated every time you run this 
script.

*Note*: This step splits the tag fields on commas. If the archive you are processing allowed commas in tag names, you
will need to replace those commas with another character and let Tag Wrangling know this is what you've done. 

#### Notes on specific archives
##### eFiction
Some eFiction versions have comma-delimited ids in the story tag fields instead of the name of the tag. You will need
to inspect the `fanfiction_stories` table to determine if this is the case before running step 02. The script will ask you if all the tag fields contain ids (rather than text). If they do, answer y, and it will look up the tag text in the original tag table.


### Step 03 - Export tags, authors and stories

    python 03-Export-Tags-Authors-Stories.py -p <archive name>.yml

Before an external archive can be imported, the following two steps need to be performed:

1. the external archive's tags have to be mapped to the Archive's existing tags. This saves tag wranglers from having to
map the external tags manually to the correct ones.

2. all the stories from the original archive have to searched for on the Archive to prevent importing duplicates.

This step exports those two CSV files which you then have to import into Google Spreadsheet and share with the rest of the Open Doors committee.


### Step 04 - Reimport the Tag Wrangling sheet and map the original tags to the new AO3 tags

    python 04-Rename-Tags.py -p <archive name>.yml

When Tag Wrangling have finished mapping the tags in Google Drive, export the Google spreadsheet as a CSV file and make
sure its path is specified in `tag_input_file`. This script then copies the AO3 tags from that file into the 
`tags` table in the temporary database.


### Step 05 - Create the Open Doors tables

    python 05-Create-Open-Doors-Tables.py -p <archive name>.yml

This script creates the tables for the temporary import site and populates them based on the data in the temporary
database. It also filters out authors without stories, and if a file of comma-separated ids is specified in 
the `story_ids_to_remove` property, it will also filter out any stories in the list.

The temporary sites are currently all run off the same database, with the tables prefixed to distinguish them - specify 
the prefix to use in `db_table_prefix`.

This script will destroy the prefixed tables for this archive before recreating them, so do not edit them manually
until you are sure you are finished with this stage.

*Notes*: 
- The `stories` and `bookmarks` tables will not contain any tags at all after this stage. These aren't added
until you run step 06.
- The `chapters` table will not contain the story contents, which are loaded in step 07.


### Step 06 - Copy AO3 tags into the stories table

    python 06-Update-Tags-In-Story-Table.py -p <archive name>.yml

This script matches up the AO3 tags from the `tags` table with the corresponding stories. Note
that unlike the other scripts, this one does not destroy any databases or tables, though it does overwrite the tag 
fields in the `stories` or `bookmarks` databases.


### Step 07 - Load Chapters into the Open Doors chapters table

    python 07-Load-Chapters-to-Open-Doors-Table.py -p <archive name>.yml

Loads the chapter contents in the output database (this can be run at any point after stage 05). It does this by going
through all the files in the `chapters_path` and trying to find an entry in the chapters table that has the same
`url`. It then copied the contents of the file into the `text` column for that row.

If there are duplicate chapters (for example if co-authored stories were listed under each author), the script will
try to deduplicate them by only keeping the duplicate whose `authorid` is the same as the `authorid` in the `story` table.
It will list duplicates it has found in the console output. 

Common problems to look out for when processing chapters:
- Email addresses in story files. These should be removed to protect the authors, but check for any stories that include 
fictional email conversations between the characters.
- Navigation for the original site should be removed. (This is not typically a problem for eFiction sites)
- Encoding problems - these result in curly quotes and accented characters being replaced by rubbish characters. Trying 
"Windows 1252" instead of "UTF-8" when prompted may solve this, or you might have to edit-replace the broken characters
in the affected story files.
- In some cases, a story file might contain a character that prevents it from being copied to the MySQL table. Edit the 
story manually to resolve.
- Missing stories - sometimes the url in the database doesn't exactly match the path to the story. You should check for
empty chapters after this step and look for their corresponding chapter files manually.


## Other Scripts

### Remove DNI from Open Doors tables

Given a comma-separated list of story ids specified in the `story_ids_to_remove` parameter, deletes the corresponding 
rows from the `table_prefix`_stories table in the final output database.




## Parameters

| Flag | Property name            | Description |
|------|--------------------------|----------------------------------|
| -h   | help                     | show help message and exit |
| -p   | properties_file          | Load properties from specified file (ignores all command-line arguments). This is the simplest way to handle all these options. See `example.yml`. |
| *MySQL* |
| -dp  | db_password              | MySQL password |
| -du  | db_user                  | MySQL user |
| -dh  | db_host                  | MySQL host name and port |
| *General* |
| -a   | archive_type             | Type of archive: AA or EF |
| -o   | output_folder            | Path for output files (creator works, and tag spreadsheets) |
| -df  | default_fandom           | Default fandom to use. Optional - the column will only be populated with fandoms from the TW sheet if this is blank. |
| -si  | story_ids_to_remove      | Location of the text file containing the story ids to remove. Optional - if no path is specified, the stories table will be copied over as is. |
| *Databases* |
| -i   | db_input_file            | Full path to input file (ARCHIVE_DB.pl for AA, SQL script for eFiction)|
| -dd  | temp_db_database         | MySQL temporary database name to use for processing (will be destroyed in step 1 if it exists) |
| -dt  | db_table_prefix          | MySQL prefix for tables eg: "isf" for Ink Stained Fingers, "hex" for The Hex Files and so on. |
| -od  | output_database          | Name of the database the final tables should be created in (default "od_sgf") |
| *Tags* |
| -t   | tag_input_file           | Full path to Tag Wrangling CSV |
| -n   | archive_name             | Name of the original archive (used in export file names) |
| -ft  | tag_fields               | Name of tag field(s) in original db (comma-delimited) |
| -fc  | character_fields         | Name of character field(s) in original db (comma-delimited) |   
| -fr  | relationship_fields      | Name of relationship field(s) in original db (comma-delimited) |
| -ff  | fandom_fields            | Name of fandom field(s) in original db (comma-delimited) |     
| *Chapters* |
| -cp  | chapters_path            | Location of the text files containing the stories. Optional - if no path is specified, the chapter table will be copied over as is. |
| -cf  | chapters_file_extensions | File extension(s) of the text files containing the stories (eg: "txt, html"). Only required if a chapter path is specified. |

If the `-p` flag is set, these values will be read from a YAML file in same folder as the script (see `example.yml`
in the project root). This is a much simpler way of providing the parameters, but they can also be passed on the
command line using the flags specified. For example:

    python 01-Load-into-Mysql.py -dh localhost -du root -dd od_dsa -a AA -i /Users/me/Documents/ARCHIVE_DB.pl
    
You will be prompted for any missing settings when you run each stage.




    
