# open-doors-code

Code to convert Open Doors imports into a set of tables for importing. 

## Process

### Set up your system and the Open Doors scripts

You will need the following installed before you start (consult the tools' documentation for installation instructions
for your operating system):
- MySQL server 5.7 or higher
- Python 3.8

Some general tools you will find useful:
- A text editor which can open and save files with different encodings, and perform regular expression replacing across
files in a directory. For example: Sublime Text (on MacOS) or Notepad++ (on Windows)
- A MySQL client that allows you to view tables side-by-side. For example: Sequel Pro (MacOS) or MySQL Workbench (all
operating systems)

1. Either clone the repository at https://github.com/otwcode/open-doors-code, or download the code as a zip file.
(Note that if you download the code, you will need to download it again when changes are made)
1. Strongly recommended: create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for this project 
   to keep its dependencies separate from other Python projects you might have.
1. Run `pip install -r requirements.txt` from the root folder of the project to install required dependencies


### Prepare the archive backup for local processing
Note: for eFiction Archives, pre-process the archive using the [eFiction Processor](https://github.com/otwcode/open-doors-eFiction).
1. Copy the archive backup to your local machine. You will need the following files:
    1. The story metadata (authors, titles, summaries, tags etc.)
        - For Automated Archive, this is in a Perl file called ARCHIVE_DB.pl.
        - Other archive types may store their metadata in a custom database, or in flat HTML files. These archives will
        need bespoke coding or manual processing to create the MySQL tables in step 01.
    1. The story files.
        - For AA, this is usually in a folder called `archive`.
        - Other archives may store their story contents elsewhere, for instance, in the database itself or as flat HTML files.

1. Make a copy of `example.yml`, give it a simple name related to the archive you're processing, and fill it in.
See [Parameters](#parameters) for the list of properties. You will be prompted for any property you didn't include in
the file if it is needed for a given stage.

## High-level overview of each step

- 01 - Load the original data into a temporary database for processing (AA only)
- 01.5 - Load chapters into the chapters table of the temporary database (AA and custom only)
- 02 - Extract tags from stories and story links into a new `tags` table. (AA and custom only)
- 03 - Export the distinct tags into a spreadsheet to enable wranglers to map tags to AO3 tags, and export story and
story link information into spreadsheets used for searching. (all)
- 04 - Map the tags in the `tags` table to AO3 tags suggested by wranglers. (all)
- 05 - Create the final tables that will be used for the temp site and copy all the authors, stories and story links. (all)
- 06 - Copy the AO3 tags into the final story and story link rows. (all)
- 08 - Audit the final tables to find common problems. (all)

At this point, the final database is ready to be loaded into a [temporary website](https://github.com/otwcode/open-doors-temp-site) that will be used to feed the works into
the Archive using its mass import API.

### Step 01 - Load the original database into MySQL (AA and custom)

This step populates a set of temporary tables which will be used for later processes.

#### Automated Archive

    python 01-Load-Automated-Archive-into-Mysql.py -p <archive name>.yml

This imports the Automated Archive ARCHIVE_DB.pl file specified in the `db_input_file` property into the 
`temp_db_database` on your MySQL server using the `db_host`, `db_user` and `db_password` properties. The destination 
database will be destroyed and recreated every time you run the script, so you can safely rerun it as often as needed.

*Import problems*: Some ARCHIVE_DB.pl files contain formatting that breaks the import. Common problems include, but are not limited to:
- unescaped single quotes
- irregular indents
- line breaks within fields
- characters incompatible with UTF-8
- HTML entities

You will get a Python error when something breaks the import; this will include a snippet of the record that could not
be processed, so use that to find the record in the ARCHIVE_DB.pl and look for problems like the above. You will have
to manually edit the file in your text editor to resolve these issues.

*Fields*: All the field names found in the file will be listed in the console output when you run this step, allowing you
to populate the tag fields (see below) with all the relevant fields in the ARCHIVE_DB.pl file.

*Tag fields*: As the metadata in AA files is customisable, you can use the `tag_fields`, `character_fields`,
`relationship_fields` and `fandom_fields` properties to map fields in the ARCHIVE_DB.pl to the right tag columns in the
temporary database table.

##### Custom archives

The step 01 script can't be used with archives which do not use Automated Archive or eFiction. The metadata for custom
archives needs to be loaded manually or using custom scripts into `authors`, `story_links`, `chapters`
and `stories` tables matching [the Open Doors table schema](shared_python/create-open-doors-tables.sql) in the
`temp_db_database`.

### Step 02a - Load Chapters into the chapters table [NEEDS REVISION]

    python 02-Load-Chapters-to-Open-Doors-Table.py -p <archive name>.yml

Loads the chapter contents in the output database (this can be run at any point after stage 05). It does this by going
through all the files in the `chapters_path` and trying to find an entry in the chapters table that has the same
`url`. It then copied the contents of the file into the `text` column for that row.

You will be prompted to answer two questions:

    Chapter file names are chapter ids? Y/N

Look at the file names in `chapters_path`  and compare against the `chapterid` column in the database. For AA or other databases they probably are more likely to be a human
readable name instead (N).

    Importing chapters: pick character encoding (check for curly quotes):
    1 = Windows 1252
    enter = UTF-8

See note at the end about encoding problems and other issues that usually need to be fixed in chapters.

If there are duplicate chapters (for example if co-authored stories were listed under each author), the script will
try to deduplicate them by only keeping the duplicate whose `author_id` is the same as the `author_id` in the `story` table.
It will list duplicates it has found in the console output.

### Step 02b - Extract tags from the original stories (AA and custom)

    python 02-Extract-Tags-From-Stories.py -p <archive name>.yml

This script creates a table called `tags` in the temporary database and denormalises all the tags for every story and story link.
This table is the basis for the Tag Wrangling sheet and is used to map the tags back to the story when the final
tables are created. Do not edit the `tags` table manually - it will be destroyed and recreated every time you run this
script.

*Note*: This step splits the tag fields on commas. If the archive you are processing allowed commas in tag names, you
will need to replace those commas with another character and let Tag Wrangling know this is what you've done.

For multi-fandom archives that specify the fandoms for each story, the `fields_with_fandom` parameter can be used to
specify that tags from the listed columns should be exported with the fandom.


### Step 03 - Export tags, authors and stories (all: eFiction, Automated Archive and custom)

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
database. It also filters out authors without stories, and if .txt files of comma-separated ids (no final comma) are specified in
the `story_ids_to_remove` or `bookmark_ids_to_remove` properties, it will also filter out any stories or bookmarks in the list.

You will need to create an empty database (eg in Sequel Pro) for the new tables to be inserted into if you haven't already made a generic one for a previous site. Include it as property `output_database` in your yml file.

This script will destroy the temp database before recreating it, so do not edit them manually
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

*Notes*:
- The output for this command  (eg "Getting all tags per story...429/429 stories") will report the number of stories in 
the tag table, which may be more than the number of stories you have after removing DNI in the previous stage.

### Step 08 - Audit final tables for common problems

|   python 08-Check-ODAP-Tables.py -p <archive name>.yml

This script performs checks on common reasons for Archive rejection, including checking for chapters that are too long, stories that have too many chapters, etc. It makes no attempt to fix problems that arise; you must do that manually.  Also note, it will only perform each check (aligned to the old JIRA tickets O, P, Q, R, and S) if no problems have been found on previous steps.  If you encounter errors in any step, you will need to repeat running the script and fixing the errors until it exits cleanly.

### Common problems to look out for when processing chapters

*Tip*: Some of these problems might be easier to fix by loading the chapters into MySQL and then exporting the `chapters`
table as a MySQL dump. You can then perform edit-replace operations on all the chapters at once (though be very careful
not to break the MySQL commands!). Then you can import the edited dump back into MySQL.

- Email addresses in story files. These should be replaced with the text `[email address removed]` to protect the authors, 
but check for any stories that include fictional email conversations between the characters (you probably want to keep 
the made up addresses in that case). Use a text editor that can find and replace using Regular expressions (regex) - 
for example Notepad++ on Windows or Sublime on Mac. To find email addresses try: `.*(\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b).*`
- Navigation for the original site should be removed. (This is not typically a problem for eFiction sites)
- Other links may need to be removed depending on where they linked to. If they are relative links they definitely 
should be removed. Regex to find opening and closing <a> tags so you can find the links: `</?a(?:(?= )[^>]*)?>`
- Encoding problems - these result in curly quotes and accented characters being replaced by rubbish characters. Trying
"Windows 1252" instead of "UTF-8" when running the script may solve this, or you might have to edit-replace the broken characters
in the affected chapters.
- In some cases, a story file might contain a character that prevents it from being copied to the MySQL table. Edit the
story manually to resolve.
- Missing stories - sometimes the url in the database doesn't exactly match the path to the story. You should check for
empty chapters after this step and look for their corresponding chapter files manually. If found, paste the HTML of the 
story into the empty `text` column for that row in MySQL.
- If the authors table has co-authors listed with 2 email addresses in an entry, create a new line in the authors table 
for the second author, amend the first author, then put the second author ID into the `coauthor_id` column of the stories table
- The author table may need to be de-duped


## Other Scripts

### Remove emails from Open Doors tables

Scans the chapter for emails and removes some of them:

- If the email is present in the `authors` table, the email is redacted automatically.
- If the "email" does not contain alpha numeric characters, for example `~~~@~~~`, then it is preserved.
- If the email is something different a prompt is shown to the user, for example:

```
	
	<p>Lily, the Vampire Slayer</p>
	
	<p>by: Br@nw3n</p>
	
	<p>Prologue</p>
	
	<p>"Ernie!" Lily Evans

Br@nw3n ([W]hitelist, [B]lacklist) ([A]ddress, [D]omain) [C]ontext [R]ewrite domain >
```

On it we can either type (and press enter):

- `wa` - Allow this specific address, it will not be redacted and you will not be asked about it again.
- `wd` - Same as above, but allows all addresses from this specific domain, use with emails like `luz@theowlhouse.bi`, where the domain `theowlhouse.bi` was made up by the author.
- `ba` - Redact this specific address.
- `bd` - Redact this domain, use with domains like `gmail.com`, where the emails are likely to be real.
- `r` - Rewrite this email, does search and replace for this particular email.
- `c` - show the context the email shows up in, the more `ccccccc`, the more context you get.

### Remove DNI from Open Doors tables

Given a comma-separated list of story ids specified in the `story_ids_to_remove` parameter, deletes the corresponding
rows from the stories table in the final output database.


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
| -bi  | bookmark_ids_to_remove   | Location of the text file containing the bookmark ids to remove. Optional - if no path is specified, the bookmark table will be copied over as is. |
| *Databases* |
| -i   | db_input_file            | Full path to input file (ARCHIVE_DB.pl for AA)|
| -dd  | temp_db_database         | MySQL temporary database name to use for processing (will be destroyed in step 1 if it exists) |
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
