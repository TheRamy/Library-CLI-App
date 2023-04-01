from configparser import ConfigParser
from rich.table import Table

import psycopg2


def db_config(filename='db.ini', section='database'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


def sql_select(sql, fetchType='fetchall', fetchmanyN=5):
    """You can use this to query the database with fetchall,
      fetchone or fetchmany, and returns the result.
       if fetchmany is used, it will fetch 5 by default. ~ramy """

    try:

        # read connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

        cur.execute(sql)

        if fetchType == 'fetchall':

            rows = cur.fetchall()
            return rows

        elif fetchType == "fetchone":

            rows = cur.fetchone()
            return rows
        elif fetchType == "fetchmany":

            rows = cur.fetchmany(fetchmanyN)
            return rows

    except (Exception, psycopg2.Error) as error:
        print("error: ", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            # print("PostgreSQL connection is closed")


def sql_insert(sql):
    """You can use this to run insert SQL. ~ramy """

    try:

        # read connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

        cur.execute(sql)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("error: ", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            # print("PostgreSQL connection is closed")


def sql_update(sql):
    """You can use this to run update SQL. ~ramy """

    try:

        # read connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

        cur.execute(sql)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("error: ", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            # print("PostgreSQL connection is closed")

