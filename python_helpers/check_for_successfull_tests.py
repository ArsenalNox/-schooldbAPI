import mysql.connector
from mysql.connector.utils import read_string

def search_for_school_id(search_string):
    global sqlCon
    cur = sqlCon.cursor()

    sql = f""" 
        SELECT 
            main.id, 
            name_full, 
            name_short,
            munipals.name 
        FROM main 
        LEFT JOIN munipals ON main.mo=munipals.id
        WHERE name_full LIKE "%{search_string}%"
    """
    cur.execute(sql)
    result = cur.fetchall()
    if cur.rowcount == 0:
        print('Ничего не найденно')

    for row in result:
        print(f'\n{row[0]}\n{row[2]}\n{row[1]}\n{row[3]}\n\n-----')
    
    do_again = str(input('Провести поиск ещё раз?[yY|nN]'))
    if do_again == 'Y' or do_again == 'y':
        search_string = str(input('Введи название школы\n'))
        search_for_school_id(search_string)
    return 


sqlCon = mysql.connector.connect(
        user='vlad',
        host='192.168.145.114',
        password='P@ssw0rd',
        database='schools',
            
        )
cursor = sqlCon.cursor()
search_type = int(input('Тип поиска:\n1 - по имени школы\n2 - по id школы\n'))

if search_type == 1:
    search_string = str(input('Введи название школы\n'))
    search_for_school_id(search_string)

check_school_id = int(input('Введите id школы\n'))

sql = """
    SELECT  
        DISTINCT(results.test_uid), 
        results.sid, 
        modules.name, 
        subjects.name, 
        students.name, 
        students.last_name, 
        students.patrn, 
        classes.name  
    FROM results 
    LEFT JOIN modules ON results.mid=modules.id 
    LEFT JOIN subjects ON modules.subject=subjects.id
    LEFT JOIN students ON results.student=students.id 
    LEFT JOIN classes ON students.cid=classes.id 
"""

sql = """
    SELECT 
        DISTINCT(classes.name), 
        classes.id, 
        modules.name, 
        subjects.name  
        FROM results 
    LEFT JOIN modules ON results.mid=modules.id 
    LEFT JOIN subjects ON modules.subject=subjects.id 
    LEFT JOIN students ON results.student=students.id 
    LEFT JOIN classes ON students.cid=classes.id  
    WHERE results.sid = {}
    ORDER BY classes.name
""".format(check_school_id)

cursor.execute(sql)
result = cursor.fetchall()

print('Класс | Кол-во тестов')
for row in result:
    sql = """
    SELECT  
        COUNT(DISTINCT(results.test_uid)) as 'count' 
    FROM results 
    LEFT JOIN modules ON results.mid=modules.id 
    LEFT JOIN subjects ON modules.subject=subjects.id 
    LEFT JOIN students ON results.student=students.id 
    LEFT JOIN classes ON students.cid=classes.id  
    WHERE 
        classes.id = {}
        AND subjects.name = '{}';

    """.format(row[1], row[3])

    cursor.execute(sql)
    count_r = cursor.fetchone()
    print(f'{row[0]} {row[3]} {count_r[0]}')
    
