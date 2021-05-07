# Test
import sqlite3
from create_sql import *

#script = " CREATE TABLE users (id INTEGER PRIMARY KEY, name text, password text, role int) "

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def execute_multiple_records(recordList, db_file, insert_script):
    try:
        sqlite_connection = sqlite3.connect(db_file)
        cursor = sqlite_connection.cursor()
        cursor.executemany(insert_script, recordList)
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    except sqlite3.Error as e:
        print(e)


# conn = sqlite3.connect("sql2.db")
# cur = conn.cursor()

db = "sql2.db"

# record_list = [("Belarus",),
#                ("Russia",) ,
#                ("China",)  ,
#                ("USA",)     ]

#
conn =create_connection(db)
if conn is not None:
# execute_multiple_records(delete_list, db, sql_delete_country)
    create_table(conn, sql_create_country)
    create_table(conn, sql_create_city)
    create_table(conn, sql_create_street)
    create_table(conn, sql_create_address)
    create_table(conn, sql_create_personal_info)
    create_table(conn, sql_create_role)
    create_table(conn, sql_create_ticket)
    create_table(conn, sql_create_event_info)
    create_table(conn, sql_create_user)
    create_table(conn, sql_create_event)

#else:
 #  # print("Error! cannot the databese connection.")
