import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('memoryos.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def setup_database():
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL UNIQUE,
                                        password text NOT NULL
                                    ); """

    conn = create_connection()
    if conn is not None:
        create_table(conn, sql_create_users_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

def add_user(username, password):
    conn = create_connection()
    sql = ''' INSERT INTO users(username,password)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (username, password))
    conn.commit()
    return cur.lastrowid

def get_user(username):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    rows = cur.fetchall()
    return rows

def get_user_by_id(user_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    rows = cur.fetchall()
    return rows[0] if rows else None

if __name__ == '__main__':
    setup_database()
