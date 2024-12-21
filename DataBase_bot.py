import mysql.connector

def create_database(database_name):
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'auth_plugin': 'mysql_native_password'
    }

    conn = mysql.connector.connect(**config)
    c = conn.cursor()
    c.execute(f"DROP DATABASE IF EXISTS {database_name}")
    c.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f'database "{database_name}" created')


def create_bot_table():
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'Bot_DB',
        'auth_plugin': 'mysql_native_password'}

    conn = mysql.connector.connect(**config)
    c = conn.cursor(dictionary=True)
    c.execute("""CREATE TABLE users (
        cid         BIGINT PRIMARY KEY,
        first_name  VARCHAR(50) NOT NULL,
        username    VARCHAR(100),
        phone       VARCHAR(11),
        join_date   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()
    print('customer table created')


def insert_user_data(cid, first_name, username, phone):
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'Bot_DB',
        'auth_plugin': 'mysql_native_password'
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """INSERT IGNORE INTO users 
                    (cid, first_name, username, phone)
                    VALUES (%s, %s, %s, %s)"""
    cursor.execute(SQL_Query, (cid, first_name, username, phone))
    conn.commit()
    conn.close()
    print(f'user with cid: {cid} inserted into users')


def show_user_info(cid):
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'Bot_DB',
        'auth_plugin': 'mysql_native_password'
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT cid, first_name, username, phone FROM users WHERE cid = %s", (cid,)
        )

    result = cursor.fetchone()
    conn.close()
    if result:
        return result
    else:
        return None
    


if __name__ == '__main__':
    create_database('Bot_DB')
    create_bot_table()
  
