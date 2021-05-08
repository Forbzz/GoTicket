import sqlite3

sql_select_event_info_description = '''
select * from event_info where description = ?;'''



sql_select_personal_info_fio = '''
select fio from personal_info where id = ?;
'''
sql_select_user_role_id = '''
select * from user where role_id = ?;'''
sql_select_role_name = '''
select * from role where name = ?;'''
sql_select_role_id = '''
select * from role where id = ?;'''
sql_select_ticket_user = '''
select * from ticket where user_id = ?;'''
sql_select_ticket_event = '''
select * from ticket where event_id = ?;'''

sql_select_country_id = '''
select * from country where id = ?;'''
sql_select_city_id = '''
select * from city where id = ?;'''
sql_select_street_id = '''
select * from street where id = ?;
'''

sql_select_country_name = '''
select * from country where name = ?;'''
sql_select_city_name = '''
select * from city where name = ?;'''
sql_select_street_name = '''
select * from street where name = ?;
'''

sql_select_address_id = '''
select * from address where id = ?;'''
sql_select_address_country_id = '''
select * from address where country_id = ?;'''
sql_select_address_city_id = '''
select * from address where city_id = ?;'''
sql_select_address_street_id = '''
select * from address where street_id = ?;'''
sql_select_event_all = '''
select * from event;'''
sql_select_event_name = '''
select * from event where name = ?;'''
sql_select_event_info_id = '''
select * from event_info where id = ?;'''
sql_select_event_info_date = '''
select * from event_info where date = ?;'''
sql_select_users_login = '''
select login from user;'''
sql_select_users_all = '''
select personal_info_id from user;'''
sql_select_users_role = '''
select role_id from user where login = ?;'''
sql_select_users_login_pass = '''
select password from user where login = ?;'''
sql_select_event_like_name = '''
SELECT * FROM event WHERE mylower(name) LIKE ?
'''

sql_select_event_from_event_info_id = '''
SELECT * FROM event WHERE event_info_id = ?
'''


sql_select_last_personal_info='''
SELECT  id FROM personal_info ORDER BY id DESC LIMIT 1'''