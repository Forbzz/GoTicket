import sqlite3

sql_create_personal_info = """
    CREATE TABLE IF NOT EXISTS personal_info(
    id integer primary key autoincrement not null,
    fio varchar(128) not null,
    age integer not null
);"""

sql_create_user = """
    CREATE TABLE IF NOT EXISTS USER(
    id integer primary key autoincrement not null,
    password VARCHAR(200) not null,
    login VARCHAR(200) not null,
    registration_date date not null,
    balance integer,
    role_id integer,
    personal_info_id integer,
    foreign key (role_id) references role(id), 
    foreign key (personal_info_id) references personal_info(id) ON DELETE CASCADE
    );
"""

sql_create_role = """
    CREATE TABLE IF NOT EXISTS role(
    id integer primary key autoincrement not null,
    name varchar(128),
    role_id integer,
    foreign key (role_id) references role(id) 
    );"""

sql_create_country = """
    CREATE TABLE IF NOT EXISTS country(
    id integer primary key autoincrement not null,
    name varchar(128)
    );"""

sql_create_city = """
    CREATE TABLE IF NOT EXISTS city(
    id integer primary key autoincrement not null,
    name varchar(128)
    );"""

sql_create_street = """
    CREATE TABLE IF NOT EXISTS street(
    id integer primary key autoincrement not null,
    name varchar(128)
    );"""

sql_create_address = """
CREATE TABLE IF NOT EXISTS address(
    id integer primary key autoincrement not null,
    country_id tinyint,
    city_id integer,
    street_id integer,
    foreign key (country_id) references country(id),
    foreign key (city_id) references city(id),
    foreign key (street_id) references street(id)
    );
"""

sql_create_ticket = """
    CREATE TABLE IF NOT EXISTS ticket(
    id integer primary key autoincrement not null,
    price integer not null,
    date date not null,
    user_id integer,
    event_id integer,
    foreign key (user_id) references user(id),
    foreign key (event_id) references event(id)
    );
"""

sql_create_event_info = """
    CREATE TABLE IF NOT EXISTS event_info(
    id integer primary key autoincrement not null,
    date date not null,
    duration smallint not null,
    description varchar(300)
    );
"""

sql_create_event = """
    CREATE TABLE IF NOT EXISTS event(
    id integer primary key autoincrement not null,
    name varchar(100) not null,
    ticket_amount smallint,
    event_info_id integer,
    address_id integer,
    foreign key (event_info_id) references event_info(id) ON DELETE CASCADE,
    foreign key (address_id) references address(id)
);
"""

db = r"sql1.db"

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


conn = create_connection(db)
if conn is not None:
    create_table(conn, """
    CREATE TABLE IF NOT EXISTS log_table(
        id INTEGER PRIMARY KEY autoincrement NOT NULL,
        user_id INTEGER, 
        ticket_id INTEGER,
        event_id INTEGER,
        operation_time DATE,
        operation_action VARCHAR  (128) NOT NULL	
    )
""")
    print('gc!')
else:
    print("Error! cannot the databese connection.")