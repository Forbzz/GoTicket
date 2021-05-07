sql_update_country = """
    UPDATE country 
    SET name = ?
    WHERE id = ?;
"""

sql_update_city = """
    UPDATE city 
    SET name = ?
    WHERE id = ?;
"""
sql_update_street = """
    UPDATE street 
    SET name = ?
    WHERE id = ?;
"""

sql_update_address = """
    UPDATE address
    SET country_id = ?,
    city_id = ?,
    street_id = ?
    WHERE ID = ?;
"""
sql_update_role = """
    UPDATE role SET
    name = ?,
     role_id = ?
      WHERE ID = ?;
"""
sql_update_event = """
    UPDATE event 
    SET
    ticket_amount = ?, 
    event_info_id = ?, 
    address_id = ?
    WHERE ID = ?;
"""
sql_update_ticket = """
    UPDATE ticket 
    SET price = ?, 
    date = ?, 
    user_id = ?, 
    event_id = ?
    WHERE id = ?;
"""
sql_update_user = """
    UPDATE user SET
    balance = ?, 
    password = ?, 
    personal_info_id = ?, 
    role_id = ?
    WHERE id = ?;
"""
sql_update_personal_info = """
    UPDATE personal_info
    SET 
    fio = ?, 
    age = ?
    WHERE id = ?;
"""
sql_update_event_info = """
    UPDATE event_info
    SET
    description = ?, 
    duration = ?
    WHERE id = ?; 
    """

sql_update_event_tickets = """
    UPDATE event SET
    ticket_amount = ?
    WHERE id = ?;
"""