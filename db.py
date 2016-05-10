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

def get_deals(cursor, id = 0):
    q = """
SELECT
    deals.id,
    deals.bdcid,
    deals.state,
    deals.description,
    deals.creator AS creator_id,
    users1.fullname AS creator_name,
    deals.validator AS validator_id,
    users2.fullname AS validator_name,
    deals.site AS site_id,
    sites.name AS site_name,
    sites.pic AS site_pic,
    sites.currency
FROM deals
LEFT JOIN users AS users1 ON users1.id = deals.creator
LEFT JOIN users AS users2 ON users2.id = deals.validator
LEFT JOIN sites ON sites.id = deals.site
    """
    if (id > 0):
        q = q + " WHERE deals.id = '" + str(id) + "'"
    return (fetchall(cursor, q))

def insert_deal(conn, cursor, bdcid, description, site_id, creator_id, validator_id, state):
    q = """
INSERT INTO deals (bdcid, description, site, creator, validator, state) VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(q, (bdcid, description, site_id, creator_id, validator_id, state))
    q = "SELECT LAST_INSERT_ID() AS id"
    cursor.execute(q)
    conn.commit()
    tmp = cursor.fetchall()
    return tmp[0]['id']

def update_deal(conn, cursor, id, bdcid, description, site_id, creator_id, validator_id, state):
    if (id == 0):
        return (insert_deal(conn, cursor, bdcid, description, site_id, creator_id, validator_id, state))
    q = """
UPDATE deals SET
    bdcid = %s,
    description = %s,
    site = %s,
    creator = %s,
    validator = %s,
    state = %s
WHERE
    id = %s
    """
    cursor.execute(q, (bdcid, description, site_id, creator_id, validator_id, state, id))
    conn.commit()
    return id

def get_contractors(cursor, id = 0):
    q = """
SELECT
    contractors.id,
    contractors.enterprise,
    contractors.contact_name,
    contractors.contact_tel,
    contractors.contact_mail
FROM contractors
    """
    if (id > 0):
        q = q + " WHERE contractors.id = '" + str(id) + "'"
    return (fetchall(cursor, q))

def insert_contractor(conn, cursor, enterprise, contact_name, contact_tel, contact_mail):
    q = """
INSERT INTO contractors (enterprise, contact_name, contact_tel, contact_mail) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(q, (enterprise, contact_name, contact_tel, contact_mail))
    q = "SELECT LAST_INSERT_ID() AS id"
    cursor.execute(q)
    conn.commit()
    tmp = cursor.fetchall()
    return tmp[0]['id']

def update_contractor(conn, cursor, id, enterprise, contact_name, contact_tel, contact_mail):
    if (id == 0):
        return (insert_contractor(conn, cursor, enterprise, contact_name, contact_tel, contact_mail))
    q = """
UPDATE contractors SET
    enterprise = %s,
    contact_name = %s,
    contact_tel = %s,
    contact_mail = %s
WHERE
    id = %s
    """
    cursor.execute(q, (enterprise, contact_name, contact_tel, contact_mail, id))
    conn.commit()
    return id

def get_devis(cursor, did = 0, id = 0):
    q = """
SELECT
    devis.id,
    devis.deal_id,
    devis.contractor_id,
    devis.amount,
    DATE_FORMAT(devis.date_received, '%Y-%m-%d %H:%i') AS d_received,
    DATE_FORMAT(devis.date_proceed, '%Y-%m-%d %H:%i') AS d_proceed,
    devis.state,
    deals.bdcid,
    deals.description,
    sites.name AS site_name,
    sites.id AS site_id,
    sites.currency,
    contractors.id AS contractor_id,
    contractors.enterprise AS issuer,
    contractors.contact_name
FROM devis
LEFT JOIN deals ON deals.id = devis.deal_id
LEFT JOIN sites ON sites.id = deals.site
LEFT JOIN contractors ON contractors.id = devis.contractor_id
    """
    if (did > 0):
        q = q + " WHERE devis.deal_id = '" + str(did) + "'"
        if (id > 0):
            q = q + " AND devis.id = '" + str(id) + "'"
    else:
        if (id > 0):
            q = q + " WHERE devis.id = '" + str(id) + "'"
    return (fetchall(cursor, q))

