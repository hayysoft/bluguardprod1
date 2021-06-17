from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
	SessionAuthentication, BasicAuthentication
)
from rest_framework.decorators import (
	api_view, permission_classes,
	authentication_classes
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

import os
import json
import mysql.connector as mysql


config = {
    'host': 'bluguardprod1.mysql.database.azure.com',
    'user': 'bluguardprod1@bluguardprod1',
    'password': 'DoNotHack2021!',
    'database': 'bluguarddb',
    'client_flags': [mysql.ClientFlag.SSL],
    'ssl_ca': '',
}

def Create_Connector_To_DB():
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()
	Cursor.execute('SET GLOBAL connect_timeout = 10')

	return Cursor


def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row)) for row in cursor.fetchall()
	]


def Process_Files_For_Discharded_Users(Device_Mac, Patient_Tag):
	os.chdir('C:/Users/hayysoft/Documents/Scripts/interview/media')
	try:
		os.rename(f'C:/Users/hayysoft/Documents/Scripts/interview/media/{Device_Mac}.json', f'C:/Users/hayysoft/Documents/Scripts/interview/media/Discharged_Patients/{Patient_Tag}.json')
	except FileNotFoundError:
		pass


def Get_Device_ID_For_Symptom_Check_In(Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Device_ID,
			CONCAT(Device_Last_Updated_Date, ' ',
                   Device_Last_Updated_Time) AS Datetime
		FROM TBL_Device
		WHERE Wearer_ID = %s
	'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	try:
		Device_IDs = [row[0] for row in results]
		Datetimes = [row[1] for row in results]
	except Exception:
		return None, None

	return Device_IDs, Datetimes



# @require_http_methods(['POST'])
# @csrf_exempt
def Crest_CR03_Symptoms_Check_In(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()
	query = '''
		SELECT Daily_Survey_Q2_Y1,
			   Daily_Survey_Q2_Y2, Daily_Survey_Q2_Y3,
			   Daily_Survey_Q2_Y4, Daily_Survey_Q2_Y5,
			   Wearer_ID
		FROM tbl_daily_survey
	'''
	Cursor.execute(query)
	results = Cursor.fetchall()
	data = [
		{
			'subject_id': 0,
			'device_id': 0,
			'datetime': '',
			'fever': row[0],
			'breathing': row[1],
			'coughing': row[2],
			'eating': row[3],
			'tiredness': row[4],
			'doctor': '',
			'photo': '',
			'cough_sound': ''
		} for row in results
	]
	Wearer_IDs = [row[5] for row in results]
	# print(Wearer_IDs)

	Device_IDs = []
	for wearer_id in Wearer_IDs:
		results = Get_Device_ID_For_Symptom_Check_In(wearer_id)
		Device_ID = results[0]
		Datetimes = results[1]
		Device_IDs.append((Device_ID, Datetimes))

	for index, values in enumerate(Device_IDs):
		data[index]['device_id'] = values[0]
		data[index]['datetime'] = values[1]

	return JsonResponse({
		'symptom': data
	})



@require_http_methods(['POST'])
@csrf_exempt
def Crest_CR03_Check_Out_Patient(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	data = json.loads(request.body)
	Patient_Tag = data['Patient_Tag']

	query = '''
		SELECT COUNT(*) FROM TBL_Crest_Patient
		WHERE Patient_Tag = %s AND
			  Patient_Discharged = %s
	'''
	parameters = (Patient_Tag, 0)
	Cursor.execute(query, parameters)
	results = dictfetchall(Cursor)

	if len(results) == 0:
		return JsonResponse({
			'response': 'Patient ID does not exists OR already discharged'
		})

	query = '''SELECT Wearer_ID, Patient_ID FROM TBL_Crest_Patient
				WHERE Patient_Tag = %s
			'''
	parameter = (Patient_Tag,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)
	Wearer_ID = results[0]['Wearer_ID']
	Patient_ID = results[0]['Patient_ID']

	query = '''UPDATE TBL_Wearer
				SET Status = %s
				WHERE Wearer_ID = %s
			'''
	parameters = ('Unassigned', Wearer_ID)
	Cursor.execute(query, parameters)
	Connector.commit()

	query = '''UPDATE TBL_Crest_Patient
				SET Patient_Discharged = %s
				WHERE Patient_ID = %s
			'''
	parameters = (1, Patient_ID)
	Cursor.execute(query, parameters)
	Connector.commit()

	query = '''SELECT Device_Mac FROM TBL_Device
				WHERE Wearer_ID = %s'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)
	Device_Mac = results[0]['Device_Mac']
	print(f'Device_Mac = {Device_Mac}')

	Process_Files_For_Discharded_Users(
		Device_Mac, Patient_Tag
	)

	return JsonResponse({
		'response': 'Successfull'
	})



def Get_Patient_Tag_Checkout_Status(request, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()
	query = '''
		SELECT Patient_Tag, Patient_Discharged
		FROM TBL_Crest_Patient
		WHERE Wearer_ID = %s
	'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	data = [
		{
			'Patient_Tag': row[0],
			'Patient_Discharged': row[1]
		} for row in results
	]
	try:
		data = data[0]
	except Exception:
		pass

	return JsonResponse({
		'checkout_status': data
	})



# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(['POST'])
@csrf_exempt
def Post_Creat_Device_Alert(request):
	data = json.loads(request.body)
	print(data)

	return JsonResponse({
		'data': data
	})



# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(['POST'])
@csrf_exempt
def Post_Creat_Checkin_Api(request):
	data = json.loads(request.body)
	print(json.dumps(data, indent=4))

	return JsonResponse({
		'data': data
	})



def Fetch_Crest_TBL_Patient():
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT * FROM Crest_TBL_Patient'
	Cursor.execute(query)
	rows = Cursor.fetchall()

	for row in rows:
	    query = '''
	        SELECT * FROM tbl_device WHERE
	        Device_Tag = %s
	    '''
	    Device_Tag = row[3]
	    parameter = (Device_Tag,)
	    Cursor.execute(query, parameter)
	    results = Cursor.fetchall()
	    for result in results:
	        Subject_ID = row[0]
	        Device_ID = result[0]
	        Gateway_Mac = result[-4]
	        query = '''
	            SELECT * FROM tbl_gateway
	            WHERE Gateway_Mac = %s
	        '''
	        parameter = (Gateway_Mac,)
	        Cursor.execute(query, parameter)
	        gateway_results = Cursor.fetchall()
	        for gateway in gateway_results:
	            Latitude = gateway[6]
	            Longitude = gateway[7]
	            Datetime = datetime.now().time()
	            Device_Temp = result[8]
	            Device_HR = result[9]
	            Device_O2 = result[10]
	            Respiratory_Rate = 0
	            Data_To_Submit = {
	                'subject_id': Subject_ID,
	                'device_id': Device_ID,
	                'datetime': str(Datetime),
	                'latitude': str(Latitude),
	                'longitude': Longitude,
	                'temperature': Device_Temp,
	                'SpO2': Device_O2,
	                'heartrate': Device_HR,
	                'respiratory_rate': Respiratory_Rate
	            }




@require_http_methods(['POST'])
@csrf_exempt
def Post_Data_To_API(request):
    data = json.loads(request.body)

    return JsonResponse(data)




def Check_Device_Tag(Device_Tag):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT COUNT(*) FROM TBL_Wearer
                 WHERE Status = %s AND Wearer_ID IN (
                 	SELECT Wearer_ID FROM TBL_Device
                 	WHERE Device_Tag = %s
                 )'''
	parameter = ('Unassigned', Device_Tag)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()

	if results[0][0] != 0:
	    return 1

	return 0



@require_http_methods(['POST'])
@csrf_exempt
def Post_CR03_Registration(request):
	data = json.loads(request.body)
	Patient_Tag = data['Patient_Tag']
	Device_Tag = data['Device_Tag']

	band_tag_check = Check_Device_Tag(Device_Tag)
	results = None

	if band_tag_check == 0:
		results = 0
	else:
		Connector = mysql.connect(**config)
		Cursor = Connector.cursor()

		query = '''
			UPDATE TBL_Wearer
			SET Status = %s
			WHERE Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Device
				WHERE Device_Tag = %s
			)
		'''
		print(f'Device_Tag = {Device_Tag}')
		parameters = ('Assigned', Device_Tag)
		Cursor.execute(query, parameters)
		Connector.commit()

		query = '''
		INSERT INTO TBL_Crest_Patient
		        (Patient_ID, Patient_Tag, Device_Tag,
		        Created_Date, Created_Time, Wearer_ID,
		        Patient_Discharged)
		VALUES ((SELECT Create_PK("PID")), %s, %s, CURDATE(),
		        CURTIME(), (
		            SELECT Wearer_ID FROM tbl_wearer
		            WHERE Wearer_ID = (
		                SELECT Wearer_ID FROM tbl_device
		                WHERE Device_Tag = %s
		            )
		        ), %s)

		'''
		parameters = (Patient_Tag, Device_Tag, Device_Tag, 0)
		Cursor.execute(query, parameters)
		Connector.commit()
		results = 1

	return JsonResponse({
    	'results': results
    })



@require_http_methods(['POST'])
@csrf_exempt
def Post_Wearer_Login(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	data = json.loads(request.body)
	Wearer_Nick = data['Wearer_Nick']
	Wearer_Pwd = data['Wearer_Pwd']

	query = '''
		SELECT * FROM tbl_wearer
		WHERE Wearer_Nick = %s AND
			  Wearer_Pwd = %s
	'''
	parameters = (Wearer_Nick, Wearer_Pwd)
	Cursor.execute(query, parameters)
	results = Cursor.fetchall()

	data = [
		{
			'Wearer_ID': row[0],
			'Wearer_Nick': row[1],
			'Wearer_Pwd': row[2]
		} for row in results
	]

	try:
		data = data[0]
	except Exception:
		data = data

	return JsonResponse({
		'Wearer_Data': data
	})




def Get_Wearer_All_Devices(request, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT * FROM tbl_device
		WHERE Wearer_ID = %s
	'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()

	data = [
		{
			'Device_ID': row[0],
			'Device_Type': row[1],
			'Device_Serial_No': row[2],
			'Device_Mac': row[3],
			'Device_Bat_Level': row[4],
			'Device_Last_Updated_Date': row[5],
			'Device_Last_Update_Time': row[6],
			'Wearer_ID': row[7],
			'Device_Temp': row[8],
			'Device_HR': row[9],
			'Device_O2': row[10],
			'Incoming_ID': row[11],
			'Device_RSSI': row[12],
			'Gateway_Mac': row[13],
			'Incorrect_Data_Flag': row[14],
			'Device_Status': row[13],
			'Device_Tag': row[15],
		} for row in results
	]

	return JsonResponse({
		'Wearer_Data': data
	})





def Get_Wearer_Alert(request, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Alert_ID, Alert_Code, Alert_Date,
			   Alert_Time, Device_ID, Alert_Reading
		FROM TBL_Alert
		WHERE Device_ID IN
			(SELECT Device_ID FROM tbl_device
			WHERE Wearer_ID = %s)
	'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()

	data = [
		{
			'Alert_ID': row[0],
			'Alert_Code': row[1],
			'Alert_Date': row[2],
			'Alert_Time': row[3],
			'Device_ID': row[4],
			'Alert_Reading': row[5]
		} for row in results
	]

	return JsonResponse({
		'Wearer_Alert': data
	})



def Get_Wearer_Message(request, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT * FROM TBL_Message
		WHERE Wearer_ID = %s OR
		Wearer_ID = 'ALL'
	'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()

	data = [
		{
			'Message_ID': row[0],
			'Message_Description': row[1],
			'Message_Date': row[2],
			'Message_Time': row[3],
			'Message_Type': row[4],
			'User_ID': row[5],
			'Wearer_ID': row[6]
		} for row in results
	]

	return JsonResponse({
		'Wearer_Alert': data
	})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_All_Users_Data(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT * FROM tbl_user';
	Cursor.execute(query)
	results = Cursor.fetchall()
	data = [
		{'User_ID': row[0]} for row in results
	]

	return JsonResponse({
		'User_IDs': data
	})



def Get_Wearer_Survey(request, Daily_Survey_Session, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT * FROM TBL_Daily_Survey
		WHERE Daily_Survey_Session = %s AND Wearer_ID = %s
	'''
	parameters = (Daily_Survey_Session, Wearer_ID)
	Cursor.execute(query, parameters)
	results = Cursor.fetchall()
	data = [
		{
			'Daily_Survey_ID': row[0],
			'Daily_Survey_Q1': row[1],
			'Daily_Survey_Q2_Y1': row[2],
			'Daily_Survey_Q2_Y2': row[3],
			'Daily_Survey_Q2_Y3': row[4],
			'Daily_Survey_Q2_Y4': row[5],
			'Daily_Survey_Q2_Y5': row[6],
			# 'Daily_Survey_Q2_N': row[7],
			'Daily_Survey_Q3': row[7],
			'Daily_Survey_Date': row[8],
			'Daily_Survey_Time': row[9],
			'Daily_Survey_Session': row[10],
			'Wearer_ID': row[11]
		} for row in results
	]

	return JsonResponse({
		'Wearer_Survey': data
	})



@require_http_methods(['POST'])
@csrf_exempt
def Post_Wearer_Survey(request):
	data = json.loads(request.body)

	Daily_Survey_Q1 = data['Daily_Survey_Q1']
	Daily_Survey_Q2_Y1 = data['Daily_Survey_Q2_Y1']
	Daily_Survey_Q2_Y2 = data['Daily_Survey_Q2_Y2']
	Daily_Survey_Q2_Y3 = data['Daily_Survey_Q2_Y3']
	Daily_Survey_Q2_Y4 = data['Daily_Survey_Q2_Y4']
	Daily_Survey_Q2_Y5 = data['Daily_Survey_Q2_Y5']
	# Daily_Survey_Q2_N = data['Daily_Survey_Q2_N']
	Daily_Survey_Q3 = data['Daily_Survey_Q3']
	Daily_Survey_Date = data['Daily_Survey_Date']
	Daily_Survey_Time = data['Daily_Survey_Time']
	Daily_Survey_Session = data['Daily_Survey_Session']
	Wearer_ID = data['Wearer_ID']

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
	INSERT INTO TBL_Daily_Survey (
		Daily_Survey_ID,
		Daily_Survey_Q1,
		Daily_Survey_Q2_Y1,
		Daily_Survey_Q2_Y2,
		Daily_Survey_Q2_Y3,
		Daily_Survey_Q2_Y4,
		Daily_Survey_Q2_Y5,
		Daily_Survey_Q3,
		Daily_Survey_Date,
		Daily_Survey_Time,
		Daily_Survey_Session,
		Wearer_ID
	) VALUES (
		(SELECT Create_PK("SVY")),
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s
	)
	'''
	parameters = (
		Daily_Survey_Q1,
		Daily_Survey_Q2_Y1,
		Daily_Survey_Q2_Y2,
		Daily_Survey_Q2_Y3,
		Daily_Survey_Q2_Y4,
		Daily_Survey_Q2_Y5,
		Daily_Survey_Q3,
		Daily_Survey_Date,
		Daily_Survey_Time,
		Daily_Survey_Session,
		Wearer_ID
	)
	Cursor.execute(query, parameters)
	Connector.commit()


	return JsonResponse({
		'message': 'Daily_Survey was inserted successfully!'
	})



@require_http_methods(['POST'])
@csrf_exempt
def Delete_Message(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	data = json.loads(request.body)
	Message_ID = data['Message_ID']

	query = '''
		DELETE FROM tbl_message
		WHERE Message_ID = %s
	'''
	parameter = (Message_ID,)
	Cursor.execute(query, parameter)
	Connector.commit()

	return JsonResponse({
		'message': f'Message_ID = {Message_ID} was successfully deleted!'
	})



def Get_All_Users(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT User_ID, User_Name FROM tbl_user';
	Cursor.execute(query)
	results = Cursor.fetchall()
	data = [
		{
			'User_ID': row[0],
			'User_Name': row[1],
			'Device_ID': row[2]
		} for row in results
	]

	return JsonResponse({
		'User_IDs': data
	})



def Fetch_One_Or_Many(field, tablename, query):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if field == 'NULL':
		Cursor.execute(f'SELECT * FROM {tablename}')
	else:
		parameter = (field,)
		Cursor.execute(query, parameter)

	return Cursor


def Get_Alert(request, Wearer_ID='NULL'):
	Cursor = Fetch_One_Or_Many(Wearer_ID, 'TBL_Alert',
					 '''SELECT * FROM TBL_Alert
						WHERE Device_ID IN
						(SELECT Device_ID FROM tbl_device
						WHERE Wearer_ID = %s)
						ORDER BY Device_ID DESC LIMIT 5''')

	results = Cursor.fetchall()
	data = [
		{
			'Alert_ID': row[0],
			'Alert_Code': row[1],
			'Alert_Date': row[2],
			'Alert_Time': row[3],
			'Device_ID': row[4]
		} for row in results
	]

	return JsonResponse({
		'Alert': data
	})



def Get_User_Message(request, User_id):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = """SELECT * FROM TBL_Message
		WHERE User_ID = %s OR
		User_ID = 'ALL'"""
	parameter = (User_id,)
	Cursor.execute(query, parameter)


	results = Cursor.fetchall()
	data = [
		{
			'Message_ID': row[0],
			'Message_Description': row[1],
			'Message_Date': row[2],
			'Mesage_Time': row[3],
			'Message_Type': row[4],
			'User_ID': row[5]
		} for row in results
	]

	return JsonResponse({
		'Message': data
	})



def Fetch_One(field, query):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	parameter = (field,)
	Cursor.execute(query, parameter)

	return Cursor


def Get_User_Password(request, User_id):
	Cursor = Fetch_One(User_id,
				   '''SELECT User_Pwd FROM tbl_user
					  WHERE User_ID = %s''')

	try:
		results = Cursor.fetchone()[0]
	except (IndexError, TypeError):
		results = ''

	return JsonResponse({
		'User_Pwd': results
	})



def Get_User_ID(request, User_Login):
	Cursor = Fetch_One(User_Login,
				  '''SELECT * FROM tbl_user
					 WHERE User_LogIn = %s''')

	try:
		results = Cursor.fetchone()
		data = [
			{'User_ID': results[0],
			 'User_Name': results[1],
			 'User_Email': results[2],
			 'User_Login': results[3],
			 'User_Pwd': results[4],
			 'Org_ID': results[5]}
		]
		results = data
	except (IndexError, TypeError):
		results = ''

	return JsonResponse({
		'User': results
	})



def Get_Subscribed_Device(request, User_id='NULL'):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if User_id == 'NULL':
		Cursor.execute(f'SELECT * FROM tbl_subscription')
	else:
		query = '''SELECT Device_ID FROM tbl_subscription
					 WHERE User_ID = %s'''
		parameter = (User_id,)
		Cursor.execute(query, parameter)

	# Cursor = Fetch_One(User_id,
	# 			  '''SELECT Device_ID FROM tbl_subscription
	# 				 WHERE User_ID = %s''')

	results = Cursor.fetchall()
	values = []
	for result in results:
		values.append({f'Device_ID': result[0]})
	results = values

	return JsonResponse({
		'Device': results
	})


def Get_All_Unsubscribed_Device(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT * FROM TBL_Device
			     WHERE Device_ID NOT IN
			   (SELECT Device_ID FROM tbl_subscription)'''
	Cursor.execute(query)
	results = Cursor.fetchall()

	data = [
		{
			'Device_ID': row[0],
			'Device_Type': row[1],
			'Device_Serial_No': row[2],
			'Device_Mac': row[3],
			'Device_Bat_Level': row[4],
			'Device_Last_Updated_Date': row[5],
			'Device_Last_Update_Time': row[6],
			'Wearer_ID': row[7],
			'Device_Temp': row[8],
			'Device_HR': row[9],
			'Device_O2': row[10],
			'Incoming_ID': row[11]
		} for row in results
	]
	results = data

	return JsonResponse({
		'Device': results
	})


def Get_Unsubscribed_Device(request, User_id='NULL'):
	Cursor = Fetch_One(User_id,
				  '''SELECT Device_ID FROM TBL_Device
					 WHERE Device_ID NOT IN
					 (SELECT Device_ID FROM tbl_subscription
					 WHERE User_ID = %s)''')

	results = Cursor.fetchall()
	x = 1
	values = []
	for result in results:
		values.append({f'Device_ID': result[0]})
	results = values

	return JsonResponse({
		'Device_ID': results
	})


def Get_All_Device(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT Device_ID FROM tbl_device'
	Cursor.execute(query)

	results = Cursor.fetchall()
	x = 1
	data = {}
	for result in results:
		data[f'Device_ID_{x}'] =  result[0]
		x += 1
	results = data

	return JsonResponse({
		'Device_ID': results
	})


def Get_Wearer(request, Device_ID='NULL'):
	Cursor = Fetch_One(Device_ID,
			  '''SELECT * FROM tbl_wearer
				 WHERE Wearer_ID IN
				 (SELECT Wearer_ID FROM TBL_Device
			 	 WHERE Device_ID = %s)''')

	results = Cursor.fetchall()
	data = [
		{
			'Wearer_ID': row[0],
			'Wearer_Nick': row[1]
		} for row in results
	]
	results = data

	return JsonResponse({
		'Wearer': results[0]
	})



def Get_Device_Vital(request, Device_ID='NULL'):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT Device_Temp, Device_HR, Device_O2
	FROM TBL_Device WHERE Device_ID = %s'''

	parameter = (Device_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	data = [
		{
			'Device_Temp': row[0],
			'Device_HR': row[1],
			'Device_O2': row[2]
		} for row in results
	]

	try:
		results = data[0]
	except Exception:
		results = []

	return JsonResponse({
		'Device_Vital': results
	})



def Get_Ack(request, Alert_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT * FROM TBL_Acknowledgement
			 WHERE Alert_ID = %s'''
	parameter = (Alert_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()

	try:
		data = [
			{
				'Ack_ID': row[0],
				'User_ID': row[1],
				'Ack_Date': row[2],
				'Ack_Time': row[3],
				'Alert_ID': row[4]
			} for row in results
		]
		results = data[0]
	except IndexError:
		results = []

	return JsonResponse({
		'Ack': results
	})


def Post_Update_Values(field1, field2, query):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if field1 == 'NULL' or field2 == 'NULL':
		results = 0
	else:
		parameter = (field1, field2,)
		Cursor.execute(query, parameter)
		Connector.commit()
		results = 1

	return results


@require_http_methods(['POST'])
@csrf_exempt
def Post_Add_Subscription(request):
	data = json.loads(request.body)
	User_ID = data['User_ID']
	Wearer_ID = data['Wearer_ID']

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT Device_ID FROM TBL_Device
			   WHERE Wearer_ID = %s'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	for row in results:
		query = '''INSERT INTO tbl_subscription
						VALUES ((SELECT Create_PK("SUBS")), %s, %s,
							    CURRENT_DATE(), CURRENT_TIME())'''
		parameter = (User_ID, row[0],)
		Cursor.execute(query, parameter)
		Connector.commit()

	return JsonResponse({
		'Add_Subscription': results
	})



@require_http_methods(['POST'])
@csrf_exempt
def Post_Change_Password_Wearer(request):
	data = json.loads(request.body)
	Wearer_ID = data['Wearer_ID']
	Wearer_Pwd = data['Wearer_Pwd']

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''UPDATE tbl_wearer
		SET Wearer_Pwd = %s
		WHERE Wearer_ID = %s'''
	parameter = (Wearer_Pwd, Wearer_ID)
	Cursor.execute(query, parameter)
	Connector.commit()


	return JsonResponse({
		'Change_Password-Tbl-Wearer': f'Password for Wearer_ID = {Wearer_ID} changed successfully!'
	})





@require_http_methods(['POST'])
@csrf_exempt
def Post_Change_Password(request):
	data = json.loads(request.body)
	User_ID = data['User_ID']
	New_Password = data['New_Password']

	if User_ID == 'NULL' or New_Password == 'NULL':
		results = 0
	else:
		Connector = mysql.connect(**config)

		Cursor = Connector.cursor()

		query = '''SELECT * FROM tbl_user
			WHERE User_ID = %s'''
		parameter = (User_ID,)
		Cursor.execute(query, parameter)
		results = Cursor.fetchone()
		if results is None:
			results = 0
		else:
			query = '''UPDATE tbl_user
				SET User_Pwd = %s
				WHERE User_ID = %s'''
			parameter = (New_Password, User_ID)
			Cursor.execute(query, parameter)
			Connector.commit()
			results = 1

	return JsonResponse({
		'Change_Password-Tbl-User': results
	})


@require_http_methods(['POST'])
@csrf_exempt
def Post_Change_Email(request):
	data = json.loads(request.body)
	User_ID = data['User_ID']
	New_Email = data['New_Email']

	if User_ID == 'NULL' or New_Email == 'NULL':
		results = 0
	else:
		Connector = mysql.connect(**config)

		Cursor = Connector.cursor()
		query = '''SELECT * FROM tbl_user
			WHERE User_ID = %s'''
		parameter = (User_ID,)
		Cursor.execute(query, parameter)
		results = Cursor.fetchone()
		if results is None:
			results = 0
		else:
			query = '''UPDATE tbl_user
				SET User_Email = %s
				WHERE User_ID = %s'''
			parameter = (New_Email, User_ID)
			Cursor.execute(query, parameter)
			Connector.commit()
			results = 1

	return JsonResponse({
		'Change_Email': results
	})


@require_http_methods(['POST'])
@csrf_exempt
def Post_Acknowledgement_Alert(request):
	data = json.loads(request.body)
	User_ID = data['User_ID']
	Alert_ID = data['Alert_ID']

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''INSERT INTO TBL_Acknowledgement
				(Ack_ID, User_ID, Ack_Date,
				 Ack_Time, Alert_ID)
				VALUES ((SELECT Create_PK("ACK")), %s,
						 CURRENT_DATE(), CURRENT_TIME(),
						 %s)'''
	parameter = (User_ID, Alert_ID,)
	Cursor.execute(query, parameter)
	Connector.commit()

	return JsonResponse({
		'Add_Subscription': "Data inserted successfully!"
	})




@require_http_methods(['POST'])
@csrf_exempt
def Post_User_Login(request):
	data = json.loads(request.body)
	username = data.get('User_Name')
	password = data.get('User_Pwd')

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT * FROM tbl_user
			   WHERE User_Name = %s AND User_Pwd = %s'''
	parameters = (username, password,)
	Cursor.execute(query, parameters)
	results = Cursor.fetchall()
	data = [
		{'User_ID': row[0],
		 'User_Name': row[1],
		 'User_Email': row[2],
		 'User_LogIn': row[3],
		 'User_Pwd': row[4]
		 } for row in results
	]
	try:
		results = data[0]
	except IndexError:
		results = []

	return JsonResponse({
		'User_Info': results
	})


