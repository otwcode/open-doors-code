#!/usr/bin/env python3

import sys
from shared_python.Args import Args
from shared_python.Sql import Sql

if __name__ == "__main__":
    """Perform various audits to ensure data quality on the ODAP tables prior to
    export."""
    args_obj = Args()
    args = args_obj.args_for_08()

    log = args_obj.logger_with_filename()
    sql = Sql(args, log)
    db: str = args.output_database
    found_error = False

    log.info(f"Performing quality checks on {db}")
    sql.execute(f"USE {db}")

    ##
    ## Check for too many tags
    ##

    # The Archive will error if a work has more than 75 total tags.

    log.debug("Checking for too many tags.")

    tag_counts: dict[str, int] = sql.execute_dict(
        """SELECT
        id,
        length(categories) - length(replace(categories, ",", "")) as cat_num,
        length(characters) - length(replace(characters, ",", "")) as chr_num,
        length(fandoms) - length(replace(fandoms, ",", "")) as fnd_num,
        length(tags) - length(replace(tags, ",", "")) as tag_num
        FROM
        stories""",
    )

    for story in tag_counts:
        # We're counting commas, not items, so we need to add 4 to the total to
        # account for the worst-case of each type having one entry.
        total = (
            story["cat_num"]
            + story["chr_num"]
            + story["fnd_num"]
            + story["tag_num"]
            + 4
        )
        if total > 75:
            log.error(f"Found story {story['id']} with too many tags!")
            found_error = True

    if found_error:
        log.error("Found at least one story with too many tags; ending audit here.")
        sys.exit(1)

    ##
    ## Check for excessively long summaries
    ##

    # The Archive does not support summaries longer than 1250 characters.

    log.debug("Checking for excessively long summaries.")
    found_error = False

    long_sums = sql.execute_dict(
        "SELECT id, char_length(summary) as len FROM stories HAVING len >= 1250"
    )
    if long_sums:
        found_error = True
        for story in long_sums:
            log.error(f"Found story {story['id']} with too long summary!")

    if found_error:
        log.error("Found at least one story with too long summary; ending audit here.")
        sys.exit(2)

    ##
    ## Check for excessively long notes
    ##

    # The Archive does not support notes longer than 5000 characters.

    log.debug("Checking for excessively long notes.")
    found_error = False

    long_notes = sql.execute_dict(
        "SELECT id, char_length(notes) as len FROM stories HAVING len >= 5000"
    )
    if long_notes:
        found_error = True
        for story in long_notes:
            log.error(f"Found story {story['id']} with too long notes!")

    if found_error:
        log.error(
            "Found at least one story with excessively long notes; ending audit here."
        )
        sys.exit(3)

    ##
    ## Check for too-long chapters
    ##

    # Chapters longer than 500,000 characters should be split.
    # NB: This is counting bytes, not characters, for performance reasons.
    log.debug("Checking for too long chapters.")
    found_error = False

    long_chap = sql.execute_dict(
        "SELECT id as chap, story_id as sid, length(text) as len FROM chapters HAVING len > 500000",
    )
    if long_chap:
        found_error = True
        for story in long_chap:
            log.error(
                f"Found chapter {story['chap']} in story {story['sid']} that could be too long.  Check to make sure it's under 500k characters."
            )

    if found_error:
        log.error("Found at least one too-long chapter; ending audit here.")
        sys.exit(4)

    ##
    ## Check for stories with too many chapters
    ##

    # The Archive does not allow importing a story with more than 200 chapters
    log.debug("Checking for stories with too many chapters")
    found_error = False

    many_chap = sql.execute_dict(
        "SELECT story_id as sid, count(id) as len FROM chapters GROUP BY sid HAVING len >= 200",
    )
    if many_chap:
        found_error = True
        for story in many_chap:
            log.error(
                f"Found story {story['sid']} that has too many chapters ({story['len']})!"
            )

    if found_error:
        log.error("Found at least one story with too many chapters; ending audit here.")
        sys.exit(5)

    log.info("All checks completed successfully.")
