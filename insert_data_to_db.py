import mysql.connector
import pandas
import logging

logging.basicConfig(
    filename='insert.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

logging.info("Starting insertion...")

def main():
    try:
        df = pandas.read_excel('data/data.xlsx')
    except FileNotFoundError as err:
        logging.critical(err)
        return False
    except Exception as err:
        logging.critical(err)
        return False

    #TODO: Сделать импорт основных необходимых данных из таблицы 
    #TODO: Написать API для организации создания сдошек
    needeed_columns = {
        "s_name":'SCHOOLNAME',
        "s_short_name": 'SHORTNAME',
        "s_type":'SCHOOLTYPEFK'
    }
    iter = 0
    for column in df: 
        print(f'Iterating over column "{column}"...')
        for row in df[column]:

            print(df[needeed_columns['s_name']][iter])

            iter += 1
        break
    print('OK')
    return True 

if __name__ == '__main__':
    if not main():
        print('Insertion exited with error')
    
