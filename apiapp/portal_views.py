from django.shortcuts import render, redirect
from django.contrib import messages as notification_messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
	authenticate, login, logout
)
from django.utils.safestring import mark_safe
from django.http import JsonResponse

import os
import json
import random
import requests
from datetime import datetime
import mysql.connector as mysql

from .forms import (
	DeviceCreateForm, DeviceUpdateForm,
	WearerCreateForm, WearerUpdateForm,
	GatewayCreateForm, MessageCreateForm,
	SubscriptionCreateForm,
	UserLoginForm, UserUpdateForm
)


Connector = mysql.connect(
	user=os.getenv('BluguardDB_User'),
	password=os.getenv('BluguardDB_Pwd'),
	host='localhost',
	port=os.getenv('BluguardDB_Port'),
	database=os.getenv('BluguardDB_Name')
)

Cursor = Connector.cursor()



def Get_Latest_Alerts(request):
	Connector = mysql.connect(
	    user=os.getenv('BluguardDB_User'),
	    password=os.getenv('BluguardDB_Pwd'),
	    host='localhost',
	    port=os.getenv('BluguardDB_Port'),
	    database=os.getenv('BluguardDB_Name')
	)

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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
			return redirect('/')
	else:
		form = UserLoginForm()

	return render(request,
				  'auth/login.html',
				  {'form': form})


@login_required
def homepage(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
				   'value': 'value'})



def Gateway_Lat_Lng(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

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
		 'Device_Serial_No': row[11]
		 } for row in devices
	]

	return JsonResponse({
		'lastest': devices_data
	})



@login_required
def vitals_page(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data = response.json()['Alert'][:5]

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
		 'Device_Serial_No': row[11]
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
				  {'latest_altert': data,
				   'gateways_': gateway_data,
				   'wearers_': wearers,
				   'devices_': devices_data,
				   'alerts_': alerts_data,
				   'value': 'value'})


