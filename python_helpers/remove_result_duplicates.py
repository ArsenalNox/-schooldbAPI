import mysql.connector
import time 

def getAllSubjects():
    global cursor

    sql = """
        SELECT 
            *
        FROM subjects;
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    subjects = []

    for row in result:
        subjects.append({
            'id':   row[0],
            'name': row[1]
            })

    return subjects
    

con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
        )

cursor = con.cursor()

subjects = getAllSubjects()
for sbj in subjects: #Итерация через все предметы 
    print(f'Checking for tests with subject "{sbj["name"]}"')
    if sbj['id'] == 1:
        print(f'Skipping "{sbj["name"]}"')
        continue

    sql = f"""
        SELECT
            DISTINCT(test_uid)
        FROM results
        LEFT JOIN modules ON modules.id=results.mid 
        WHERE modules.subject = '{sbj["id"]}'
        LIMIT 10
    """

    cursor.execute(sql)
    result = cursor.fetchall()
    


    for row in result:
        empty_answers = 0
        answers_count = 0
        print(f'Checking test {row[0]}')
        sql = f"""
            SELECT 
                * 
            FROM results
            WHERE 
                test_uid = '{row[0]}'
        """
        cursor.execute(sql)
        result_answ = cursor.fetchall()
        answers_count = cursor.rowcount
        for answ in result_answ:
            
            if answ[3] == '':
                empty_answers += 1 
        print(f'Answer count:{answers_count}\nEmpty:{empty_answers}')
