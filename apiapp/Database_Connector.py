import mysql.connector as mysql



Connector = mysql.connect(
	user='root',
	password='Hayysoft',
	host='localhost',
	port=3306,
	database='bluguarddb'
)

Cursor = Connector.cursor()
# Cursor.execute('SELECT * FROM tbl_device')
# results = Cursor.fetchall()
# print(results)

