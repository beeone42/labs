import pymysql

conn = ''
cursor = ''

#
#   db general utils
#

def connect(host, user, passwd, base):
    ''' connection to db '''

    conn = pymysql.connect(host=host,user=user,passwd=passwd, database=base, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    return (conn, cursor)

def query(cursor, query):
    ''' query in db '''

    cursor.execute(query)

def fetchall(cursor, query):
    ''' display db request '''

    cursor.execute(query)
    return (cursor.fetchall())
    
def close(conn):
    ''' close connection '''

    conn.close()

#
#   db firms utils [id,name,representative,phone,mail]
#

def get_all_firms(cursor):
    ''' get all firms details '''
    request_firms = """
SELECT
    firms.id,
    firms.name,
    firms.representative,
    firms.phone,
    firms.mail
FROM firms
    """
    cursor.execute(request_firms)
    return cursor.fetchall()

    
def insert_firm(conn, cursor, name, representative, phone, mail):
    ''' insert new firm in db '''

    request_new_firm = """
INSERT INTO firms
    (name, representative, phone, mail)
VALUES
    (%s, %s, %s, %s)
    """
    cursor.execute(request_new_firm)
    request_last_id = """
SELECT LAST_INSERT_ID() AS id
    """
    cursor.execute(request_last_id)
    conn.commit()
    tmp = cursor.fetchall()
    return tmp[0]['id']

#
#   db users utils [id,login,password,fullname]
#


def get_users(cursor, id = 0, ):
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