def insert_devis(conn, cursor, deal_id, contractor_id, amount, date_received, state):
    q = """
INSERT INTO devis (deal_id, contractor_id, amount, date_received, state) VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(q, (deal_id, contractor_id, amount, date_received, state))
    q = "SELECT LAST_INSERT_ID() AS id"
    cursor.execute(q)
    conn.commit()
    tmp = cursor.fetchall()
    return tmp[0]['id']

def update_devis(conn, cursor, id, deal_id, contractor_id, amount, date_received, state):
    if (id == 0):
        return (insert_devis(conn, cursor, deal_id, contractor_id, amount, date_received, state))
    q = """
UPDATE devis SET
    deal_id = %s,
    contractor_id = %s,
    amount = %s,
    date_received = %s,
    state = %s
WHERE
    id = %s
    """
    cursor.execute(q, (deal_id, contractor_id, amount, date_received, state, id))
    conn.commit()
    return id


def get_docs(cursor, id = 0, deal_id = 0, devis_id = 0, bdc_id = 0, invoice_id = 0):
    q = """
SELECT
    docs.id,
    deals.bdcid,
    deals.description,
    docs.deal_id,
    docs.devis_id,
    docs.fname,
    DATE_FORMAT(docs.date_received, '%Y-%m-%d %H:%i') AS d_received,
    docs.doc_type,
    sites.name AS site_name,
    contractors.enterprise AS contractor,
    contractors.contact_name AS contractor_contact
FROM docs
LEFT JOIN deals ON deals.id = docs.deal_id
LEFT JOIN devis ON devis.id = docs.devis_id
LEFT JOIN sites ON sites.id = deals.site
LEFT JOIN contractors ON contractors.id = devis.contractor_id
    """
    if (id > 0):
        q = q + " WHERE docs.id = '" + str(id) + "'"
    else:
        if (deal_id > 0):
            q = q + " WHERE docs.deal_id = '" + str(deal_id) + "'"
            if (devis_id > 0):
                q = q + " AND docs.devis_id = '" + str(devis_id) + "'"
            if (bdc_id > 0):
                q = q + " AND docs.bdc_id = '" + str(bdc_id) + "'"
            if (invoice_id > 0):
                q = q + " AND docs.invoice_id = '" + str(invoice_id) + "'"
    return (fetchall(cursor, q))


def insert_doc(conn, cursor, deal_id, devis_id, bdc_id, invoice_id, contractor_id, fname, doc_type):
    q = """
INSERT INTO devis (deal_id, devis_id, bdc_id, invoice_id, contractor_id, fname, date_received, doc_type) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
    """
    cursor.execute(q, (deal_id, devis_id, bdc_id, invoice_id, contractor_id, fname, doc_type))
    q = "SELECT LAST_INSERT_ID() AS id"
    cursor.execute(q)
    conn.commit()
    tmp = cursor.fetchall()
    return tmp[0]['id']

def get_users(cursor, id = 0):
    q = """
SELECT
    users.id,
    users.login,
    users.fullname
FROM users
    """
    if (id > 0):
        q = q + " WHERE users.id = '" + str(id) + "'"
    return (fetchall(cursor, q))

def get_sites(cursor, id = 0):
    q = """
SELECT
    sites.id,
    sites.name,
    sites.pic,
    sites.currency
FROM sites
    """
    if (id > 0):
        q = q + " WHERE sites.id = '" + str(id) + "'"
    return (fetchall(cursor, q))

def get_deal_states(cursor):
    q = "SHOW COLUMNS FROM deals WHERE Field = 'state';"
    cursor.execute(q)
    tmp = cursor.fetchall()[0]['Type']
    return (tmp.split('(', 1)[1].split(')', 1)[0].replace("'", "").split(','))

def get_devis_states(cursor):
    q = "SHOW COLUMNS FROM devis WHERE Field = 'state';"
    cursor.execute(q)
    tmp = cursor.fetchall()[0]['Type']
    return (tmp.split('(', 1)[1].split(')', 1)[0].replace("'", "").split(','))


def find_next_bdcid(cursor, site_id):
    q = """
SELECT
    COUNT(deals.id) AS m
FROM deals
    WHERE deals.site = %s
    """
    cursor.execute(q, [site_id])
    res = cursor.fetchall()
    id = res[0]['m'] + 1
    return ('42.' + str(site_id) + '.' + str(id / 256) + '.' + str(id % 256))
