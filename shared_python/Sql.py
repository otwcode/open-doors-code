import re
import warnings

# ignore unhelpful MySQL warnings
from pymysql import connect, cursors, OperationalError

warnings.filterwarnings("ignore", category=Warning)


class Sql(object):
    def __init__(self, args, log):
        self.tag_count = 0
        conn = connect(args.db_host, args.db_user, args.db_password)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS `{0}`".format(args.temp_db_database)
        )
        self.log = log

        self.conn = connect(
            args.db_host,
            args.db_user,
            args.db_password,
            args.temp_db_database,
            charset="utf8",
            use_unicode=True,
            autocommit=True,
        )
        self.cursor = self.conn.cursor()
        self.database = args.temp_db_database

    def execute(self, script, parameters=(), database=None):
        cursor = self.conn.cursor()
        cursor.execute(f"USE {database or self.database}")
        cursor.execute(script, parameters)
        self.conn.commit()

    def execute_dict(self, script, parameters=()):
        dict_cursor = self.conn.cursor(cursors.DictCursor)
        dict_cursor.execute(script, parameters)
        return dict_cursor.fetchall()

    def execute_and_fetchall(self, database: str, statement: str):
        """
        Execute a SQL statement and then fetch its results.
        :param database: The database to run the statement against.
        :param statement: The SQL statement to execute.
        :return: The fetched result of the SQL statement as a dict.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"USE {database}")
        cursor.execute(statement)
        self.conn.commit()
        return cursor.fetchall()

    def run_script_from_file(self, filename, database, initial_load=False):
        # Open and read the file as a single buffer
        fd = open(filename, "r")
        sqlFile = fd.read()
        fd.close()

        # replace placeholders and return all SQL commands (split on ';')
        sqlCommands = sqlFile.replace("$DATABASE$", database).split(";\n")

        # Start a transaction
        self.cursor.execute("START TRANSACTION")
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(database))
        self.cursor.execute("USE {0}".format(database))

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                # Strip out commented out lines
                end_command = re.sub(r"(--|#|\/\*).*?\n", "", command)
                lc_command = end_command.lower().strip().replace("\n", "")
                if initial_load and (
                    lc_command.startswith("create database ")
                    or lc_command.startswith("use ")
                ):
                    self.log.info("Skipping command - {0}".format(lc_command))
                elif lc_command is None or lc_command == "":
                    self.log.info(lc_command)
                else:
                    self.cursor.execute(lc_command)
            except OperationalError as e:
                self.log.info("Command skipped: {0} [{1}]".format(command, e))

        self.conn.commit()

    def col_exists(self, col, table, database):
        self.cursor.execute(
            """
        SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{0}' AND TABLE_NAME = '{1}' AND COLUMN_NAME = '{2}'
      """.format(database, table, col)
        )
        result = self.cursor.fetchone()
        return result is not None
