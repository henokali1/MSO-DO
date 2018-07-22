import mysql.connector


# Get all user info by id.
# @returns: A dictionary with all(single user according to id) user info
def get_user_by_id(id):
    cnx = mysql.connector.connect(
        user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')

    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE id=" + str(id))
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r

# Get a single user by email.
def get_user_by_email(email):
    cnx = mysql.connector.connect(
        user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT id, first_name, last_name, email, register_date, airport_id, job_title, department FROM users WHERE email = %s", [email])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r

# Get user psw by email
def user_psw(email):
    cnx = mysql.connector.connect(
        user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor()

    cur.execute("SELECT password FROM users WHERE email = %s", [email])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r[0].encode('utf8')

# Save new data into the db.
def save(sql, data):
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor()
    cur.execute(sql, data)
    cnx.commit()
    cur.close()
    cnx.close()

# All MSO's
def get_all_msos():
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM tsd_mso_form ORDER BY id DESC")
    r = cur.fetchall()
    cnx.commit()
    cur.close()
    cnx.close()
    return r

# Returns one MSO based on the id parameter
def get_mso(id):
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')

    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT * FROM tsd_mso_form WHERE id=" + str(id))
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r

# Get only technicians out of users
def get_technicians():
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor()
    # Get first name and last name of all technicians
    cur.execute("SELECT first_name, last_name FROM users WHERE job_title=%s", ['technician'])
    all_technicians = cur.fetchall()
    cur.close()
    cnx.close()

    technicians = []
    for i in all_technicians:
        technicians.append(i[0].encode('utf8').capitalize() + ' ' + i[1].encode('utf8').capitalize())
    return technicians

# Update MSO 
def update_mso(sql, data):
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor()
    cur.execute(sql, data)
    cnx.commit()
    cur.close()
    cnx.close()

# MSO's pending for TSM approval
def get_tsm_approval_msos():
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM tsd_mso_form WHERE tsm_approval IS NULL ORDER BY id DESC")
    r = cur.fetchall()
    cnx.commit()
    cur.close()
    cnx.close()
    return r

# MSO's pending for TSS(Supervisor) approval
def get_tss_approval_msos():
    cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM tsd_mso_form WHERE supervisor_approval IS NULL ORDER BY id DESC")
    r = cur.fetchall()
    cnx.commit()
    cur.close()
    cnx.close()
    return r

# Delete MSO
def delete_mso(id):
    try:
        cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
        cur = cnx.cursor(dictionary=True)
        sql = "DELETE FROM `maillist_subscription` WHERE id = ?"
        cur.execute(sql, (id,))
        cnx.commit()
        cur.close()
        cnx.close()
        return 1
    except:
        return 0
#print(tsm_tss_approved())