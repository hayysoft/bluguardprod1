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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def Get_User_Wearers(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	data = json.loads(request.body)
	User_ID = data['User_ID']

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
		for row_ in results_:
			row['Device_Temp'] = row_['Device_Temp']
			row['Device_HR'] = row_['Device_HR']
			row['Device_O2'] = row_['Device_O2']

	return JsonResponse({
		'Wearer_Data': results
	})
