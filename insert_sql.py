import sqlite3

sql_insert_country = """
    INSERT INTO country(name) VALUES (?);
"""

sql_insert_street = """
    INSERT INTO street (name) VALUES (?);
"""

sql_insert_city = """
    INSERT INTO city (name) VALUES (?);
"""

sql_insert_address = """
    INSERT INTO address (country_id, city_id, street_id) VALUES (?,?,?);
"""
sql_insert_ticket = """
    INSERT INTO ticket (price, date, user_id, event_id) VALUES (?,?,?,?);
"""

sql_insert_event = """
    INSERT INTO event (name, ticket_amount, event_info_id, address_id) VALUES (?,?,?,?);
"""

sql_insert_personal_info = """
    INSERT INTO personal_info (fio, age) VALUES (?,?);
"""
sql_insert_role = """
    INSERT INTO role (name, role_id) VALUES (?,?);
"""

sql_insert_event_info = """
    INSERT INTO event_info (description, duration, date) VALUES (?,?, ?);
"""

sql_insert_user = """
    INSERT INTO user (password, login, registration_date, balance, role_id, personal_info_id) VALUES (?, ?,?, ?,?,?);
"""


