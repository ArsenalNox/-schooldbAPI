from re import escape
import mysql.connector
import sys

sqlCon = mysql.connector.connect(
        user='vlad',
        host='192.168.145.114',
        password='P@ssw0rd',
        database='schools',
            
        )
cur = sqlCon.cursor()

def main():
    try:     
        search_type = sys.argv[1]
    except Exception:
        print("""
                1 - поиск по полному имени 
                2 - поиск по сокращенному имени
                3 - поиск по муниципалитету 
                4 - поиск по полному имени и муниципалитету
                """)
        return 

    if search_type == 1:
        search_string = str(input('Введите название школы\n'))
        sql = """
            SELECT 
                * 
            FROM main 
            WHERE main.name_full LIKE "%{}%"
        """.format(search_string)

if __name__ == '__main__':
    main()
