import re
from typing import runtime_checkable
import mysql.connector
from mysql.connector.cursor import RE_SQL_COMMENT

con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
        )

cursor = con.cursor()
school_id = 619
class_name = '9А'
sql1 = "(select results.id, results.test_uid, students.id as 'stdid', results.a_given, students.name, students.last_name, students.patrn, classes.name from results LEFT JOIN students ON results.student=students.id LEFT JOIN classes ON students.cid=classes.id  where results.sid = {} and classes.name='{}');".format(school_id, class_name)
print(sql1)

sql = 'select results.id from results  LEFT JOIN main ON results.sid=main.id LEFT JOIN munipals ON main.mo=munipals.id where main.mo = 653;'
type_d = 2

if type_d == 1:
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
else:
    cursor.execute(sql1)
    result = cursor.fetchall()
    for row in result:
        sql = 'DELETE FROM results WHERE id = {}'.format(row[0])
        print(sql)
        cursor.execute(sql)
input()