import datetime
from configparser import ConfigParser
from logging import Logger
from typing import Tuple
import pdb
import pymysql
import sqlparse
from pymysql.cursors import DictCursor

def get_full_path(path):
    """
    Return the absolute path based on the supplied fragment
    :param path: A relative path fragment. If this is already the absolute path, just return it.
    :return: The absolute path.
    """
    full_path: Path = Path(path).resolve(strict=False)
    return str(full_path)

class SqlDb:
    """
    Wrapper and helper methods for MySQL commands
    """

    def __init__(self, config: ConfigParser, logger: Logger, suppress_log: bool = False):
        self.config = config
        self.logger = logger
        self.conn = pymysql.connect(
                **self.get_db_config(),
                cursorclass=DictCursor,
                local_infile=True)
        if not suppress_log:
            self.logger.info(f"Connected to MySQL database server at {self.config['host']} "
                         f"as {self.config['user']}")

    def get_db_config(self):
        """
        Get or prompt user for MySQL connection config
        :return: MySQL connection config
        """
        if not (self.config.db_user
                and self.config.db_host
                and self.config.db_password):
            host = input("MySQL host name (eg: localhost):\n>> ")
            user = input("MySQL user name (eg: root):\n>> ")
            password = input("MySQL password:\n>> ")
            self.config = {
                'host': host,
                'user': user,
                'password': password
            }
        else:
            self.config = {
                'host': self.config.db_host,
                'user': self.config.db_user,
                'password': self.config.db_password
            }
        return self.config

    def load_sql_file_into_db(self, sql_path: str):
        """
        Execute all the statements in a .sql file
        :param sql_path: the path to the .sql file
        """
        cursor = self.conn.cursor()
        try:
            with open(sql_path, "r", encoding="utf-8") as f:
                stmts = sqlparse.format(f.read(), None, strip_comments=True)
                raw_statements = sqlparse.split(stmts)
                for statement in raw_statements:
                    if statement == ';':
                        continue
                    if statement:
                        cursor.execute(statement)
                self.conn.commit()
        finally:
            cursor.close()

    def read_table_to_dict(self, database: str, tablename: str):
        """
        Read a table from MySQL and return its contents as a Python dict
        :param database: The name of the database containing the table.
        :param tablename: The name of the table to read.
        :return: The contents of the table as a dict.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {database}.{tablename};")
        return cursor.fetchall()

    def read_table_with_total(self, database: str, table_name: str):
        """
        Convenience method for use in the progress method. Read the contents of a table and return them with the total count of rows.
        :param sql: The instance of SqlDb to use to connect to the database.
        :param database: The name of the database containing the table.
        :param table_name: The name of the table.
        :return: The contents of the table, a starter value of 0, and the total row count.
        """
        old_table = self.read_table_to_dict(database, table_name)
        current = 0
        total = len(old_table)
        return old_table, current, total

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

    def execute(self, database: str, statement: str, params: Tuple=None):
        """
        Execute a statement without fetching the results.
        :param database: The database to run the statement against.
        :param statement: The statement to execute.
        :param params: The parameters to the statement.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"USE {database}")
        cursor.execute(statement, params)
        self.conn.commit()

    def drop_database(self, database: str):
        cursor = self.conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {database};")
        self.conn.commit()

    def dump_database(self, database: str, destination_filepath: str):
        """
        Write the contents of an entire database to file.
        :param database: The name of the database to dump.
        :param destination_filepath: The full path to the destination file.
        :return: The full path to the written file.
        """
        cursor = self.conn.cursor()
        f = open(get_full_path(destination_filepath), "w", encoding="UTF-8")
        f.write(f"DROP DATABASE IF EXISTS {database};\n")
        f.write(f"CREATE DATABASE {database};\n")
        f.write(f"USE {database};\n\n")
        cursor.execute(f"USE {database}")
        cursor.execute("SHOW TABLES")
        tables = []
        for table in cursor.fetchall():
            tables.append(table[f'Tables_in_{database}'])

        for table in tables:
            f.writelines(f"\nDROP TABLE IF EXISTS {database}.`{str(table)}`;\n")

            cursor.execute(f"SHOW CREATE TABLE {database}.`{str(table)}`;")
            f.writelines([str(cursor.fetchone()['Create Table']), ";\n"])

            cursor.execute(f"SHOW COLUMNS FROM {str(table)};")
            column_definitions = cursor.fetchall()
            column_names = ", ".join([f"`{definition['Field']}`" for definition in column_definitions])

            cursor.execute(f"SELECT * FROM {database}.`{str(table)}`;")
            counter = 0
            row_group = []
            for row in cursor.fetchall():
                if counter == 0 or counter % 500 == 0:
                    if row_group:
                        f.write(",\n".join(row_group) + ";\n")
                    row_group = []
                    f.write(f"INSERT INTO {database}.`{str(table)}` ({column_names}) VALUES \n")
                field_arr = []
                for field in row:
                    if type(row[field]) == str or type(row[field]) == datetime.datetime:
                        field_arr.append(self.conn.escape(row[field]))
                    elif row[field] is None:
                        field_arr.append("NULL")
                    else:
                        field_arr.append(str(row[field]))
                fields = ",".join(field_arr)
                row_group.append(f"({fields})")
                counter = counter + 1
            f.write(",\n".join(row_group))
            f.write(";\n")
        f.close()
        return destination_filepath

    def get_another_connection(self):
        """
        Returns another connection to the database, with the same config
        """
        return SqlDb(self.config, self.logger, True)

    def ensure_local_infile(self):
        """
        Checks if local_infile is enabled, and if not enables it
        """
        local_infile_query = r"SELECT @@global.local_infile"
        cursor = self.conn.cursor()
        cursor.execute(local_infile_query)
        if not cursor.fetchone()[r"@@global.local_infile"]:
            self.logger.info("Enabling local_infile inserts for faster processing")
            cursor.execute("SET GLOBAL local_infile=1")
        cursor.close()


    def __del__(self):
        """
        Destructor to disconnect from the database
        """
        try:
            self.conn.close()
        except:
            pass

