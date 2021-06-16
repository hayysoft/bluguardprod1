import os
import json
import requests
import logging
from datetime import datetime
import mysql.connector as mysql
import datetime as dt



X = lambda s: os.system(s)
# os.chdir('D:\\Scripts')
# X('python Main_Program.py')

# X('python Process_Device_Alerts.py')
# X('python Send_Reminder_For_Survey_Completion.py')



# logging.basicConfig(filename='C:/Users/hayysoft/Desktop/sample4.log', level=logging.INFO)
# log = logging.getLogger('ex')

# now = dt.datetime.now()
# today = dt.date.today()
# logging.info(f'\nInformational message on {today} {now.strftime("%H:%M:%S")}')
# logging.error('An error has happened!\n')
# log.exception('Server stopped by KeyboardInterrupt')

# try:
#     logger = logging.getLogger('Run Server')
#     logger.setLevel(logging.INFO)

#     file_handler = logging.FileHandler('C:/Users/hayysoft/Desktop/sample4.log')
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)
#     logger.info('\nProgram started!')

#     X('python Main_Program.py')
# except KeyboardInterrupt as e:
#     logger.exception(e)
# except Exception as e:
#     logger.exception(e)
# finally:
#     logger.info('Program Finished!\n')

# with open("server-logging.log") as file_handler:
#     for line in file_handler:
#         print(line)



# X('python Run_Server.py')

# X('python Process_Device_Alerts.py')

# X('pyinstaller --onefile Send_Reminder_For_Survey_Completion.py')


from multiprocessing import Process


# if __name__ == '__main__':
#     p1 = Process(target=Process_Device_Alerts)
#     p1.start()
#     p2 = Process(target=Send_Reminder_For_Survey_Completion)
#     p2.start()
#     p3 = Process(target=Update_Device_Reading.py)
#     p3.start()
#     p4 = Process(target=Process_Quarentine_Breach.py)
#     p4.start()
#     p1.join()
#     p2.join()
#     p3.join()
#     p4.join()



config = {
    'host': 'bluguardprod1.mysql.database.azure.com',
    'user': 'bluguardprod1@bluguardprod1',
    'password': 'DoNotHack2021!',
    'database': 'bluguarddb',
    'client_flags': [mysql.ClientFlag.SSL],
    'ssl_ca': '',
}


# Connector = mysql.connect(**config)

# Cursor = Connector.cursor()
# Cursor.execute('SELECT * FROM TBL_Wearer')
# results = Cursor.fetchall()
# print(results)



def Check_Device_Tag(Device_Tag):
    Connector = mysql.connect(**config)

    Cursor = Connector.cursor()

    query = '''SELECT COUNT(*) FROM TBL_Wearer
                 WHERE Status = %s AND Wearer_ID = (
                    SELECT Wearer_ID FROM TBL_Device
                    WHERE Device_Tag = %s
                 )'''
    parameter = ('Unassigned', Device_Tag)
    Cursor.execute(query, parameter)
    results = Cursor.fetchall()
    print(results)


Check_Device_Tag('CR03-0002')
