import mysql.connector

sqlCon = mysql.connector.connect(
        user='root',
        host='localhost',
        database='schools',
        password='root'
        )

cursor = sqlCon.cursor()

print('Connected')

