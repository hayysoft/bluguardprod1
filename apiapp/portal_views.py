from django.shortcuts import render, redirect
from django.contrib import messages as notification_messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

from .forms import (
	DeviceCreateForm, DeviceUpdateForm,
	WearerCreateForm, WearerUpdateForm,
	GatewayCreateForm, MessageCreateForm,
	SubscriptionCreateForm,
	UserLoginForm, UserUpdateForm,
	CreateWearerForDevice
)
# from .models import (
# 	TblDevice
# )



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



def patient_page(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT * FROM TBL_Crest_Patient
		WHERE Device_Tag IN (
			SELECT Device_Tag FROM TBL_Device
		) AND Q_Device_ID IN (
			SELECT Device_ID FROM TBL_Device
		)
	'''
	Cursor.execute(query)
	results = dictfetchall(Cursor)

	return render(request,
				  'portal/patient/patient.html',
				  {'patients': results})



# def set_Q_Device_and_Q_Start(Device_ID, Patient_ID):
# 	"""
# 		Once user click on Start Then Update tbl patient
# 		Q_Device field for the patient with the Device
# 		ID of the quarantine band AND Q_Start
# 		as CurrentDateTime
# 	"""
# 	Connector = mysql.connect(**config)
# 	Cursor = Connector.cursor()

# 	Device_ID = request.GET.get('Device_ID')
# 	Patient_ID = request.GET.get('Patient_ID')

# 	query = '''
# 		(SELECT )
# 	'''
# 	pass


def set_Q_Device_and_Q_Start(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	Device_ID = request.GET.get('Device_ID')
	Wearer_ID = request.GET.get('Wearer_ID')
	Patient_Tag = request.GET.get('Patient_Tag')
	print(f'Device_ID = {Device_ID}')
	print(f'Wearer_ID = {Wearer_ID}')
	print(f'Patient_Tag = {Patient_Tag}')

	# query = '''
	# 	(SELECT Start_Quarantine(%s, %s))
	# '''
	query = '''
		Update tbl_crest_patient
		set Q_Device_ID = %s,
			Q_Start = CURRENT_TIMESTAMP()
		Where Patient_Tag = %s;
	'''
	if Patient_Tag != '0' or Patient_Tag != '':
		try:
			# print(Patient_Tag)
			parameters = (Device_ID, int(Patient_Tag))
			Cursor.execute(query, parameters)
			Connector.commit()
			# print('Updated')
		except Exception:
			pass
	else:
		# print(Patient_Tag)
		pass

	# query = '''
	# 	UPDATE TBL_Crest_Patient
	# 	SET Q_Device_ID = %s
	# 	WHERE Wearer_ID = %s
	# '''

	# parameter = (Device_ID, Wearer_ID)
	# Cursor.execute(query, parameter)
	# Connector.commit()

	# query = '''
	# 	UPDATE TBL_Crest_Patient
	# 	SET Q_Start = CURRENT_TIMESTAMP()
	# 	WHERE Wearer_ID = %s
	# '''

	# parameter = (Wearer_ID,)
	# Cursor.execute(query, parameter)
	# Connector.commit()

	return JsonResponse({
		'Status': f'Q_Start was updated!'
	})


def set_Q_Device_and_Q_End(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	Device_ID = request.GET.get('Device_ID')
	Wearer_ID = request.GET.get('Wearer_ID')
	Patient_Tag = request.GET.get('Patient_Tag')
	# print(f'Device_ID = {Device_ID}')
	# print(f'Wearer_ID = {Wearer_ID}')
	# print(f'Patient_Tag = {Patient_Tag}')

	query = '''
		Update tbl_crest_patient
		set Q_End = CURRENT_TIMESTAMP()
		Where Patient_Tag = %s;
	'''
	if Patient_Tag != '0' or Patient_Tag != '':
		# print(Patient_Tag)
		try:
			parameters = (int(Patient_Tag),)
			Cursor.execute(query, parameters)
			Connector.commit()

			query = '''
				SELECT Q_Start FROM TBL_Crest_Patient
				WHERE Wearer_ID = %s
			'''
			parameter = (Wearer_ID,)
			Cursor.execute(query, parameter)
			results = dictfetchall(Cursor)
			print('Q_Start:', results)
			print('>< ' * 15)
			print(Wearer_ID)

			if results != []:
				Q_Start = results[0]['Q_Start']

				query =  '''
					UPDATE TBL_Breach
					SET Breach_St_DateTime = %s,
						Breach_End_DateTime = CURRENT_TIMESTAMP(),
						Breach_Duration = TIMEDIFF(CURRENT_TIMESTAMP(),
												   Breach_St_DateTime)
					WHERE Wearer_ID = %s
				'''
				parameter = (Q_Start, Wearer_ID,)
				Cursor.execute(query, parameter)
				Connector.commit()
			else:
				query =  '''
					UPDATE TBL_Breach
					SET Breach_End_DateTime = CURRENT_TIMESTAMP(),
						Breach_Duration = TIMEDIFF(CURRENT_TIMESTAMP(),
												   Breach_St_DateTime)
					WHERE Wearer_ID = %s
				'''
				parameter = (Wearer_ID,)
				Cursor.execute(query, parameter)
				Connector.commit()

			print('Updated')
		except Exception:
			pass
	else:
		# print(Patient_Tag)
		pass


	# query = '''
	# 	UPDATE TBL_Crest_Patient
	# 	SET Q_Device_ID = %s
	# 	WHERE Wearer_ID = %s
	# '''

	# parameter = (Device_ID, Wearer_ID)
	# Cursor.execute(query, parameter)
	# Connector.commit()

	# query = '''
	# 	UPDATE TBL_Crest_Patient
	# 	SET Q_End = CURRENT_TIMESTAMP()
	# 	WHERE Wearer_ID = %s
	# '''

	# parameter = (Wearer_ID,)
	# Cursor.execute(query, parameter)
	# Connector.commit()

	return JsonResponse({
		'Status': 'Q_End was updated!'
	})



def set_to_assigned_unassigned(request, wearer_id):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT Status FROM TBL_Wearer
		WHERE Wearer_ID = %s
	'''
	parameter = (wearer_id,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)
	Status = results[0]['Status']
	Patient_Tag_Status = request.GET.get('Patient_Tag_Status')
	print(f'Patient_Tag_Status = {Patient_Tag_Status}')

	query = '''
		UPDATE TBL_Wearer
		SET Status = %s,
			Patient_Tag_Status = %s
		WHERE wearer_id = %s
	'''
	if results[0].get('Status') == 'Unassigned':
		parameter = ('Assigned', Patient_Tag_Status, wearer_id)
		assigned = True
		Cursor.execute(query, parameter)
		Connector.commit()
	elif results[0].get('Status') == 'Assigned':
		parameter = ('Unassigned', Patient_Tag_Status, wearer_id)
		Cursor.execute(query, parameter)
		Connector.commit()
		assigned = False

	return JsonResponse({
		'Status': parameter,
		'assigned': assigned
	})



def get_individual_files():
	os.chdir('C:/Users/hayysoft/Documents/Scripts/interview/media')
	from glob import glob
	files = glob("*.json")
	files = [file.split('.')[0] for file in files if len(file) == len(file) == 17]
	return files

def invidual_files(request):
	files = get_individual_files()

	return render(request,
				  'portal/individual_devices/display_device.html',
				  {'files': files})



def device_json_display(request, file):
	os.chdir('C:/Users/hayysoft/Documents/Scripts/interview/media')
	files = get_individual_files()
	file = [filename for filename in files if filename == file][0]
	with open(f'{file}.json') as fp:
		file_data = json.loads(fp.read())

	for row in file_data:
		try:
			row['timestamp'] = row['date'] + ' ' + row['time'].split('.')[0]
		except Exception:
			pass

	return render(request,
				  'portal/individual_devices/indi_device.html',
				  {'file_data': file_data[::-1],
				   'files': files,
				   'filename': file})



def invidual_quarantine(request, wearer_id):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		SELECT * FROM TBL_Breach
		WHERE Wearer_ID = %s
		ORDER BY Breach_St_DateTime DESC
	'''
	parameter = (wearer_id,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)

	return render(request,
				  'portal/individual_quarentine/display_quarantine.html',
				  {'wearer_id': wearer_id,
				   'qb_data': results})



def Online_Gateways_API(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
	SELECT Gateway_Status, Gateway_Location, Gateway_Mac, Gateway_Serial_No, Last_Updated_Time
	FROM TBL_Gateway
	'''
	Cursor.execute(query)
	results = dictfetchall(Cursor)

	return JsonResponse({
		'online_gateways': results
	})


@login_required
def Online_Gateways(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
	SELECT Gateway_Location, Gateway_Mac, Gateway_Serial_No, Last_Updated_Time
	FROM TBL_Gateway
	'''
	Cursor.execute(query)
	results = dictfetchall(Cursor)

	return render(request,
				'portal/gateway/online_gateways.html',
				{'online_gateways': results})


def top_five_alerts_api(request):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    def format_time(time):
    	date_, time_ = str(time).split('T')
    	time_ = time_.split('.')
    	datetime_ = date_ + ' ' + time_[0]
    	return datetime_

    if request.user.is_superuser:
    	query = '''
    	SELECT Alert_Datetime, Device_ID, Alert_Reading, Alert_Code
    	FROM tbl_alert ORDER BY Alert_Datetime DESC LIMIT 5;
    	'''
    	Cursor.execute(query)
    else:
    	query = '''
    	SELECT Alert_Datetime, Device_ID, Alert_Reading, Alert_Code
    	FROM tbl_alert
    	WHERE Device_ID IN (
    	SELECT Device_ID FROM TBL_Device
    	WHERE Username = %s
    	)
    	ORDER BY Alert_Datetime DESC LIMIT 5;
    	'''
    	parameter = (request.user.username, )
    	Cursor.execute(query, parameter)

    results = Cursor.fetchall()
    # print(results)

    data = [
        {
            'Alert_Datetime': f'{row[0].date()} {row[0].time()}',
            'Device_ID': row[1],
            'Device_Temp': row[2],
            'Alert_Code': row[3]
        } for row in results
    ]
    for row in data:
    	query = '''
    		SELECT Alert_Description FROM TBL_Alert_Code
    		WHERE Alert_Code = %s
    	'''
    	Alert_Code = row['Alert_Code']
    	parameter = (Alert_Code,)
    	Cursor.execute(query, parameter)
    	results = dictfetchall(Cursor)
    	row['Alert_Description'] = results[0]['Alert_Description']


    	if row['Alert_Code'] == '1':
    		row['vital_icon'] = 'Alert_Icons_Latest/temp_high_alert.png'
    	elif row['Alert_Code'] == '2':
    		row['vital_icon'] = 'Alert_Icons_Latest/temp_high_alert.png'
    	elif row['Alert_Code'] == '3':
    		row['vital_icon'] = 'Alert_Icons_Latest/High_O2-removebg.png'
    	elif row['Alert_Code'] == '4':
    		row['vital_icon'] = 'Alert_Icons_Latest/High_O2-removebg.png'
    	elif row['Alert_Code'] == '5':
    		row['vital_icon'] = 'Alert_Icons_Latest/High_HR-removebg.png'
    	elif row['Alert_Code'] == '6':
    		row['vital_icon'] = 'Alert_Icons_Latest/High_HR-removebg.png'
    	elif row['Alert_Code'] == '7':
    		row['vital_icon'] = 'Alert_Icons_Latest/BatLevel.jpeg'

    	row['device_icon'] ='Alert_Icons_Latest/device_icon.png'

    	Device_ID = row['Device_ID']
    	query = '''
    	SELECT Wearer_ID FROM tbl_device
    	WHERE Device_ID = %s
    	'''
    	parameter = (Device_ID,)
    	Cursor.execute(query, parameter)
    	Fetch_Results = Cursor.fetchall()

    	try:
    		Wearer_ID = Fetch_Results[0][0]
    		query = '''
    			SELECT Wearer_Nick FROM tbl_wearer
    			WHERE Wearer_ID = %s
    		'''
    		parameter = (Wearer_ID,)
    		Cursor.execute(query, parameter)
    		Fetch_Result = Cursor.fetchall()
    		Wearer_Nick = Fetch_Result[0][0]
    		row['Wearer_Nick'] = Wearer_Nick
    	except LookupError:
    		pass

    return JsonResponse({
    	'alerts': data
    })



def qrcode_page(request):
	filepath = 'C:/Users/hayysoft/Documents/APIs/media/BG_Wearer_Crest_v3_2_4_1.apk'
	filename = 'BG_Wearer_Crest_v3_2_4_1.apk'

	path = open(filepath, "rb").read()
	mime_type, _ = mimetypes.guess_type(filepath)
	response = HttpResponse(path, content_type=mime_type)
	response['Content-Disposition'] = f'attachment; filename={filename}'
	return response



def Get_Latest_Alerts(request):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	query = '''
	    SELECT Alert_Date, Alert_Time, Device_ID
	    FROM tbl_alert LIMIT 5;
	'''
	Cursor.execute(query)
	results = Cursor.fetchall()

	data = [
	    {
	        'Alert_Date': row[0],
	        'Alert_Time': row[1],
	        'Device_ID': row[2]
	    } for row in results
	]

	for index, row in enumerate(results):
		Device_ID = row[2]
		query = '''
			SELECT Device_Temp, Wearer_ID FROM tbl_device
			WHERE Device_ID = %s
		'''
		parameter = (Device_ID,)
		Cursor.execute(query, parameter)
		Fetch_Results = Cursor.fetchall()
		Temp = Fetch_Results[0][0]
		data[index]['Device_Temp'] = Temp

		Wearer_ID = Fetch_Results[0][1]
		query = '''
			SELECT Wearer_Nick FROM tbl_wearer
			WHERE Wearer_ID = %s
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		Fetch_Result = Cursor.fetchall()
		Wearer_Nick = Fetch_Result[0][0]
		data[index]['Wearer_Nick'] = Wearer_Nick


	return JsonResponse({
		'data': data
	})



def Fetch_Total_Rows(query):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	Cursor.execute(query)
	results = Cursor.fetchall()
	try:
		results = [result[0] for result in results][0]
	except IndexError:
		results = 0

	return results


def Format_Time(time):
	t = str(time)[4:]
	t = t.replace('H', ':')
	t = t.replace('M', ':')
	t = t.replace('S', '')
	return t


def Fetch_Latest_Alerts():
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	query = '''
	    SELECT Alert_Date, Alert_Time, Device_ID
	    FROM tbl_alert LIMIT 6;
	'''
	Cursor.execute(query)
	results = Cursor.fetchall()

	data = [
	    {
	        'Alert_Date': row[0].strftime('%b %d'),
	        'Alert_Time': row[1],
	        'Device_ID': row[2]
	    } for row in results
	]

	for index, row in enumerate(results):
		Device_ID = row[2]
		query = '''
			SELECT Device_Temp, Wearer_ID FROM tbl_device
			WHERE Device_ID = %s
		'''
		parameter = (Device_ID,)
		Cursor.execute(query, parameter)
		Fetch_Results = Cursor.fetchall()
		Temp = Fetch_Results[0][0]
		data[index]['Device_Temp'] = Temp

		Wearer_ID = Fetch_Results[0][1]
		query = '''
			SELECT Wearer_Nick FROM tbl_wearer
			WHERE Wearer_ID = %s
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		Fetch_Result = Cursor.fetchall()
		Wearer_Nick = Fetch_Result[0][0]
		data[index]['Wearer_Nick'] = Wearer_Nick

	return data


@login_required
def settings_page(request):
	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			data = form.cleaned_data
			username = data.get('username')
			password = data.get('password')
			email = data.get('email')
			first_name = data.get('first_name')
			last_name = data.get('last_name')
			user = User.objects.filter(username=request.user.username)
			if user.exists():
				user = user.first()
				if email != '':
					user.email = email
				if password != '':
					user.set_password(password)
					user.save()
					login(request, user)
				user.save()
				notification_messages.success(request, 'Profile was updated successfully')
	else:
		form = UserUpdateForm(instance=request.user)


	return render(request,
				  'auth/settings.html',
				  {'latest_altert': data,
				   'gateways': gateways,
				   'wearers': wearers,
				   'form': form})

def logout_page(request):
	logout(request)
	return redirect('/login/')


def login_page(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			username = data['username']
			password = data['password']

			user = authenticate(username=username,
								password=password)

			if user is None:
				return redirect('/login/')

			login(request, user)
			return redirect('/vitals/')
	else:
		form = UserLoginForm()

	return render(request,
				  'auth/login.html',
				  {'form': form})


@login_required
def homepage(request):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request, 'homepage.html',
				  {'latest_altert': data,
				   'gateways': gateways,
				   'wearers': wearers,
				   'data_to_display': [], #data_to_display,
				   'user': request.user})



def Gateway_Lat_Lng(request):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()


	query = '''
		SELECT Gateway_Location, Gateway_Address,
			   Gateway_Latitude, Gateway_Longitude
		FROM tbl_gateway;
	'''
	Cursor.execute(query)
	results = Cursor.fetchall()

	gateway_lat_lng = [
		[
			row[0] + ' - ' + row[1],
			row[2],
			row[3]
		] for row in results
	]

	return JsonResponse({
		'lat_lng': gateway_lat_lng
	})



def Lastest_Device_Data(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		# query = '''SELECT * FROM latest_table;'''
		query = '''
			SELECT
		        Device_ID AS Device_ID,
		        Wearer_ID AS Wearer_ID,
		        Device_Temp AS Device_Temp,
		        Device_HR AS Device_HR,
		        Device_O2 AS Device_O2,
		        Device_Last_Updated_Date AS Device_Last_Updated_Date,
		        Device_Last_Updated_Time AS Device_Last_Updated_Time,
		        Incorrect_Data_Flag AS Incorrect_Data_Flag,
		        Device_Status AS Device_Status,
		        Device_Mac AS Device_Mac,
		        Device_Bat_Level AS Device_Bat_Level,
		        Device_Tag AS Device_Tag
		    FROM
		    	TBL_Device
		    WHERE
		        Device_Type <> %s
		    ORDER BY Device_Tag;
		'''
		parameter = ('HSWB004', )
		Cursor.execute(query, parameter)
		# devices = Cursor.fetchall()
	else:
		query = '''
			SELECT
		        Device_ID AS Device_ID,
		        Wearer_ID AS Wearer_ID,
		        Device_Temp AS Device_Temp,
		        Device_HR AS Device_HR,
		        Device_O2 AS Device_O2,
		        Device_Last_Updated_Date AS Device_Last_Updated_Date,
		        Device_Last_Updated_Time AS Device_Last_Updated_Time,
		        Incorrect_Data_Flag AS Incorrect_Data_Flag,
		        Device_Status AS Device_Status,
		        Device_Mac AS Device_Mac,
		        Device_Bat_Level AS Device_Bat_Level,
		        Device_Tag AS Device_Tag
		    FROM
		    	TBL_Device
		    WHERE
		        Device_Type <> %s AND
		        Username = %s
		    ORDER BY Device_Tag;
		'''
		parameters = ('HSWB004', request.user.username)
		Cursor.execute(query, parameters)

	devices = Cursor.fetchall()

	devices_data = []
	for row in devices:
		files = get_individual_files()
		try:
			file = [filename for filename in files if filename == row[9]][0]
			Device_Mac_Link = f'http://52.237.83.22:5050/device_json_display/{row[9]}/'
			Is_Link = True
		except IndexError:
			file = None
			Device_Mac_Link = '#'
			Is_Link = False

		default = lambda obj: obj.isoformat() if isinstance(obj, datetime) else obj
		row_data = {
			'Device_ID': row[0],
			'Wearer_ID': row[1],
			'Device_Temp': row[2],
			'Device_HR': row[3],
			'Device_O2': row[4],
			'Device_Last_Updated_Date': row[5],
			'Device_Last_Updated_Time': row[6],
			'Incorrect_Data_Flag': row[7],
			'Device_Status': row[8],
			'Device_Mac': row[9],
			'Device_Bat_Level': row[10],\
			'Device_Tag': row[11],
			'Device_Mac_Link': Device_Mac_Link,
			'Is_Link': Is_Link
		}
		devices_data.append(row_data)


	for row in devices_data:
		Wearer_ID = row['Wearer_ID']
		query = '''
			SELECT Status FROM TBL_Wearer
			WHERE Wearer_ID = %s
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		results = dictfetchall(Cursor)

		try:
			Status = results[0]['Status']
			row['Status'] = Status
		except LookupError:
			pass

	return JsonResponse({
		'lastest': devices_data
	})



@login_required
def vitals_page(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT Gateway_ID, Gateway_Location FROM tbl_gateway'
	Cursor.execute(query)
	gateways = Cursor.fetchall()
	gateway_data = [
		{'Gateway_ID': row[0],
		 'Gateway_Location': row[1]
		 } for row in gateways
	]

	query = 'SELECT * FROM tbl_wearer'
	Cursor.execute(query)
	wearers = Cursor.fetchall()

	query = '''SELECT * FROM latest_table;'''
	Cursor.execute(query)
	devices = Cursor.fetchall()

	devices_data = [
		{'Device_ID': row[0],
		 'Wearer_ID': row[1],
		 'Device_Temp': row[2],
		 'Device_HR': row[3],
		 'Device_O2': row[4],
		 'Device_Last_Updated_Date': row[5],
		 'Device_Last_Updated_Time': row[6],
		 'Incorrect_Data_Flag': row[7],
		 'Device_Status': row[8],
		 'Device_Mac': row[9],
		 'Device_Bat_Level': row[10],
		 'Device_Serial_No': row[11],
		 'Device_Mac_Link': f'http://52.237.83.22:5050/device_json_display/{row[9]}/'
		 } for row in devices
	]

	query = '''
			SELECT
				Alert_ID,
				Device_ID,
				Alert_Date,
				Alert_Time
			FROM tbl_alert
			'''
	Cursor.execute(query)
	alerts = Cursor.fetchall()
	alerts_data = [
		{'Alert_ID': row[0],
		 'Device_ID': row[1],
		 'Alert_Date': row[2],
		 'Alert_Time': row[3]
		 } for row in alerts
	]

	return render(request, 'vitals.html',
				  {
				   # 'latest_altert': data,
				   'gateways_': gateway_data,
				   'wearers_': wearers,
				   # 'devices_': devices_data,
				   'user': request.user,
				   'value': 'value'})


def Quanrantine_Surveillance_Data(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''
		SELECT
			Device_Status, Device_ID, Device_Last_Updated_Time,
			Device_Last_Updated_Date, Wearer_ID, Device_Tag
		FROM
			TBL_Device
		WHERE
			Device_Type = %s
		ORDER BY Device_Tag;
		'''
		parameter = ('HSWB004', )
		Cursor.execute(query, parameter)
	else:
		query = '''
			SELECT
				Device_Status, Device_ID, Device_Last_Updated_Time,
				Device_Last_Updated_Date, Wearer_ID, Device_Tag
			FROM
				TBL_Device
			WHERE
				Device_Type = %s AND
				Username = %s
			ORDER BY Device_Tag;
		'''
		parameters = ('HSWB004', request.user.username)
		Cursor.execute(query, parameters)

	results = Cursor.fetchall()
	data = [
		{
			'Device_Status': row[0],
			'Device_ID': row[1],
			'Device_Last_Updated_Time': row[2],
			'Device_Last_Updated_Date': row[3],
			'Wearer_ID': row[4],
			'Device_Tag': row[5]
		} for row  in results
	]

	for row in range(len(data)):
		Device_ID = data[row]['Device_ID']
		Wearer_ID = data[row]['Wearer_ID']

		query = '''
			SELECT * FROM TBL_Crest_Patient
			WHERE Patient_Discharged = %s AND Q_Device_ID = %s
		'''
		parameters = (0, 'NA')
		Cursor.execute(query, parameters)
		results = dictfetchall(Cursor)
		data[row][f'Patient_Tag'] = results

		query = '''
			SELECT Patient_Tag FROM TBL_Crest_Patient
			WHERE Q_Device_ID = %s AND
				  Wearer_ID IN (
				  	SELECT Wearer_ID FROM TBL_Wearer
				  	WHERE Status = %s
				)
		'''
		parameter = (Device_ID, 'Assigned')
		Cursor.execute(query, parameter)
		Patient_Tag_Row = dictfetchall(Cursor)
		print(Patient_Tag_Row)
		data[row]['Patient_Tag_Row'] = Patient_Tag_Row


		data[row]['Breach_Link'] = f"http://52.237.83.22:5050/invidual_quarantine/{Wearer_ID}/"
		data[row]['Assign_Unassign'] = f"http://52.237.83.22:5050/set_to_assigned_unassigned/{Wearer_ID}/"
		data[row]['set_Q_Device_and_Q_End'] = f"http://52.237.83.22:5050/set_Q_Device_and_Q_End/?Device_ID={Device_ID}&Wearer_ID={Wearer_ID}&Patient_Tag={'Patient_Tag'}"
		data[row]['set_Q_Device_and_Q_Start'] = f"http://52.237.83.22:5050/set_Q_Device_and_Q_Start/?Device_ID={Device_ID}&Wearer_ID={Wearer_ID}&Patient_Tag={'Patient_Tag'}"

		query = '''
			SELECT Status, Patient_Tag_Status FROM TBL_Wearer
			WHERE Wearer_ID = %s
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		results = dictfetchall(Cursor)
		Status = results[0]['Status']
		data[row]['Patient_Tag_Status'] = results[0]['Patient_Tag_Status']

		if results[0].get('Status') == 'Unassigned':
			data[row]['Assigned'] = False
			data[row]['Background'] = 'green-bg'
		elif results[0].get('Status') == 'Assigned':
			data[row]['Assigned'] = True
			data[row]['Background'] = 'red-bg'

		query = '''
			SELECT Wearer_Nick FROM tbl_wearer
			WHERE Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Device
				WHERE Wearer_ID = %s
			)
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		results = Cursor.fetchall()
		try:
			Wearer_Nick = results[0][0]
			data[row]['Wearer_Nick'] = Wearer_Nick
		except Exception:
			pass

		query = '''
			SELECT Alert_ID FROM TBL_Alert
			WHERE Device_ID IN (
				SELECT Device_ID FROM TBL_Device
				WHERE Device_ID = %s
			)
		'''
		parameter = (Device_ID,)
		Cursor.execute(query, parameter)
		results = Cursor.fetchall()
		try:
			Alert_ID = results[0][0]
			data[row]['Alert_ID'] = Alert_ID
		except Exception:
			pass


		query = '''
			SELECT Quarantine_Start_Date, Quarantine_End_Date FROM TBL_Quarantine
			WHERE Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Device
				WHERE Wearer_ID = %s
			)
		'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		results = Cursor.fetchall()
		try:
			Quarantine_Start_Date = results[0][0]
			Quarantine_End_Date = results[0][1]
			data[row]['Quarantine_Start_Date'] = Quarantine_Start_Date
			data[row]['Quarantine_End_Date'] = Quarantine_End_Date
			Time_Diff = Quarantine_End_Date - Quarantine_Start_Date
			data[row]['Time_Diff'] = f'{Time_Diff}'
		except Exception:
			pass

	return JsonResponse({
		'surveillance': data
	})



@login_required
def quanrentine_surveilance_page(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	return render(request, 'quanrentine_surveilance.html',
				  {'user': request.user})



@login_required
def communication(request):
	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data = response.json()['Alert'][:5]

	url = 'http://52.237.83.22:5050/get-messages/'
	response = requests.get(url)
	messages = response.json()['Message']

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request, 'communication.html',
				 {'latest_altert': data,
				  'gateways': gateways,
				  'wearers': wearers,
				  'messages': messages,
				  })
				  # })

@login_required
def messages(request):
	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request, 'messages.html',
				 {'latest_altert': data,
				  'gateways': gateways,
				  'wearers': wearers})



def Get_All_Device_For_Portal(request):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	# query = 'SELECT * FROM tbl_device'
	if request.user.is_superuser:
		query = '''SELECT * FROM latest_table;'''
		Cursor.execute(query)
		devices = Cursor.fetchall()
	else:
		query = '''
			SELECT
		        Device_ID AS Device_ID,
		        Wearer_ID AS Wearer_ID,
		        Device_Temp AS Device_Temp,
		        Device_HR AS Device_HR,
		        Device_O2 AS Device_O2,
		        Device_Last_Updated_Date AS Device_Last_Updated_Date,
		        Device_Last_Updated_Time AS Device_Last_Updated_Time,
		        Incorrect_Data_Flag AS Incorrect_Data_Flag,
		        Device_Status AS Device_Status,
		        Device_Mac AS Device_Mac,
		        Device_Bat_Level AS Device_Bat_Level,
		        Device_Tag AS Device_Tag
		    FROM
		    	TBL_Device
		    WHERE
		        Device_Type <> %s AND
		        Username = %s
		'''
		parameters = ('HSWB004', request.user.username)
		Cursor.execute(query, parameters)
	# Cursor.execute(query)

	results = Cursor.fetchall()
	data = [
		{
			'Device_ID': row[0],
			'Device_Type': row[1],
			'Device_Serial_No': row[2],
			'Device_Mac': row[3],
			'Device_Bat_Level': row[4],
			'Device_Last_Updated_Date': row[5], #.strftime("%b %d"),
			'Wearer_ID': row[7],
			'Device_Temp': row[8],
			'Device_HR': row[9],
			'Device_O2': row[10]
		} for row in results
	]

	return JsonResponse({
		'Device': data
	})


@login_required
def Device_View(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''SELECT * FROM latest_table;'''
		Cursor.execute(query)
	else:
		query = '''
			SELECT
		        Device_ID AS Device_ID,
		        Wearer_ID AS Wearer_ID,
		        Device_Type AS Device_Type,
		        Device_Serial_No AS Device_Serial_No,
		        Device_Temp AS Device_Temp,
		        Device_HR AS Device_HR,
		        Device_O2 AS Device_O2,
		        Device_Last_Updated_Date AS Device_Last_Updated_Date,
		        Device_Last_Updated_Time AS Device_Last_Updated_Time,
		        Incorrect_Data_Flag AS Incorrect_Data_Flag,
		        Device_Status AS Device_Status,
		        Device_Mac AS Device_Mac,
		        Device_Bat_Level AS Device_Bat_Level,
		        Device_Tag AS Device_Tag
		    FROM
		    	TBL_Device
		    WHERE
		        Device_Type <> %s AND
		        Username = %s
		'''
		parameters = ('HSWB004', request.user.username)
		Cursor.execute(query, parameters)

	results = dictfetchall(Cursor)

	data1 = [
		{
			'Device_ID': row['Device_ID'],
			'Device_Type': row['Device_Type'],
			'Device_Serial_No': row['Device_Serial_No'],
			'Device_Mac': row['Device_Mac'],
			'Device_Bat_Level': row['Device_Bat_Level'],
			'Device_Last_Updated_Date': row['Device_Last_Updated_Date'],
			'Wearer_ID': row['Wearer_ID'],
			'Device_Temp': row['Device_Temp'],
			'Device_HR': row['Device_HR'],
			'Device_O2': row['Device_O2'],
		} for row in results
	]


	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')


	return render(request,
				  'portal/device/device.html',
				  {
				  	'note': 'Device Page',
				   	'data': data1,
				   	'gateways': gateways,
				   	'wearers': wearers,
				   })


def Device_Confirm(request, Device_Type, Device_Serial_No, Device_Mac):
	Wearer_ID = None
	if request.method == 'POST':
		form = CreateWearerForDevice(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Wearer_ID = data['Wearer_ID']
			return redirect(f'/Device_Confirm_Create/{Device_Type}/{Device_Serial_No}/{Device_Mac}/{Wearer_ID}/')
	else:
		form = CreateWearerForDevice()

	return render(request,
				  'portal/device/device_confirm.html',
				  {'Device_Type': Device_Type,
				   'Device_Serial_No': Device_Serial_No,
				   'Device_Mac': Device_Mac,
				   'Wearer_ID': Wearer_ID,
				   'form': form})


def Device_Confirm_Create(request, Device_Type, Device_Serial_No,
						  Device_Mac, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		INSERT INTO tbl_device (Device_ID, Device_Type,
	   	Device_Serial_No, Device_Mac, Device_Last_Updated_Date,
	   	Device_Last_Updated_Time, Wearer_ID, Username)
	   	VALUES ((SELECT Create_PK("DVC")), %s, %s, %s,
	   			 CURDATE(), CURTIME(), %s, %s)
	'''
	parameters = (Device_Type, Device_Serial_No,
				  Device_Mac, Wearer_ID, request.user.username)
	Cursor.execute(query, parameters)
	Connector.commit()
	return redirect('/device/')



@login_required
def Device_Create(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = DeviceCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Device_Type = data.get('Device_Type')
			Device_Serial_No = data.get('Device_Serial_No')
			Device_Mac = data.get('Device_Mac')
			return redirect(f'/device-confirm/{Device_Type}/{Device_Serial_No}/{Device_Mac}/')
	else:
		form = DeviceCreateForm()


	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/device/create_device.html',
				  {'form': form,
				   'gateways': gateways,
				   'wearers': wearers})

@login_required
def Device_Update(request, Device_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT * FROM tbl_device
			   WHERE Device_ID = %s'''
	parameter = (Device_ID,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)
	device_data = results[0]

	if request.method == 'POST':
		form = DeviceUpdateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Device_Type = data['Device_Type']
			Device_Serial_No = data['Device_Serial_No']
			Device_Mac = data['Device_Mac']
			Gateway_Mac = data['Gateway_Mac']
			Device_Status = data['Device_Status']
			Device_Tag = data['Device_Tag']

			query = '''
				UPDATE  tbl_device
			   	SET Device_Type = %s,
			   		Device_Serial_No = %s,
			   		Device_Mac = %s,
			   		Gateway_Mac = %s,
			   		Device_Status = %s,
			   		Device_Tag = %s
			   	WHERE Device_ID = %s'''
			parameters = (Device_Type, Device_Serial_No,
						  Device_Mac, Gateway_Mac, Device_Status,
						  Device_Tag, Device_ID)
			Cursor.execute(query, parameters)
			Connector.commit()
	else:
		form = DeviceUpdateForm(initial={
			'Device_Type': device_data['Device_Type'],
			'Device_Serial_No': device_data['Device_Serial_No'],
			'Device_Mac': device_data['Device_Mac'],
			'Gateway_Mac': device_data['Gateway_Mac'],
			'Device_Status': device_data['Device_Status'],
			'Device_Tag': device_data['Device_Tag']
		})


	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'portal/device/update_device.html',
				  {'results': Device_ID,
				   'form': form,
				   'gateways': gateways,
				   'wearers': wearers})


def Device_Delete(request, Device_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''SELECT Device_ID FROM tbl_device
			   WHERE Device_ID = %s'''
		parameter = (Device_ID, )
		Cursor.execute(query, parameter)
	else:
		query = '''SELECT Device_ID FROM tbl_device
				   WHERE Device_ID = %s AND
			        	 Username = %s'''
		parameters = (Device_ID, request.user.username)
		Cursor.execute(query, parameters)

	results = Cursor.fetchone()

	try:
		Device_ID = results[0]
		if request.user.is_superuser:
			query = '''DELETE FROM tbl_device
				   WHERE Device_ID = %s'''
			parameter = (Device_ID, )
			Cursor.execute(query, parameter)
		else:
			query = '''DELETE FROM tbl_device
					   WHERE Device_ID = %s AND
			        	 Username = %s'''
			parameters = (Device_ID, request.user.username)
			Cursor.execute(query, parameters)

		Connector.commit()
		notification_messages.success(request, f'Device_ID = {Device_ID} was deleted successfully.')
		return redirect('/device/')
	except TypeError:
		notification_messages.warning(request, f'Device_ID = {Device_ID} does not exist.')
		return redirect('/device/')

	return redirect('/device/')




def Get_All_Wearer_For_Portal(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''SELECT * FROM tbl_wearer;'''
		Cursor.execute(query)
	else:
		query = '''SELECT * FROM tbl_wearer
				   WHERE Username = %s
		'''
		parameter = (request.user.username,)
		Cursor.execute(query, parameter)

	results = Cursor.fetchall()

	data = [
		{
			'Wearer_ID': row[0],
			'Wearer_Nick': row[1]
		} for row in results
	]

	return JsonResponse({
		'Wearer': data
	})


@login_required
def Wearer_View(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''SELECT * FROM tbl_wearer;'''
		Cursor.execute(query)
	else:
		query = '''SELECT * FROM tbl_wearer
				   WHERE Username = %s
		'''
		parameter = (request.user.username,)
		Cursor.execute(query, parameter)

	results = Cursor.fetchall()

	data = [
		{
			'Wearer_ID': row[0],
			'Wearer_Nick': row[1]
		} for row in results
	]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'portal/wearer/wearer.html',
				  {'note': 'Device Page',
				   'data': data,
				   'gateways': gateways,
				   'wearers': wearers})



def Wearer_Confirm(request, Wearer_Nick, Wearer_Pwd):
	if request.method == 'POST':
		return redirect(f'/Wearer_Confirm_Create/{Wearer_Nick}/{Wearer_Pwd}/')

	return render(request,
				  'portal/wearer/wearer_confirm.html',
				  {'Wearer_Nick': Wearer_Nick,
				   'Wearer_Pwd': Wearer_Pwd})


def Wearer_Confirm_Create(request, Wearer_Nick, Wearer_Pwd):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		INSERT INTO tbl_wearer (Wearer_ID, Wearer_Nick,
		Wearer_Pwd, Status, Patient_Tag_Status, Username)
	   	VALUES ((SELECT Create_PK("WER")), %s, %s, %s, %s, %s)'''
	parameters = (Wearer_Nick, Wearer_Pwd,
				  'Unassigned', 'NA', request.user.username)
	Cursor.execute(query, parameters)
	Connector.commit()
	return redirect('/wearer/')




@login_required
def Wearer_Create(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = WearerCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			print(data)
			Wearer_Nick = data.get('Wearer_Nick')
			Wearer_Pwd = data.get('Wearer_Pwd')
			return redirect(f'/Wearer_Confirm/{Wearer_Nick}/{Wearer_Pwd}/')
	else:
		form = WearerCreateForm()


	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/wearer/create_wearer.html',
				  {'form': form,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Wearer_Update(request, Wearer_Nick):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT * FROM tbl_wearer
			   WHERE Wearer_Nick = %s'''
	parameter = (Wearer_Nick,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)

	if request.method == 'POST':
		form = WearerUpdateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Wearer_Nick = data.get('Wearer_Nick')
			Wearer_Pwd = data.get('Wearer_Pwd')
			Status = data.get('Status')
			Patient_Tag_Status = data.get('Patient_Tag_Status')

			query = '''
				UPDATE  tbl_wearer
			   	SET Wearer_Nick = %s,
			   		Wearer_Pwd = %s,
			   		Status = %s,
			   		Patient_Tag_Status = %s
			   	WHERE Wearer_Nick = %s'''
			parameters = (Wearer_Nick, Wearer_Pwd, Status,
						  Patient_Tag_Status, Wearer_Nick)
			Cursor.execute(query, parameters)
			Connector.commit()
	else:
		form = WearerUpdateForm(initial=results[0])

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'portal/wearer/update_wearer.html',
				  {
				   'form': form,
				   'Wearer_Nick': Wearer_Nick,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Wearer_Delete(request, Wearer_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''SELECT Wearer_ID FROM tbl_wearer
				   WHERE Wearer_ID = %s'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
	else:
		query = '''SELECT Wearer_ID FROM tbl_wearer
			   WHERE Wearer_ID = %s AND
			   		 Username = %s'''
		parameters = (Wearer_ID, request.user.username)
		Cursor.execute(query, parameters)

	results = Cursor.fetchone()
	try:
		Wearer_ID = results[0]
		query = '''DELETE FROM TBL_Device
				   WHERE Wearer_ID = %s'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()

		query = '''DELETE FROM tbl_wearer
				   WHERE Wearer_ID = %s'''
		parameter = (Wearer_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()
		notification_messages.success(request, f'Wearer_ID = {Wearer_ID} was deleted successfully.')
		return redirect('/wearer/')
	except TypeError:
		notification_messages.warning(request, f'Wearer_ID = {Wearer_ID} does not exist.')
		return redirect('/wearer/')

	return redirect('/wearer/')




def Get_All_Gateway_For_Portal(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = 'SELECT * FROM tbl_gateway'
		Cursor.execute(query)
	else:
		query = '''SELECT * FROM tbl_gateway
				   WHERE Username = %s'''
		parameter = (request.user.username,)
		Cursor.execute(query, parameter)

	results = Cursor.fetchall()
	data = [
		{
			'Gateway_ID': row[0],
			'Gateway_Location': row[1],
			'Gateway_Address': row[2],
			'Gateway_Mac': row[3],
			'Gateway_Serial_No': row[4],
			'Gateway_Topic': row[5],
			'Gateway_Latitude': row[6],
			'Gateway_Longitude': row[7],
			'Gateway_Type': row[8],
		} for row in results
	]

	return JsonResponse({
		'Gateway': data
	})


@login_required
def Gateway_View(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = 'SELECT * FROM tbl_gateway'
		Cursor.execute(query)
	else:
		query = '''SELECT * FROM tbl_gateway
				   WHERE Username = %s'''
		parameter = (request.user.username,)
		Cursor.execute(query, parameter)

	results = Cursor.fetchall()
	data = [
		{
			'Gateway_ID': row[0],
			'Gateway_Location': row[1],
			'Gateway_Address': row[2],
			'Gateway_Mac': row[3],
			'Gateway_Serial_No': row[4],
			'Gateway_Topic': row[5],
			'Gateway_Latitude': row[6],
			'Gateway_Longitude': row[7],
			'Gateway_Type': row[8],
		} for row in results
	]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/gateway/gateway.html',
				  {'note': 'Device Page',
				   'data': data,
				   # 'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


def Gateway_Confirm(request, Gateway_Location, Gateway_Address, Gateway_Mac,
					Gateway_Serial_No, Gateway_Topic, Gateway_Latitude,
					Gateway_Longitude, Gateway_Type):

	if request.method == 'POST':
		return redirect(f'/Gateway_Confirm_Create/{Gateway_Location}/{Gateway_Address}/{Gateway_Mac}/{Gateway_Serial_No}/{Gateway_Topic}/{Gateway_Latitude}/{Gateway_Longitude}/{Gateway_Type}/')

	return render(request,
				  'portal/gateway/gateway_confirm.html',
				  {'Gateway_Location': Gateway_Location,
				   'Gateway_Address': Gateway_Address,
				   'Gateway_Mac': Gateway_Mac,
				   'Gateway_Serial_No': Gateway_Serial_No,
				   'Gateway_Topic': Gateway_Topic,
				   'Gateway_Latitude': Gateway_Latitude,
				   'Gateway_Longitude': Gateway_Longitude,
				   'Gateway_Type': Gateway_Type})


def Gateway_Confirm_Create(request, Gateway_Location, Gateway_Address, Gateway_Mac,
						   Gateway_Serial_No, Gateway_Topic, Gateway_Latitude,
						   Gateway_Longitude, Gateway_Type):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
		INSERT INTO tbl_gateway
		(Gateway_ID, Gateway_Location,
	   	Gateway_Address, Gateway_Mac, Gateway_Serial_No,
	   	Gateway_Topic, Gateway_Latitude, Gateway_Longitude,
	   	Gateway_Type, Username)
	   	VALUES ((SELECT Create_PK("GTE")), %s, %s, %s, %s,
	   			 %s, %s, %s, %s, %s)'''
	parameters = (Gateway_Location,
	   			  Gateway_Address, Gateway_Mac, Gateway_Serial_No,
	   			  Gateway_Topic, Gateway_Latitude, Gateway_Longitude,
	   			  Gateway_Type, request.user.username)
	Cursor.execute(query, parameters)
	Connector.commit()
	return redirect('/gateway/')



@login_required
def Gateway_Create(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = GatewayCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Gateway_Location = data.get('Gateway_Location')
			Gateway_Address = data.get('Gateway_Address')
			Gateway_Mac = data.get('Gateway_Mac')
			Gateway_Serial_No = data.get('Gateway_Serial_No')
			Gateway_Topic = data.get('Gateway_Topic')
			Gateway_Latitude = data.get('Gateway_Latitude')
			Gateway_Longitude = data.get('Gateway_Longitude')
			Gateway_Type = data.get('Gateway_Type')
			return redirect(f'/Gateway_Confirm/{Gateway_Location}/{Gateway_Address}/{Gateway_Mac}/{Gateway_Serial_No}/{Gateway_Topic}/{Gateway_Latitude}/{Gateway_Longitude}/{Gateway_Type}/')
	else:
		form = GatewayCreateForm(initial={
			'Gateway_Location': 'Malaysia', 'Gateway_Address': 'Malaysia',
			'Gateway_Mac': 'Testing', 'Gateway_Serial_No':  '1234',
			'Gateway_Topic': 'Testing', 'Gateway_Latitude': 12.3456,
			'Gateway_Longitude': 6.8235, 'Gateway_Type': 'Testing'
		})

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/gateway/create_gateway.html',
				  {'form': form,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Gateway_Update(request, Gateway_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT * FROM tbl_gateway
			   WHERE Gateway_ID = %s'''
	parameter = (Gateway_ID,)
	Cursor.execute(query, parameter)
	results = dictfetchall(Cursor)
	gateway_data = results[0]
	print(gateway_data)

	if request.method == 'POST':
		form = GatewayCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Gateway_Location = data.get('Gateway_Location')
			Gateway_Address = data.get('Gateway_Address')
			Gateway_Mac = data.get('Gateway_Mac')
			Gateway_Serial_No = data.get('Gateway_Serial_No')
			Gateway_Topic = data.get('Gateway_Topic')
			Gateway_Latitude = data.get('Gateway_Latitude')
			Gateway_Longitude = data.get('Gateway_Longitude')
			Gateway_Type = data.get('Gateway_Type')

			query = '''
				UPDATE  tbl_gateway
			   	SET Gateway_Location = %s,
			   		Gateway_Address = %s,
			   		Gateway_Mac = %s,
			   		Gateway_Serial_No = %s,
			   		Gateway_Topic = %s,
			   		Gateway_Latitude = %s,
			   		Gateway_Longitude = %s,
			   		Gateway_Type = %s
			   	WHERE Gateway_ID = %s'''
			parameters = (Gateway_Location,
			   			  Gateway_Address, Gateway_Mac, Gateway_Serial_No,
			   			  Gateway_Topic, Gateway_Latitude, Gateway_Longitude,
			   			  Gateway_Type, Gateway_ID)
			Cursor.execute(query, parameters)
			Connector.commit()
	else:
		form = GatewayCreateForm(initial={
			'Gateway_Location': gateway_data['Gateway_Location'],
		   	'Gateway_Address': gateway_data['Gateway_Address'],
		   	'Gateway_Mac': gateway_data['Gateway_Mac'],
		   	'Gateway_Serial_No': gateway_data['Gateway_Serial_No'],
		   	'Gateway_Topic': gateway_data['Gateway_Topic'],
		   	'Gateway_Latitude': gateway_data['Gateway_Latitude'],
		   	'Gateway_Longitude': gateway_data['Gateway_Longitude'],
		   	'Gateway_Type': gateway_data['Gateway_Type']
		})

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'portal/gateway/update_gateway.html',
				  {'results': Gateway_ID,
				   'form': form,
				   'gateways': gateways,
				   'wearers': wearers})



def Gateway_Delete(request, Gateway_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.user.is_superuser:
		query = '''SELECT Gateway_ID FROM tbl_gateway
				   WHERE Gateway_ID = %s'''
		parameter = (Gateway_ID,)
		Cursor.execute(query, parameter)
	else:
		query = '''SELECT Gateway_ID FROM tbl_gateway
				   WHERE Gateway_ID = %s AND
				   		 Username = %s'''
		parameters = (Gateway_ID, request.user.username)
		Cursor.execute(query, parameters)

	results = Cursor.fetchone()
	try:
		Gateway_ID = results[0]
		query = '''DELETE FROM tbl_gateway
				   WHERE Gateway_ID = %s'''
		parameter = (Gateway_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()
		notification_messages.success(request, f'Gateway_ID = {Gateway_ID} was deleted successfully.')
		return redirect('/gateway/')
	except TypeError:
		notification_messages.warning(request, f'Gateway_ID = {Gateway_ID} does not exist.')
		return redirect('/gateway/')

	return redirect('/gateway/')





def Get_All_Message_For_Portal(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT * FROM TBL_Message'
	Cursor.execute(query)

	results = Cursor.fetchall()
	data = [
		{
			'Message_ID': row[0],
			'Message_Description': row[1],
			'Message_Date': row[2],
			'Message_Time': row[3],
			'Message_Type': row[4],
			'User_ID': row[5]
		} for row in results
	]

	return JsonResponse({
		'Message': data
	})


@login_required
def Message_View(request):
	url = 'http://52.237.83.22:5050/get-messages/'
	response = requests.get(url)
	data = response.json()['Message']

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/message/message.html',
				  {'note': 'Message Page',
				   'data': data,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Message_Create(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = MessageCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Message_Description = data.get('Message_Description')
			Message_Date = data.get('Message_Date')
			Message_Time = data.get('Message_Time')
			Message_Type = data.get('Message_Type')
			User_ID = data.get('User_ID')
			query = '''
				INSERT INTO TBL_Message
				(Message_ID, Message_Description,
			   	Message_Date, Message_Time, Message_Type,
			   	User_ID)
			   	VALUES ((SELECT Create_PK("MSG")), %s, %s, %s, %s, %s)'''
			parameters = (Message_Description,
			   			  Message_Date, Message_Time, Message_Type,
			   			  User_ID)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/message/')
	else:
		form = MessageCreateForm()

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'portal/message/create_message.html',
				  {'form': form,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Message_Delete(request, Message_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT Message_ID FROM TBL_Message
			   WHERE Message_ID = %s'''
	parameter = (Message_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Wearer_ID = results[0]
		query = '''DELETE FROM TBL_Message
				   WHERE Message_ID = %s'''
		parameter = (Message_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()
		notification_messages.success(request, f'Message_ID = {Message_ID} was deleted successfully.')
		return redirect('/message/')
	except TypeError:
		notification_messages.warning(request, f'Message_ID = {Message_ID} does not exist.')
		return redirect('/message/')

	return redirect('/message/')




def Get_All_Subscription_For_Portal(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT * FROM tbl_subscription'
	Cursor.execute(query)

	results = Cursor.fetchall()
	data = [
		{
			'Subscription_ID': row[0],
			'User_ID': row[1],
			'Device_ID': row[2],
			'Subscription_Created_Date': row[3],
			'Subscription_Created_Time': row[4]
		} for row in results
	]

	return JsonResponse({
		'Subscription': data
	})


@login_required
def Subscription_View(request):
	url = 'http://52.237.83.22:5050/subscriptions/'
	response = requests.get(url)
	data = response.json()['Subscription']

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/subscription/subscription.html',
				  {'note': 'Message Page',
				   'data': data,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Subscription_Create(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = SubscriptionCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			User_ID = data.get('User_ID')
			Device_ID = data.get('Device_ID')
			Subscription_Created_Date = data.get('Subscription_Created_Date')
			Subscription_Created_Time = data.get('Subscription_Created_Time')
			query = '''
				INSERT INTO tbl_subscription
				(Subscription_ID, User_ID,
			   	Device_ID, Subscription_Created_Date,
			   	Subscription_Created_Time)
			   	VALUES ((SELECT Create_PK("SUBS")), %s, %s, %s, %s)'''
			parameters = (User_ID,
			   			  Device_ID, Subscription_Created_Date,
			   			  Subscription_Created_Time)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/subscription/')
	else:
		form = SubscriptionCreateForm()

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/subscription/create_subscription.html',
				  {'form': form,
				   'gateways': gateways,
				   'wearers': wearers})



def Subscription_Delete(request, Subscription_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT Subscription_ID FROM tbl_subscription
			   WHERE Subscription_ID = %s'''
	parameter = (Subscription_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Subscription_ID = results[0]
		query = '''DELETE FROM tbl_subscription
				   WHERE Subscription_ID = %s'''
		parameter = (Subscription_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()
		notification_messages.success(request, f'Subscription_ID = {Subscription_ID} was deleted successfully.')
		return redirect('/subscription/')
	except TypeError:
		notification_messages.warning(request, f'Subscription_ID = {Subscription_ID} does not exist.')
		return redirect('/subscription/')

	return redirect('/subscription/')




def Get_All_Alert_For_Portal(request):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT * FROM TBL_Alert;'
	Cursor.execute(query)

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


@login_required
def Alert_View(request):
	query = 'SELECT * FROM TBL_Alert;'
	Cursor.execute(query)

	results = Cursor.fetchall()
	data = [
		{
			'Alert_ID': row[0],
			'Alert_Code': row[1],
			'Alert_Date': row[2],
			'Alert_Time': str(row[3]),
			'Device_ID': row[4]
		} for row in results
	]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'portal/alert/alert.html',
				  {'note': 'Alert Page',
				   'data': data,
				   'gateways': gateways,
				   'wearers': wearers})



def Alert_Delete(request, Alert_ID):
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''SELECT Alert_ID FROM TBL_Alert
			   WHERE Alert_ID = %s'''
	parameter = (Alert_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Alert_ID = results[0]
		query = '''DELETE FROM TBL_Alert
				   WHERE Alert_ID = %s'''
		parameter = (Alert_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()
		notification_messages.success(request, f'Alert_ID = {Alert_ID} was deleted successfully.')
		return redirect('/alert/')
	except TypeError:
		notification_messages.warning(request, f'Alert_ID = {Alert_ID} does not exist.')
		return redirect('/alert/')

	return redirect('/alert/')


@login_required
def Latest_Alerts_View(request):
	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')

	return render(request,
				  'latest_alert.html',
				  {'note': 'Alert Page',
				   'data': data,
				   'gateways': gateways,
				   'wearers': wearers})


