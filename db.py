import pymysql

conn = ''
cursor = ''

def connect(host, user, passwd, base):
    conn = pymysql.connect(host=host,user=user,passwd=passwd, database=base, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    return (conn, cursor)

def query(cursor, query):
    cursor.execute(query)

def fetchall(cursor, query):
    cursor.execute(query)
    return (cursor.fetchall())
    
def close(conn):
    conn.close()

def get_users(cursor, id = 0, login = ''):
    q = """
SELECT
    users.id,
    users.login,
    users.password,
    users.fullname
FROM users
    """
    if (id > 0):
        q = q + " WHERE users.id = %s"
        cursor.execute(q, (id))
        return (cursor.fetchall())
    else:
        if (login != ''):
            q = q + " WHERE users.login = %s"
            cursor.execute(q, (login))
            return (cursor.fetchall())
    return (fetchall(cursor, q))

