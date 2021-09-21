import re
import mysql.connector


def generate_class_list():
    letters = ['а','б','в','г','д','е','ж',
               'з','и','й','к','л','м',
               'о','п','р','с','т','у','ф',
               'х','ц','ч','ш','э','ю','я',
                ]
    list_classes = []

    for i in range(5,12,1):
      for letter in letters:
            list_classes.append(str(str(i)+letter.upper()))
    return list_classes


def generate_student_list():
    student_count = 40
    list_students = []
    name = 0
    last = 0 
    patr = 0 

    for i in range(1, student_count+1):
        patr += 1 
        if patr == 10:
            patr = 0 
            last +=1 
            if last == 10:
                name += 1
        list_students.append([name, last, patr])
    
    return list_students


sqlCon = mysql.connector.connect(
        user='vlad',
        host='192.168.145.114',
        password='P@ssw0rd',
        database='schools'
        )

cursor = sqlCon.cursor()
sql = "SELECT * FROM main WHERE id = 2112"

cursor.execute(sql)
result = cursor.fetchall()

for row in result:
    print(f'Generating classes for school {row[0]}: "{row[2]}"')
    class_list = generate_class_list()
    for school_class in class_list:
        print(f'Adding class {school_class}')
        sql = "INSERT INTO `classes`(`sid`, `name`, `year`) VALUES(%s, %s, %s)"
        year = int(re.findall('(\d+)', school_class)[0])
        cursor.execute(sql, (row[0], school_class, year))   
        
        class_inserted_id = cursor.lastrowid
        print(class_inserted_id)
        class_students = generate_student_list()
        for student in class_students:
            print(f'Adding student "{student}" to class id {class_inserted_id}')
            sql = "INSERT INTO students(sid, cid, name, last_name, patrn) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (row[0], class_inserted_id, student[0], student[1], student[2]) )

    sqlCon.commit()