def Quanrantine_Surveillance_Data(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()
	query = 'SELECT * FROM surveillance_page;'
	Cursor.execute(query)
	results = Cursor.fetchall()
	data = [
		{
			'Device_Status': row[0],
			'Device_ID': row[1],
			'Device_Last_Updated_Time': row[2],
			'Device_Last_Updated_Date': row[3],
			'Wearer_ID': row[4]
		} for row  in results
	]

	for row in range(len(data)):
		Device_ID = data[row]['Device_ID']
		Wearer_ID = data[row]['Wearer_ID']
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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()



	return render(request, 'quanrentine_surveilance.html',
				  {})



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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = 'SELECT * FROM tbl_device'
	Cursor.execute(query)

	results = Cursor.fetchall()
	data = [
		{
			'Device_ID': row[0],
			'Device_Type': row[1],
			'Device_Serial_No': row[2],
			'Device_Mac': row[3],
			'Device_Bat_Level': row[4],
			'Device_Last_Updated_Date': row[5].strftime("%b %d"),
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
	url = 'http://52.237.83.22:5050/devices/'
	response = requests.get(url)
	data1 = response.json()['Device']

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/device/device.html',
				  {'note': 'Device Page',
				   'data': data1,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Device_Create(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = DeviceCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Device_Type = data.get('Device_Type')
			Device_Serial_No = data.get('Device_Serial_No')
			Device_Mac = data.get('Device_Mac')
			query = '''
				INSERT INTO tbl_device (Device_ID, Device_Type,
			   	Device_Serial_No, Device_Mac, Device_Bat_Level,
			   	Device_Last_Updated_Date, Device_Last_Updated_Time,
			   	Wearer_ID, Device_Temp, Device_HR, Device_O2,
			   	Incoming_Id, Device_RSSI, Gateway_Mac,
			   	Device_Status, Device_Tag)
			   	VALUES ((SELECT Create_PK("DVC")), %s, %s, %s, NULL, CURDATE(),
			   			 NULL, NULL,
			   			 NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)'''
			parameters = (Device_Type, Device_Serial_No, Device_Mac)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/device/')
	else:
		form = DeviceCreateForm()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/device/create_device.html',
				  {'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})

@login_required
def Device_Update(request, Device_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = '''SELECT Device_ID FROM tbl_device
			   WHERE Device_ID = %s'''
	parameter = (Device_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Device_ID = results[0]
	except TypeError:
		notification_messages.warning(request, f'Device_ID = {Device_ID} does not exist.')
		return redirect('/device/')

	if request.method == 'POST':
		form = DeviceUpdateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Device_Last_Updated_Date = data.get('Device_Last_Updated_Date')
			Device_Last_Updated_Time = data.get('Device_Last_Updated_Time')
			Device_Temp = data.get('Device_Temp')
			Device_HR = data.get('Device_HR')
			Device_O2 = data.get('Device_O2')

			query = '''
				UPDATE  tbl_device
			   	SET Device_Last_Updated_Date = %s,
			   		Device_Last_Updated_Time = %s,
			   		Device_Temp = %s,
			   		Device_HR = %s,
			   		Device_O2 = %s
			   	WHERE Device_ID = %s'''
			parameters = (Device_Last_Updated_Date, Device_Last_Updated_Time,
						  Device_Temp, Device_HR, Device_O2, Device_ID)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/device/')
	else:
		form = DeviceUpdateForm()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/device/update_device.html',
				  {'results': Device_ID,
				   'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


def Device_Delete(request, Device_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = '''SELECT Device_ID FROM tbl_device
			   WHERE Device_ID = %s'''
	parameter = (Device_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Device_ID = results[0]
		query = '''DELETE FROM tbl_device
				   WHERE Device_ID = %s'''
		parameter = (Device_ID,)
		Cursor.execute(query, parameter)
		Connector.commit()
		notification_messages.success(request, f'Device_ID = {Device_ID} was deleted successfully.')
		return redirect('/device/')
	except TypeError:
		notification_messages.warning(request, f'Device_ID = {Device_ID} does not exist.')
		return redirect('/device/')

	return redirect('/device/')




def Get_All_Wearer_For_Portal(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = 'SELECT * FROM tbl_wearer'
	Cursor.execute(query)

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
	url = 'http://52.237.83.22:5050/wearers/'
	response = requests.get(url)
	data = response.json()['Wearer']

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')




	return render(request,
				  'portal/wearer/wearer.html',
				  {'note': 'Device Page',
				   'data': data,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Wearer_Create(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	if request.method == 'POST':
		form = WearerCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Wearer_Nick = data.get('Wearer_Nick')
			query = '''
				INSERT INTO tbl_wearer (Wearer_ID, Wearer_Nick)
			   	VALUES ((SELECT Create_PK("WER")), %s)'''
			parameters = (Wearer_Nick,)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/wearer/')
	else:
		form = WearerCreateForm()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/wearer/create_wearer.html',
				  {'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Wearer_Update(request, Wearer_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = '''SELECT Wearer_ID FROM tbl_wearer
			   WHERE Wearer_ID = %s'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Wearer_ID = results[0]
	except TypeError:
		notification_messages.warning(request, f'Wearer_ID = {Wearer_ID} does not exist.')
		return redirect('/wearer/')

	if request.method == 'POST':
		form = WearerUpdateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Wearer_Nick = data.get('Wearer_Nick')

			query = '''
				UPDATE  tbl_wearer
			   	SET Wearer_Nick = %s
			   	WHERE Wearer_ID = %s'''
			parameters = (Wearer_Nick, Wearer_ID)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/wearer/')
	else:
		form = WearerUpdateForm()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/wearer/update_wearer.html',
				  {'results': Wearer_ID,
				   'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Wearer_Delete(request, Wearer_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = '''SELECT Wearer_ID FROM tbl_wearer
			   WHERE Wearer_ID = %s'''
	parameter = (Wearer_ID,)
	Cursor.execute(query, parameter)
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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = 'SELECT * FROM tbl_gateway'
	Cursor.execute(query)

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
	url = 'http://52.237.83.22:5050/gateways/'
	response = requests.get(url)
	data = response.json()['Gateway']

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/gateway/gateway.html',
				  {'note': 'Device Page',
				   'data': data,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Gateway_Create(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
			query = '''
				INSERT INTO tbl_gateway
				(Gateway_ID, Gateway_Location,
			   	Gateway_Address, Gateway_Mac, Gateway_Serial_No,
			   	Gateway_Topic, Gateway_Latitude, Gateway_Longitude,
			   	Gateway_Type)
			   	VALUES ((SELECT Create_PK("GTE")), %s, %s, %s, %s, %s, %s, %s, %s)'''
			parameters = (Gateway_Location,
			   			  Gateway_Address, Gateway_Mac, Gateway_Serial_No,
			   			  Gateway_Topic, Gateway_Latitude, Gateway_Longitude,
			   			  Gateway_Type)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/gateway/')
	else:
		form = GatewayCreateForm()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/gateway/create_gateway.html',
				  {'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Gateway_Update(request, Gateway_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = '''SELECT Gateway_ID FROM tbl_gateway
			   WHERE Gateway_ID = %s'''
	parameter = (Gateway_ID,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchone()
	try:
		Gateway_ID = results[0]
	except TypeError:
		notification_messages.warning(request, f'Gateway_ID = {Gateway_ID} does not exist.')
		return redirect('/gateway/')

	if request.method == 'POST':
		form = GatewayCreateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Gateway_Location = data.get('Gateway_Location')
			Gateway_Address = data.get('Gateway_Address')
			Gateway_Mac = data.get('Gateway_Mac')
			Gateway_Serial_No = data.get('Gateway_Serial_No')
			Gateway_Topic = data.get('Gateway_Topic')

			query = '''
				UPDATE  tbl_gateway
			   	SET Gateway_Location = %s,
			   		Gateway_Address = %s,
			   		Gateway_Mac = %s,
			   		Gateway_Serial_No = %s,
			   		Gateway_Topic = %s
			   	WHERE Gateway_ID = %s'''
			parameters = (Gateway_Location, Gateway_Address,
						  Gateway_Mac, Gateway_Serial_No, Gateway_Topic, Gateway_ID)
			Cursor.execute(query, parameters)
			Connector.commit()
			return redirect('/gateway/')
	else:
		form = GatewayCreateForm()

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/gateway/update_gateway.html',
				  {'results': Gateway_ID,
				   'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})



def Gateway_Delete(request, Gateway_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

	Cursor = Connector.cursor()

	query = '''SELECT Gateway_ID FROM tbl_gateway
			   WHERE Gateway_ID = %s'''
	parameter = (Gateway_ID,)
	Cursor.execute(query, parameter)
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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/message/message.html',
				  {'note': 'Message Page',
				   'data': data,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Message_Create(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/message/create_message.html',
				  {'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Message_Delete(request, Message_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/subscription/subscription.html',
				  {'note': 'Message Page',
				   'data': data,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})


@login_required
def Subscription_Create(request):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/subscription/create_subscription.html',
				  {'form': form,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})



def Subscription_Delete(request, Subscription_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
	# url = 'http://52.237.83.22:5050/alerts/'
	# response = requests.get(url)
	# data = response.json()['Alert']

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
	print(data)

	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data2 = response.json()['Alert'][:5]

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'portal/alert/alert.html',
				  {'note': 'Alert Page',
				   'data': data,
				   'latest_altert': data2,
				   'gateways': gateways,
				   'wearers': wearers})



def Alert_Delete(request, Alert_ID):
	Connector = mysql.connect(
		user=os.getenv('BluguardDB_User'),
		password=os.getenv('BluguardDB_Pwd'),
		host='localhost',
		port=os.getenv('BluguardDB_Port'),
		database=os.getenv('BluguardDB_Name')
	)

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
	url = 'http://52.237.83.22:5050/alerts/'
	response = requests.get(url)
	data = response.json()['Alert']

	gateways = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_gateway')
	wearers = Fetch_Total_Rows('SELECT COUNT(*) FROM tbl_wearer')



	return render(request,
				  'latest_alert.html',
				  {'note': 'Alert Page',
				   'data': data,
				   'gateways': gateways,
				   'wearers': wearers})


