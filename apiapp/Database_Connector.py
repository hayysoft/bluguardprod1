import mysql.connector as mysql


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}


Connector = mysql.connect(**config)

Cursor = Connector.cursor()
# Cursor.execute('SELECT * FROM tbl_device')
# results = Cursor.fetchall()
# print(results)

