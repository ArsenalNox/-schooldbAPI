from os import curdir
import mysql.connector
import xlsxwriter

sqlCon = mysql.connector.connect(
        user='vlad',
        host='192.168.145.114',
        password='P@ssw0rd',
        database='schools',
            
        )
cursor = sqlCon.cursor()

print('executing...')


sql = """
    SELECT 
        name_short, 
        type, 
        main.id, 
        munipals.name  
    FROM main
    LEFT JOIN munipals ON munipals.id=main.mo
    WHERE main.id IN (
            SELECT 
                DISTINCT(main.id) AS "schools_present" 
            FROM results 
            LEFT JOIN main ON main.id=results.sid
            );

    """

cursor.execute(sql)

result = cursor.fetchall()
xlsxBook = xlsxwriter.Workbook("таблица_присутствующих_школ.xlsx")
workSheet = xlsxBook.add_worksheet()


xl_cursor_row = 1
workSheet.write(0, 0, 'Название')
workSheet.write(0, 1, 'Тип')

for row in result:
    print(row[0])
    workSheet.write(xl_cursor_row, 0, row[0])
    workSheet.write(xl_cursor_row, 1, row[1])
    workSheet.write(xl_cursor_row, 2, row[2])

    sql = f'SELECT COUNT(DISTINCT(id)) as "count" FROM students WHERE sid = "{row[2]}" AND token IS NOT null'
    cursor.execute(sql)
    result = cursor.fetchone()
    workSheet.write(xl_cursor_row, 3, result[0])

    xl_cursor_row += 1
    
xlsxBook.close()
