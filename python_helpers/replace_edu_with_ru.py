import re
import mysql.connector

con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
        )
cursor = con.cursor()
sql = 'select id, mid, q_num, q_variant, q_image from modules_questions'

cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    if not row[4] == None:
        if re.search('okeit', row[4]):
            new_img_path = re.sub('okeit', 'oksei', row[4])
            print(new_img_path)
            sql = "UPDATE modules_questions SET q_image = '{}' WHERE id = {}".format(new_img_path, row[0])
            print(sql)
            cursor.execute(sql)
con.commit()
