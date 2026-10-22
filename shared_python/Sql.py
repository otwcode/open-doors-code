import re
import warnings

# ignore unhelpful MySQL warnings
from pymysql import OperationalError, connect, cursors

warnings.filterwarnings("ignore", category=Warning)


class Sql:
    def __init__(self, args, log):
        self.tag_count = 0
        conn = connect(host=args.db_host, user=args.db_user, password=args.db_password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{args.temp_db_database}`")
        self.log = log

        self.conn = connect(
            host=args.db_host,
            user=args.db_user,
            password=args.db_password,
            database=args.temp_db_database,
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
        with open(filename, "r") as fd:
            sqlFile = fd.read()
        self.run_sql_file(sqlFile, database, initial_load)

    def run_sql_file(self, sqlFile, database, initial_load=False):
        # replace placeholders and return all SQL commands (split on ';')
        sqlCommands = sqlFile.replace("$DATABASE$", database).split(";\n")

        # Start a transaction
        self.cursor.execute("START TRANSACTION")
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.cursor.execute(f"USE {database}")

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
                    lc_command.startswith(("create database ", "use"))
                ):
                    self.log.info(f"Skipping command - {lc_command}")
                elif lc_command is None or lc_command == "":
                    self.log.info(lc_command)
                else:
                    self.cursor.execute(lc_command)
            except OperationalError as e:
                self.log.info(f"Command skipped: {command} [{e}]")

        self.conn.commit()

    def col_exists(self, col, table, database):
        self.cursor.execute(
            f"""
        SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table}' AND COLUMN_NAME = '{col}'
      """
        )
        result = self.cursor.fetchone()
        return result is not None
