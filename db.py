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
        print(data)
        sqlite_connection = sqlite3.connect(db_file, timeout=10)
        cursor = sqlite_connection.cursor()
        cursor.execute(insert_script, data)
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    except sqlite3.Error as e:
        print("dasd")
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

def to_lower(_str: str):
    return _str.lower()

def search_record(data: str, db_file, insert_script=None):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        conn.create_function("mylower", 1, to_lower)
        cursor.execute(insert_script, ["%"+data+"%"])
        records = cursor.fetchall()
        print(records)
        return records
    except sqlite3.Error as e:
        print(e)




# def install_function():
#     conn = sqlite3.connect("sql1.db")
#     cursor = conn.cursor()
#     conn.create_function("mylower", 1, to_lower)



