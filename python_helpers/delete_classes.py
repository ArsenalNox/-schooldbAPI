import re
import mysql.connector

con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
        )

cursor = con.cursor()
sql1 = "(select results.id, results.test_uid, students.id as 'stdid', results.a_given, students.name, students.last_name, students.patrn, classes.name from results LEFT JOIN students ON results.student=students.id LEFT JOIN classes ON students.cid=classes.id  where results.sid = 653 and classes.name='6А');"

sql = 'select results.id from results  LEFT JOIN main ON results.sid=main.id LEFT JOIN munipals ON main.mo=munipals.id where main.mo = 653;'

students_to_delete = ['02', '05', '06', '09', '12', '14']

student_ids = []
cursor.execute(sql1)
result = cursor.fetchall()
for row in result:
    student_name = str(row[5])+str(row[6])
    if row[7] == '6А':
        if (student_name in students_to_delete) and not (student_name in student_ids):
            student_ids.append(row[2])

            sql = 'DELETE FROM results WHERE student = {}'.format(row[2])
            cursor.execute(sql)


print(student_ids)
con.commit()
