import sqlite3

sql_create_log_table = """
    CREATE TABLE IF NOT EXISTS log_table(
        id INTEGER PRIMARY KEY autoincrement NOT NULL,
        user_id INTEGER, 
        ticket_id INTEGER,
        event_id INTEGER,
        operation_time DATE,
        operation_action VARCHAR  (128) NOT NULL	
    )
"""
#
sql_trigger_insert_user = """
    CREATE TRIGGER IF NOT EXISTS log_insert_user
    AFTER INSERT
       ON USER
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (NEW.id, -1, -1, DATE(), 'INSERT');
    END;
"""
sql_trigger_update_user = """
    CREATE TRIGGER IF NOT EXISTS log_update_user
    AFTER UPDATE 
       ON USER
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (OLD.id, -1, -1, DATE(), 'UPDATE');
    END;
"""
sql_trigger_delete_user = """
    CREATE TRIGGER IF NOT EXISTS log_delete_user
    AFTER DELETE
       ON USER
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (OLD.id, -1, -1, DATE(), 'DELETE');
    END;
"""
#
sql_trigger_insert_ticket = """
    CREATE TRIGGER IF NOT EXISTS log_insert_ticket
    AFTER INSERT
       ON TICKET
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (-1, NEW.id, -1, DATE(), 'INSERT');
    END;
"""
sql_trigger_update_ticket = """
    CREATE  TRIGGER IF NOT EXISTS log_update_ticket
    AFTER UPDATE 
       ON TICKET
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (-1, OLD.id, -1, DATE(), 'UPDATE');
    END;
"""
sql_trigger_delete_ticket = """
    CREATE TRIGGER IF NOT EXISTS log_delete_ticket
    AFTER DELETE
       ON TICKET
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (-1, OLD.id, -1, DATE(), 'DELETE');
    END;
"""
#
sql_trigger_insert_event = """
    CREATE TRIGGER IF NOT EXISTS log_insert_event
    AFTER INSERT
       ON EVENT
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (-1, -1, NEW.id, DATE(), 'INSERT');
    END;
"""
sql_trigger_update_event = """
    CREATE  TRIGGER IF NOT EXISTS log_update_event
    AFTER UPDATE 
       ON EVENT
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (-1, -1, OLD.id, DATE(), 'UPDATE');
    END;
"""
sql_trigger_delete_event = """
    CREATE TRIGGER IF NOT EXISTS log_delete_event
    AFTER DELETE
       ON EVENT
    BEGIN
        INSERT INTO log_table(user_id, ticket_id, event_id, operation_time, operation_action)
        VALUES (-1, -1, OLD.id, DATE(), 'DELETE');
    END;
"""
#
sql_select_logg_info = """
    SELECT user_id, ticket_id, event_id, operation_time, operation_action FROM log_table
"""


#

def sql_execute(db, sql):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()

        res = list()
        for row in c.execute(sql):
            res.append(row)

        c.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
    return conn




import sqlite3
sql_drop1 = """
    DROP TABLE log_table;
"""
sql_drop2 = """
    DROP TRIGGER log_insert_user;
"""
sql_drop3 = """
    DROP TRIGGER log_update_user;
"""
sql_drop4 = """
    DROP TRIGGER log_delete_user;
"""
sql_drop5 = """
    DROP TRIGGER log_insert_ticket;
"""
sql_drop6 = """
    DROP TRIGGER log_update_ticket;
"""
sql_drop7 = """
    DROP TRIGGER log_delete_ticket;
"""
sql_drop8 = """
    DROP TRIGGER log_insert_event;
"""
sql_drop9 = """
    DROP TRIGGER log_update_event;
"""
sql_drop10 = """
    DROP TRIGGER log_delete_event;
"""
db = "sql1.db"

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


# conn = create_connection(db)
# if conn is not None:
#     create_table(conn, sql_drop1)
#     create_table(conn, sql_drop2)
#     create_table(conn, sql_drop3)
#     create_table(conn, sql_drop4)
#     create_table(conn, sql_drop5)
#     create_table(conn, sql_drop6)
#     create_table(conn, sql_drop7)
#     create_table(conn, sql_drop8)
#     create_table(conn, sql_drop9)
#     create_table(conn, sql_drop10)
#
#     create_table(conn, sql_create_log_table)
#     create_table(conn, sql_trigger_insert_user)
#     create_table(conn, sql_trigger_update_user)
#     create_table(conn, sql_trigger_delete_user)
#
#     create_table(conn, sql_trigger_insert_ticket)
#     create_table(conn, sql_trigger_update_ticket)
#     create_table(conn, sql_trigger_delete_ticket)
#
#     create_table(conn, sql_trigger_insert_event)
#     create_table(conn, sql_trigger_update_event)
#     create_table(conn, sql_trigger_delete_event)
#
#     print('gc!')
# else:
#     print("Error! cannot the databese connection.")

