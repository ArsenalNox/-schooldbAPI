import re
import mysql.connector

con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
        )
cursor = con.cursor()
sql = 'select id, mid, q_num, q_variant, q_text, answ1, answ2, answ3, answ4 from modules_questions'

list_supersc = [
         '⁰',
         '¹',
         '²',
         '³',
         '⁴',
         '⁵',
         '⁶',
         '⁷',
         '⁸',
         '⁹']

cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    if re.search('sup', row[4]) or re.search('sup', row[5]) or re.search('sup', row[6]) or re.search('sup', row[7]) or re.search('sup', row[8]) :

        print(row[0], row[1], row[5], row[6], row[7], row[8])


