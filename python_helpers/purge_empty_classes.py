import mysql.connector

sqlConnection = mysql.connector.connect(
    host='192.168.145.114',
    user='root',
    password='P@ssw0rd',
    database='schools'
)

cursor = sqlConnection.cursor()
sql = 'SELECT * FROM classes WHERE id = 25679 ORDER BY id ASC'
cursor.execute(sql)
result = cursor.fetchall()
deleted_count = 0
for row in result:
    print(f'Searching for class {row[0]}...')
    sql = f"SELECT * FROM `students` WHERE cid = {row[0]}"
    cursor.execute(sql)
    result2 = cursor.fetchall()
    if len(result2) == 0:
        print(f'EMPTY CLASS {row[0]} ')
        deleted_count+=1
        sql = f"DELETE FROM classes WHERE id = {row[0]}"
        cursor.execute(sql)
    else:
        print('Not empty')
print(f'DELETED COUNT: {deleted_count}')