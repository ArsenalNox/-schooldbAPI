#!/usr/bin/env python

import mysql.connector
import pandas
import logging

logging.basicConfig(
    filename='insert.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

logging.info("Starting insertion...")


def create_database_connection():
    sqlConnection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='schools'
            )

    return sqlConnection

def insert_new_type(new_type:str):
    sqlConnection = create_database_connection()
    cursor = sqlConnection.cursor()

    #TODO: Add check if type already exists 
    sql = "INSERT INTO `types`(`name`) VALUES('%s')"
    try:
        cursor.execute(sql, (new_type))
        sqlConnection.commit()
    except Exception as err:
        logging.error(f'Cannot insert new type to database, err:{err}')
    
def insert_new_munipla(munipal:str):
    pass


def main():
    try:
        df = pandas.read_excel('data/data.xlsx')
    except Exception as err:
        logging.critical(err)
        return False

    #TODO: Сделать импорт основных необходимых данных из таблицы 
    #TODO: Написать API для организации создания сдошек
    needeed_columns = {
        "s_name":'SCHOOLNAME',
        "s_short_name": 'SHORTNAME',
        "s_type":'SCHOOLTYPEFK',
        "s_id":"SCHOOLID",
        "s_munipal":"AREAFK",
        "s_address":"UR_ADDRESS"
    }
    
    iter = 0
    school_types = []
    schools = [] 

    for column in df: 
        print(f'Iterating over column "{column}"...')
        for row in df[column]:
            school = []

            school.append(str(df[needeed_columns['s_name']][iter]).replace('\n', ''))
            school.append(str(df[needeed_columns['s_short_name']][iter]).replace('\n', ''))
            school.append(str(df[needeed_columns['s_type']][iter]).replace('\n', ''))
            school.append(str(df[needeed_columns['s_id']][iter]))
            school.append(str(df[needeed_columns['s_munipal']][iter]).replace('\n', ''))
            school.append(str(df[needeed_columns['s_address']][iter]).replace('\n', ''))

            if school[2] not in school_types:
                school_types.append(school[2])

            outstr = "\n".join(school)
            #print(f"{outstr}")
            #print('\n\n')
            
            iter += 1
            
            schools.append(school)
        break

    print(f'OK\nSchools:{len(schools)}\nTypes:{school_types}')
    return schools, school_types

if __name__ == '__main__':
    result = main()
    
    if result == False:
        print('Insertion exited with error')
    else:
        sqlConnection = create_database_connection()
        cursor = sqlConnection.cursor()

        for school_type in result[1]:
            print(school_type)

        for school in result[0]:
            sql = "INSERT INTO `main`(`name_full`, `name_short`, `type`, `code`, `mo`, `addr`) VALUES(%s, %s, %s, %s, %s, %s)"
            values = (
                    school[0],
                    school[1],
                    school[2],
                    school[3],
                    school[4],
                    school[5]
                    )

            cursor.execute(sql, values)
        sqlConnection.commit()
        

