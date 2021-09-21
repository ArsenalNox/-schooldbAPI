import pandas
import pprint
import mysql.connector

add_only_first_variant = False

pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)

df = pandas.read_excel('tests_data/matan.xlsx', header=None)
iter = 0

print('Добавляемый модуль после добавления по умолчанию всегда неактивный\n\n')
test_name = str(input('Введите название для модуля:\n'))
test_target_class = int(input('Для какого класса предназначается данный модуль\n'))

if test_target_class > 11: 
    test_target_class = 1
if test_target_class < 5:
    test_target_class = 5

sqlConnection = mysql.connector.connect(
    host='192.168.145.114',
    user='vlad',
    password='P@ssw0rd',
    database='schools'
)
cursor = sqlConnection.cursor()
sql = 'SELECT * FROM subjects'
cursor.execute(sql)
result = cursor.fetchall()
print('Данный модуль относится к предмету:\n')
for row in result:
    print(f'{row[0]} - {row[1]}')
test_subject = int(input())

test = []

for columns in df:
    for row in df[columns]:
        if iter == 0:
            iter +=1 
            continue

        question = {}
        question['q_num']     = iter
        question['q_type']    = df[3][iter]
        question['q_subtype'] = df[4][iter]

        #Проверяем, есть ли уже этот тип вопроса в бд
        isNull = False
        if pandas.isna(question['q_type']):
            question['q_type'] = '1'
        if pandas.isna(question['q_subtype']):
            question['q_subtype'] = '1'

        sql = f"SELECT * FROM question_types WHERE name = '{question['q_type']}'"
        print(question['q_type'], sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        found = False
        for row in result:
            print(f'{iter} Тип вопроса найден в базе данных')
            found = True
            question['q_type'] = row[0]

        if not found: 
            print('Тип вопроса не найден в базе данных')
            sql = f"INSERT INTO question_types(`name`) VALUES('{question['q_type']}')"
            cursor.execute(sql)
            new_question_type_id = cursor.lastrowid
            question['q_type'] = new_question_type_id

        question['q_text'] = df[5][iter]
        question['questions'] = []

        for i in range(0, 8, +2):
            question['questions'].append(
                {
                    'text': str(df[5][iter])+' '+str(df[6+i][iter]),
                    'answ': df[7+i][iter]
                })

        iter += 1
        test.append(question)
    break

sqlConnection.commit()

#Генерация sql запрсов для внесения модуля 
sql = "INSERT INTO modules(`targeted_class`, `subject`, `name`, `isActive`) VALUES(%s, %s, %s, %s)" 
values = (test_target_class, test_subject, test_name, 0)
cursor.execute(sql, values)

mid = cursor.lastrowid

for task in test:
    variant = 1
    for question in task['questions']:
        #Добавление иднивидуального вопроса 

        sql = """INSERT INTO modules_questions(
            `mid`, 
            `q_type`, 
            `q_subtype`, 
            `q_text`,
            `q_num`,
            `q_variant`,
            `answ1`,
            `answ2`,
            `answ3`,
            `answ4`,
            `correct_answ`
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
        #TODO Написать алгоритм перемешивания ответов между answ1-2 + корректное изменение answ1 

        correct_answer = 1
        if task['questions'][0]['answ'] == question['answ']:
            correct_answer = 1
        if task['questions'][1]['answ'] == question['answ']:
            correct_answer = 2
        if task['questions'][2]['answ'] == question['answ']:
            correct_answer = 3
        if task['questions'][3]['answ'] == question['answ']:
            correct_answer = 4
        
        values = (
            mid,
            task['q_type'],
            task['q_subtype'],
            question['text'],
            task['q_num'],
            variant,
            task['questions'][0]['answ'],
            task['questions'][1]['answ'],
            task['questions'][2]['answ'],
            task['questions'][3]['answ'],
            correct_answer
        )
        print(values)
        cursor.execute(sql, values)
        print(question['text'])
        if add_only_first_variant:
            break

        variant += 1

sqlConnection.commit()

#pp.pprint(test)
print(f'Тест успешно занесён\nКоличество вопросов: {iter}')
