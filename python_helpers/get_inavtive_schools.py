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

sql = """SELECT 
            name_short, 
            type,
            munipals.name 
        FROM main 
        LEFT JOIN munipals ON munipals.id=main.mo
        WHERE 
            main.id NOT IN   
                (
                    SELECT 
                        DISTINCT(main.id) AS "schools_present" 
                    FROM results 
                    LEFT JOIN main ON main.id=results.sid
                );
                """

cursor.execute(sql)

result = cursor.fetchall()
xlsxBook = xlsxwriter.Workbook("таблица_отсутвующих_школ.xlsx")
workSheet = xlsxBook.add_worksheet()

xl_cursor_row = 1
workSheet.write(0, 0, 'Название')
workSheet.write(0, 1, 'Тип')
workSheet.write(0, 2, 'Муниципалитет')

for row in result:
    if (    row[1] == 'Иные' 
            or row[1] == 'Дошкольные образовательные учреждения'
            ):
        print(f'\nПропускаю {row[1]}\n')
        continue
    print(f'{row[0]}\n{row[1]}')
    workSheet.write(xl_cursor_row, 0, row[0])
    workSheet.write(xl_cursor_row, 1, row[1])
    workSheet.write(xl_cursor_row, 2, row[2])
    xl_cursor_row += 1

xlsxBook.close()
