import sqlite3


def execute_single_record(data, db_file, insert_script):
    try:
        sqlite_connection = sqlite3.connect(db_file, timeout=10)
        cursor = sqlite_connection.cursor()
        cursor.execute(insert_script, (data,))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    except sqlite3.Error as e:
        print(e)


# вставка нескольких переменных в одну таблицу
def execute_multiple_record(data, db_file, insert_script):
    try:
        sqlite_connection = sqlite3.connect(db_file, timeout=10)
        cursor = sqlite_connection.cursor()
        cursor.execute(insert_script, data)
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    except sqlite3.Error as e:
        print(e)


# поиск записей в таблице
def read_table(db_file, selector_script, search_name):
    try:
        sqlite_connection = sqlite3.connect(db_file)
        cursor = sqlite_connection.cursor()
        if search_name is None:
            cursor.execute(selector_script)
        else:
            cursor.execute(selector_script, (search_name,))
        records = cursor.fetchall()
        print(records)
        cursor.close()
        sqlite_connection.close()
        return records
    except sqlite3.Error as e:
        print(e)