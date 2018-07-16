import mysql.connector


def get_user_info(id):
	cnx = mysql.connector.connect(user='root',
  								password='@tmsqe!1321',
  								host='127.0.0.1',
                                database='MSO')

	cur = cnx.cursor(dictionary=True)

	query = ("SELECT * FROM users")
	cur.execute("SELECT * FROM users WHERE id=" + str(id))
	r = cur.fetchone()
	cur.close()
	cnx.close()
	return r

def register_user(sql, data):
	cnx = mysql.connector.connect(user='root',
  								password='@tmsqe!1321',
  								host='127.0.0.1',
                                database='MSO')
	cur = cnx.cursor()
	cur.execute(sql, data)
	cnx.commit()
	cur.close()
	cnx.close()
