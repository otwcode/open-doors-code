#!/bin/python3
from shared_python.Args import Args
from shared_python.Sql import Sql
import re
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import clear

email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
)

def print_context(match, amount: int):
    start, end = match.span()
    pre_context = "\t" + match.string[max(start - amount, 0) : start].replace('\n', '\n\t')
    value = match.string[start : end]
    post_context = match.string[end : end + amount].replace('\n', '\n\t')
    print_formatted_text(FormattedText([
        ('', pre_context),
        ('#ff0000 bold', value),
        ('', post_context),
    ]))

def does_contain_letters(text: str) -> bool:
    return any(x in text for x in 'qwertyuiopasdfghjklzxcvbnm') 

def is_mailto(match) -> bool:
    start, _ = match.span()
    mailto = 'mailto:'
    if len(mailto) > start:
        return False
    return mailto == match.string[start - len(mailto) : start]

def ask_user_for_action(match) -> str:
    start, end = match.span()
    raw_email = match.string[start:end]
    domain = match.group(5)
    clear()
    print_context(match, 50)
    while True:
        try:
            return return_from_list(match)
        except:
            response = input(
                f"\n{raw_email} ([W]hitelist, [B]lacklist) ([A]ddress, [D]omain) [C]ontext [R]ewrite domain >\n\t"
            ).lower()
            if "c" in response:
                amount = 50 * response.count("c")
                print_context(match, amount)
            elif "r" in response:
                new_email = input("Enter new email: ")
                if "@" in new_email:
                    addresses[raw_email] = new_email
            elif any(x in response for x in "wb") and any(
                x in response for x in "ad"
            ):
                should_block = "b" in response
                if "d" in response:
                    domains[domain] = not should_block
                    print(domain)
                else:
                    addresses[raw_email] = not should_block


BAN_TEXT = "[email address redacted]"
domains = {}
addresses = {}

def return_from_list(match) -> str:
    start, end = match.span()
    raw_email = match.string[start:end]
    address_entry = addresses.get(raw_email)
    if address_entry is False:
        return BAN_TEXT
    elif address_entry is True:
        return raw_email
    elif address_entry is not None:
        return address_entry
    domain = match.group(5)
    domain_entry = domains.get(domain)
    if domain_entry is True:
        return raw_email
    elif domain_entry is False:
        return BAN_TEXT
    raise Exception("Failed to resolve")

def escape_for_sql(raw: str) -> str:
    return raw.replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")

if __name__ == "__main__":
    args_obj = Args()
    args = args_obj.args_for_05()
    log = args_obj.logger_with_filename()
    sql = Sql(args, log)
    author_emails = [
        x[0]
        for x in sql.execute_and_fetchall(
            args.output_database, "SELECT email FROM authors"
        )
    ]
    chapter_count = int(
        sql.execute_and_fetchall(
            args.output_database, "SELECT COUNT(*) FROM chapters"
        )[0][0]
    )
    for index, (id, title, text, notes) in enumerate(
        sql.execute_and_fetchall(
            args.output_database,
            """
            SELECT 
                id, title, text, notes
            FROM 
                chapters 
            """,
        )
    ):
        print(f"{round(index / chapter_count * 100, 2)}%\t- chapter {id}", end="\r")

        def replace_func(email):
            start, end = email.span()
            raw_email = email.string[start:end]
            if raw_email in author_emails:
                # email is a real email, cause it is in users table!
                return BAN_TEXT
            if not does_contain_letters(raw_email):
                # match is not an email, but something like `!@~` or '/@/'
                return raw_email
            if is_mailto(email):
                # Mailto links are presumed to be real
                addresses[raw_email] = False
            try: 
                return return_from_list(email)
            except:
                return ask_user_for_action(email)

        cleared_text = email_regex.sub(replace_func, text)
        cleared_notes = email_regex.sub(replace_func, notes)
        if cleared_text != text or cleared_notes != notes:
            update_query = """
UPDATE chapters
    SET 
        text = %s ,
        notes = %s
    WHERE 
        id = %s;
            """.strip()
            sql.execute(update_query, (cleared_text, cleared_notes, id), args.output_database)
