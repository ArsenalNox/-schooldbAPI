import mysql.connector
import sys
import xlsxwriter
import time

def main():
    con = mysql.connector.connect(
        host='192.168.145.114',
        user='vlad',
        password='P@ssw0rd',
        database='schools'
    )

    curs = con.cursor()
    
    try:
        mo = sys.argv[1]
        
    except Exception:
        print("""
    Usage: 
    [mo_id]: generate info table for munipal
    -l:      get list of all munipals
    -a:      get all munipals 
            """)
        return 

    if mo == '-l':
        sql = 'SELECT * FROM munipals'
        curs.execute(sql)
        result = curs.fetchall()
        for row in result:
            print(f'{row[0]}-{row[1]}')
        return 
    
    if mo == '-a':
        sql = 'SELECT * FROM munipals'
        curs.execute(sql)
        active_mos = curs.fetchall()
    else:
        sql = 'SELECT * FROM munipals WHERE id = {}'.format(mo)
        curs.execute(sql)
        active_mos = curs.fetchall()
    

    workBook    = xlsxwriter.Workbook('мониторинг.xlsx')
    workSheet   = workBook.add_worksheet() 
    working_row = 0

    workSheet.write(working_row, 0, 'Муниципалитет')
    workSheet.write(working_row, 1, 'активных классов')
    workSheet.write(working_row, 2, 'сданных тестов')
    workSheet.write(working_row, 3, 'активных учеников')
    working_row += 1 

    for mo in active_mos:
        print(f'Generating report for munipal {mo[0]}:{mo[1]}')

        #кол-во тестов в данном муниципалитете 
        print('Getting test count...')
        sql = f'SELECT COUNT(DISTINCT(test_uid)) AS "count" FROM results LEFT JOIN main ON main.id=results.sid WHERE main.mo = {mo[0]};'
        curs.execute(sql)
        result = curs.fetchone()

        #кол-во активных участников 
        print('Getting active student count...')
        sql = f'SELECT COUNT(DISTINCT(student)) AS "count" FROM results LEFT JOIN main ON main.id=results.sid WHERE main.mo = {mo[0]};'
        curs.execute(sql)
        result2 = curs.fetchone()

        #кол-во активных классов 
        print('Getting active classes count...')
        sql = f"""
            SELECT 
                COUNT(DISTINCT(classes.id))
            FROM results 
            LEFT JOIN students ON results.student=students.id 
            LEFT JOIN classes ON students.cid=classes.id
            LEFT JOIN main ON main.id=classes.sid
            WHERE main.mo = {mo[0]}
        """
        print(sql)
        curs.execute(sql)
        result3 = curs.fetchone()
            
        workSheet.write(working_row, 0, f'{mo[1]}')
        workSheet.write(working_row, 1, f'{result3[0]}')
        workSheet.write(working_row, 2, f'{result[0]}')
        workSheet.write(working_row, 3, f'{result2[0]}')
        workSheet.write(working_row+1, 0, 'Школы')
        workSheet.set_row(working_row+1, 0, None, {'level': 1})
        working_row += 2 
        
        #Проведение выборки по всем школам данного муниципалитета 

        sql = f"SELECT * FROM main WHERE mo = {mo[0]} AND (main.type = 'Общеобразовательные учреждения' OR main.type = 'Специальные (коррекционные)  учреждения для обучающихся, воспитанников  с отклонениями в развитии')"
        curs.execute(sql)
        result = curs.fetchall()

        for row in result:
            print(row[2])

            #кол-во тестов в данном муниципалитете 
            print('Getting test count for school...')
            sql = f'SELECT COUNT(DISTINCT(test_uid)) AS "count" FROM results LEFT JOIN main ON main.id=results.sid WHERE main.id = {row[0]};'
            curs.execute(sql)
            result = curs.fetchone()

            #кол-во активных участников 
            print('Getting active student count for school...')
            sql = f'SELECT COUNT(DISTINCT(student)) AS "count" FROM results LEFT JOIN main ON main.id=results.sid WHERE main.id = {row[0]};'
            curs.execute(sql)
            result2 = curs.fetchone()

            #кол-во активных классов 
            print('Getting active classes count...')
            sql = f"""
                SELECT 
                    COUNT(DISTINCT(classes.id))
                FROM results 
                LEFT JOIN students ON results.student=students.id 
                LEFT JOIN classes ON students.cid=classes.id
                LEFT JOIN main ON main.id=classes.sid
                WHERE main.id = {row[0]}
            """
            curs.execute(sql)
            result3 = curs.fetchone()

            workSheet.write(working_row, 0, row[2])
            workSheet.write(working_row, 1, f'{result3[0]}')
            workSheet.write(working_row, 2, f'{result[0]}')
            workSheet.write(working_row, 3, f'{result2[0]}')
            workSheet.set_row(working_row, 0, None, {'level': 1})
            working_row += 1 
    
    #кол-во тестов  
    print('Getting test count for school...')
    sql = f'SELECT COUNT(DISTINCT(test_uid)) AS "count" FROM results;'
    curs.execute(sql)
    result = curs.fetchone()

    #кол-во активных участников 
    print('Getting active student count for school...')
    sql = f'SELECT COUNT(DISTINCT(student)) AS "count" FROM results LEFT JOIN main ON main.id=results.sid;'
    curs.execute(sql)
    result2 = curs.fetchone()

    #кол-во активных классов 
    print('Getting active classes count...')
    sql = f"""
        SELECT 
            COUNT(DISTINCT(classes.id))
        FROM results 
        LEFT JOIN students ON results.student=students.id 
        LEFT JOIN classes ON students.cid=classes.id
        LEFT JOIN main ON main.id=classes.sid
    """
    curs.execute(sql)
    result3 = curs.fetchone()
    working_row+=1 
    workSheet.write(working_row, 0, f'Итого: ')
    workSheet.write(working_row, 1, f'{result3[0]}')
    workSheet.write(working_row, 2, f'{result[0]}')
    workSheet.write(working_row, 3, f'{result2[0]}')   
    
    workBook.close()
    

if __name__ == '__main__':
    main()
