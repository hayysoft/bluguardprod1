from django.shortcuts import render, redirect
from django.contrib import messages as notification_messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import (
	authenticate, login, logout
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
	BaseAuthentication, SessionAuthentication
)
from rest_framework.decorators import (
	api_view, permission_classes,
	authentication_classes
)
from django.utils.safestring import mark_safe
from django.http import (
	JsonResponse, HttpResponse
)

from .portal_views import (
	get_individual_files,
)

import os
import json
import random
import requests
import mimetypes
from datetime import datetime
import mysql.connector as mysql


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    'port': '3306'
}

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row)) for row in cursor.fetchall()
	]


Connector = mysql.connect(**config)
Cursor = Connector.cursor()



def logout_page(request):
    logout(request)
    return JsonResponse({
    	'message': 'Successfully logged out'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def Get_Device_Details(request, Device_Mac):
	file_data = []
	files = get_individual_files()

	for file in files:
		if file == Device_Mac:
			with open(f'{file}.json') as fp:
				file_data = json.loads(fp.read())
				file_data = file_data[len(file_data) - 10:]
				for row in file_data:
					del row['timestamp']
					del row["device_mac"]
					del row["bleName"]
					del row["rssi"]
					del row["gateway_mac"]

	return JsonResponse({
		'device_data': file_data
	})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def Vital_Surveillance(request, User_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	# data = json.loads(request.body)
	# User_ID = data['User_ID']

	query = '''
		SELECT Wearer_ID, Wearer_Nick FROM TBL_Wearer
			WHERE User_ID IN (
				SELECT User_ID FROM TBL_User
					WHERE User_ID = %s
			)
	'''
	parameter = (User_ID,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)

	results_ = []
	for row in results:
		Wearer_ID = row['Wearer_ID']
		query = '''
			SELECT Device_Temp, Device_HR, Device_O2 FROM TBL_Device
				WHERE Wearer_ID = %s
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		results_ = dictfetchall(Cursor)

		row['User_ID'] = User_ID

		if len(results_) == 0:
			row['Device_Temp'] = 0.0
			row['Device_HR'] = 0
			row['Device_O2'] = 0

		for row_ in results_:
			row['Device_Temp'] = row_['Device_Temp']
			row['Device_HR'] = row_['Device_HR']
			row['Device_O2'] = row_['Device_O2']

		# del row['Wearer_ID']

	return JsonResponse({
		'Vital_Surveillance_Data': results
	})



def Get_Device_Details_Link(Device_Mac, User_ID=None):
	files = get_individual_files()
	Device_Link = None
	for file in files:
		if file == Device_Mac:
			Device_Link = f'http://52.237.83.22:5050/api/v1/app/Get_Device_Details/{Device_Mac}/'

	return Device_Link
	

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Wearers_Details(request, User_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Device_ID, Device_Type FROM TBL_Device
			WHERE Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Wearer
					WHERE User_ID = %s
			)
	'''
	parameter = (User_ID,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)

	# for row in results:
	# 	Device_Mac = row['Device_Mac']
	# 	row['Device_Link'] = Get_Device_Details_Link(Device_Mac, User_ID)

	return JsonResponse({
		'Wearers_Data': results
	})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Alerts_Details(request, User_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Device_ID, Alert_Reading, Alert_Code, Alert_Datetime FROM TBL_Alert
			WHERE Device_ID IN (
				SELECT Device_ID FROM TBL_Device
					WHERE Wearer_ID IN (
						SELECT Wearer_ID FROM TBL_Wearer
							WHERE User_ID = %s
					)
			)
	'''
	parameter = (User_ID,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)
	for row in results:
		Device_ID = row['Device_ID']
		query = '''
			SELECT Wearer_ID, Wearer_Nick FROM TBL_Wearer
			WHERE User_ID IN (
				SELECT User_ID FROM TBL_User
					WHERE User_ID = %s
			) AND Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Device
					WHERE Device_ID = %s
			)
		'''
		parameters = (User_ID, Device_ID)
		Cursor.execute(query, parameters)
		results_ = dictfetchall(Cursor)
		for row_ in results_:
			row['Wearer_Nick'] = row_['Wearer_Nick']





	# query = '''
	# 	SELECT Wearer_ID, Wearer_Nick FROM TBL_Wearer
	# 		WHERE User_ID IN (
	# 			SELECT User_ID FROM TBL_User
	# 				WHERE User_ID = %s
	# 		)
	# '''
	# parameter = (User_ID,)
	# Cursor.execute(query, parameter)
	# results = dictfetchall(Cursor)

	# for row in results:
	# # 	Device_Mac = row['Device_Mac']
	# # 	row['Device_Link'] = Get_Device_Details_Link(Device_Mac, User_ID)
		
	# 	Wearer_ID = row['Wearer_ID']
	# 	query = '''
	# 		SELECT Alert_Reading, Alert_Datetime FROM TBL_Alert
	# 			WHERE Device_ID IN (
	# 				SELECT Device_ID FROM TBL_Device
	# 					WHERE Wearer_ID = %s
	# 			)
	# 	'''
	# 	parameter = (Wearer_ID, )
	# 	Cursor.execute(query, parameter)
	# 	results_ = dictfetchall(Cursor)
	# 	for row_ in results_:
	# 		row['Alert_Reading'] = row_['Alert_Reading']
	# 		row['Alert_Datetime'] =  row_['Alert_Datetime']

	return JsonResponse({
		'Wearers_Alerts': results
	})




def Get_Alert_Type(Alert_Code):
	Type = ''
	Alert_Code=int(Alert_Code)
	if Alert_Code == 1:
		Type = 'High Temperature'
	elif Alert_Code == 2:
		Type = 'Low Temperature'
	elif Alert_Code == 3:
		Type = 'High Oxygen'
	elif Alert_Code == 4:
		Type = 'Low Oxygen'
	elif Alert_Code == 5:
		Type = 'High Heart Rate'
	elif Alert_Code == 6:
		Type = 'Low Heart Rate'
	elif Alert_Code == 7:
		Type = 'Low Battery Level'
	elif Alert_Code == 8:
		Type = 'Breach'

	return Type


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_Alert_Details(request, User_ID, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT * FROM TBL_Alert
			WHERE Device_ID IN (
				SELECT Device_ID FROM TBL_Device
					WHERE Wearer_ID IN (
						SELECT Wearer_ID FROM TBL_Wearer
							WHERE User_ID = %s
					) AND Wearer_ID = %s
			);
	'''
	parameters = (User_ID, Wearer_ID)
	Cursor.execute(query, parameters)
	results = dictfetchall(Cursor)

	for row in results:
		del row['Alert_ID']
		del row["Alert_Date"]
		del row["Alert_Time"]
		# del row["Device_ID"]
		del row["Sent_To_Crest"]
		row['Alert_Code'] = Get_Alert_Type(row['Alert_Code'])

	return JsonResponse({
		'Alerts_Details': results
	})




# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def Quanrantine_Surveillance_Data(request, User_ID):
# 	Connector = mysql.connect(**config)
# 	Cursor = Connector.cursor()

# 	query = '''
# 		SELECT * FROM TBL_Alert
# 			WHERE Device_ID IN (
# 				SELECT Device_ID FROM TBL_Device
# 					WHERE Wearer_ID IN (
# 						SELECT Wearer_ID FROM TBL_Wearer
# 							WHERE User_ID = %s
# 					) AND Wearer_ID = %s
# 			);
# 	'''
# 	parameters = (User_ID, Wearer_ID)
# 	Cursor.execute(query, parameters)
# 	results = dictfetchall(Cursor)

# 	for row in results:
# 		del row['Alert_ID']
# 		del row["Alert_Date"]
# 		del row["Alert_Time"]
# 		# del row["Device_ID"]
# 		del row["Sent_To_Crest"]
# 		row['Alert_Code'] = Get_Alert_Type(row['Alert_Code'])

# 	return JsonResponse({
# 		'Alerts_Details': results
# 	})





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Quanrantine_Surveillance_Data(request, User_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Wearer_ID, Device_Status FROM TBL_Device
			WHERE Device_Type = %s
	'''
	parameter = ('HSWB004', )
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)

	for row in results:
		Wearer_ID = row['Wearer_ID']
		query = '''
			SELECT Wearer_ID, Wearer_Nick FROM TBL_Wearer
				WHERE Wearer_ID = %s OR
					  User_ID = %s
		'''
		parameters = (Wearer_ID, User_ID, )
		Cursor.execute(query, parameters)
		results = dictfetchall(Cursor)

	# query = '''
	# 	SELECT Wearer_ID, Wearer_Nick FROM TBL_Wearer
	# 		WHERE User_ID IN (
	# 			SELECT User_ID FROM TBL_User
	# 				WHERE User_ID = %s
	# 		)
	# '''
	# parameters = (User_ID, )
	# Cursor.execute(query, parameters)
	# results = dictfetchall(Cursor)

	# for row in results:
	# 	Wearer_ID = row['Wearer_ID']
	# 	query = '''
	# 		SELECT Device_Status FROM TBL_Device
	# 			WHERE Wearer_ID = %s AND
	# 			Device_Type = %s
	# 	'''
	# 	parameter = (Wearer_ID, 'HSWB004')
	# 	Cursor.execute(query, parameter)
	# 	results_ = dictfetchall(Cursor)
	# 	for row_ in results_:
	# 		row['Device_Status'] =  row_['Device_Status']

	# 	del row['Wearer_ID']

	return JsonResponse({
		'Quanrantine_Surveillance_Data': results
	})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Support(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	data = json.loads(request.body)
	result = None

	try:
		Wearer_ID = data['Wearer_ID']
		Name = data['Name']
		Email = data['Email']
		Subject = data['Subject']
		Message = data['Message']

		query = '''
			INSERT INTO TBL_Support (Support_ID, Support_Datetime, Name, Email, Subject, Message, Wearer_ID)
			VALUES ((SELECT Create_PK('SUP')), CURRENT_TIMESTAMP(), %s, %s, 
					 %s, %s, %s)
		'''
		parameters = (Name, Email, Subject, Message, Wearer_ID)
		Cursor.execute(query, parameters)
		Connector.commit()
		result = 'Support created successfully'
	except:
		result = 'Support was not created'

	return JsonResponse({
		'Message': result
	})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_User_Message(request, Wearer_ID): #User_ID,
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Message_ID, Message_Description, Message_Date, 
			   Message_Time, Message_Type  FROM TBL_Message
		WHERE Wearer_ID = %s
	'''
	parameters = (Wearer_ID, )
	Cursor.execute(query, parameters)
	results = dictfetchall(Cursor)

	return JsonResponse({
		'Messages': results
	})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Invidual_Quarantine(request, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Breach_ID, Wearer_ID, Breach_St_DateTime, Breach_End_DateTime,
			   TIMESTAMPDIFF(SECOND, Breach_St_DateTime, Breach_End_DateTime) AS
			   Breach_Duration_In_Seconds
		FROM TBL_Breach
		WHERE Wearer_ID = %s
		ORDER BY Breach_St_DateTime DESC
		LIMIT 10
	'''
	parameter = (Wearer_ID, )
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)

	return JsonResponse({
		'Breach_Details': results
	})