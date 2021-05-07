import sqlite3

sql_delete_country = """
    DELETE FROM country WHERE id = ?
"""

sql_delete_country = """
    DELETE FROM country WHERE id = ?
"""

sql_delete_country = """
    DELETE FROM country WHERE id = ?
"""

sql_delete_city = """
    DELETE FROM city WHERE id = ?
"""

sql_delete_street = """
    DELETE FROM street WHERE id = ?
"""

sql_delete_address = """
    DELETE FROM address WHERE id = ?
"""

sql_delete_role = """
    DELETE FROM role WHERE id = ?
"""

sql_delete_event = """
    DELETE FROM role WHERE id = ?
"""

sql_delete_ticket = """
    DELETE FROM ticket WHERE id = ?
"""

sql_delete_user = """
    DELETE FROM ticket WHERE id = ?
"""

db = r"sql1.db"


# def execute_multiple_records(recordList, db_file, insert_script):
#     try:
#         sqlite_connection = sqlite3.connect(db_file)
#         cursor = sqlite_connection.cursor()
#         cursor.executemany(insert_script, recordList)
#         sqlite_connection.commit()
#         cursor.close()
#         sqlite_connection.close()
#     except sqlite3.Error as e:
#         print(e)
# delete_list = [(1,)]
# execute_multiple_records(delete_list, db, sql_delete_country)