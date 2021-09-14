import mysql.connector

sqlConnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='schools'
        )

cursor = sqlConnection.cursor()
sql = "SELECT * FROM `main`"

cursor.execute(sql)
result = cursor.fetchall()

for row in result:
    current_mo = row[3]
    
    get_mo_id_sql = f"SELECT id FROM munipals WHERE name = '{current_mo}'"
    cursor.execute(get_mo_id_sql)
    mo_id_result = cursor.fetchone()
    print(mo_id_result[0])

    update_sql = f"UPDATE `main` SET mo='{mo_id_result[0]}' WHERE mo = '{current_mo}'"
    cursor.execute(update_sql)
    print(current_mo)

sqlConnection.commit()
