import re
import mysql.connector

con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
        )

cursor = con.cursor()

sbj = 2
school_id = 830
class_name = '9Б'

#Выбирает результаты конкретного класса школы 
sql1 = """
    select 
        results.id, 
        results.test_uid,
        students.id as 'stdid',
        results.a_given,
        students.name, 
        students.last_name,
        students.patrn, 
        classes.name 
    from results 
    LEFT JOIN students ON results.student=students.id 
    LEFT JOIN classes ON students.cid=classes.id  
    where results.sid = {} and classes.name='{}';
    """.format(school_id, class_name)

#Выбират ВСЕ классы конкретной параллели 
sql_all = """
    select 
        results.id, 
        results.test_uid, 
        students.id as 'stdid', 
        results.a_given, 
        students.name, 
        students.last_name, 
        students.patrn, 
        classes.name 
    from results 
    LEFT JOIN students ON results.student=students.id 
    LEFT JOIN classes ON students.cid=classes.id  
    where 
        results.sid = {} 
        and classes.year=8
    """.format(school_id)
    
#Выбирает классы школы
sql3 = """
    select 
        results.id, 
        results.test_uid, 
        students.id as 'stdid', 
        results.a_given, 
        students.name, 
        students.last_name, 
        students.patrn, 
        classes.name,
        subjects.name,
        results.sid
    from results 
    LEFT JOIN students ON results.student=students.id 
    LEFT JOIN classes ON students.cid=classes.id  
    LEFT JOIN modules ON results.mid=modules.id
    LEFT JOIN subjects ON modules.subject=subjects.id
    where 
        results.sid = {}
        and subjects.id = {}
    """.format(school_id, sbj)

sql = """
    select 
        results.id 
    from results  
    LEFT JOIN main ON results.sid=main.id 
    LEFT JOIN munipals ON main.mo=munipals.id 
    where main.id = 1679;'
    """

sql = """
    select 
        results.id 
    from results  
    LEFT JOIN main ON results.sid=main.id 
    LEFT JOIN munipals ON main.mo=munipals.id 
    where main.id = 1679;"""

type_d = 1

active_sql = sql3

if type_d == 1:
    students_to_delete = [
            '03',
            ]

    student_ids = []

    print(active_sql)

    cursor.execute(active_sql)
    result = cursor.fetchall()
    for row in result:
        student_name = str(row[5])+str(row[6])
        if row[7] == class_name:
        #if '9' in row[7]:
            print(row)
            if (student_name in students_to_delete) and not (student_name in student_ids):
                student_ids.append(row[2])

            sql = 'DELETE FROM results WHERE id = {}'.format(row[0])
            print(sql)
            cursor.execute(sql)

    print(student_ids)
else:
    print('in progres...')
    cursor.execute(active_sql)
    print(active_sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
        sql = 'DELETE FROM results WHERE id = {}'.format(row[0])
        print(sql)
        cursor.execute(sql)


con.commit()
print('done')
