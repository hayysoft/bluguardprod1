import os
import json
import requests
import logging
from datetime import datetime
import mysql.connector as mysql
import datetime as dt



X = lambda s: os.system(s)
os.chdir('C:/Users/hayysoft/Documents/BluguardScripts')
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

X('pyinstaller --onefile Run_Main_Program.py')








