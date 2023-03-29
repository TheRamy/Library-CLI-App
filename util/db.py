from configparser import ConfigParser

import psycopg2


def db_config (filename='db.ini', section='database'):
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




def example_sql ():
    """Just an example by Ramy."""
    try:

        # read connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

    
    
        cur.execute("SELECT * FROM test")
        row = cur.fetchone()
        
        return row


    except (Exception, psycopg2.Error) as error:
        print("error: ", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            # print("PostgreSQL connection is closed")




def example_table ():
    """Just an example by Ramy."""
    try:

        # read connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

    
    
        cur.execute("SELECT * FROM cool_table")
        rows = cur.fetchall()
        
        return rows


    except (Exception, psycopg2.Error) as error:
        print("error: ", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            # print("PostgreSQL connection is closed")

