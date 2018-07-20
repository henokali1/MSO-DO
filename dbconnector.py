import mysql.connector


# Get all user info by id.
# @returns: A dictionary with all(single user according to id) user info
def get_user_by_id(id):
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')

    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE id=" + str(id))
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r


# Get a single user by email.
def get_user_by_email(email):
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE email = %s", [ email])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r



# Register new user into the DB.
def register_user(sql, data):
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor()
    cur.execute(sql, data)
    cnx.commit()
    cur.close()
    cnx.close()
