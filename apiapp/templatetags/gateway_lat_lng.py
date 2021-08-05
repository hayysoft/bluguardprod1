from django.utils.safestring import mark_safe
from django import template

import os
import json
import random
import requests
import mysql.connector as mysql


register = template.Library()


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


@register.simple_tag(name='top_five_alerts')
def top_five_alerts():
    Connector = mysql.connect(**config)

    Cursor = Connector.cursor()

    query = '''
        SELECT Alert_Date, Alert_Time, Device_ID, Alert_Reading, Alert_Code
        FROM tbl_alert ORDER BY Alert_Time DESC LIMIT 5;
    '''
    Cursor.execute(query)
    results = Cursor.fetchall()

    data = [
        {
            'Alert_Date': row[0],
            'Alert_Time': row[1],
            'Device_ID': row[2],
            'Device_Temp': row[3],
            'Alert_Code': row[4]
        } for row in results
    ]


    for index, row in enumerate(results):
        Device_ID = row[2]
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
            data[index]['Wearer_Nick'] = Wearer_Nick
        except LookupError:
            pass

    return data



@register.filter(name='latitude_longitude')
def latitude_longitude(value):
    Connector = mysql.connect(**config)

    Cursor = Connector.cursor()


    query = '''
        SELECT Gateway_Location, Gateway_Address,
               Gateway_Latitude, Gateway_Longitude,
               Gateway_Status, Username
        FROM tbl_gateway;
    '''
    Cursor.execute(query)
    results = Cursor.fetchall()

    gateway_lat_lng = []

    for row in results:
        username = row[5]
        query = '''
            SELECT COUNT(*) AS Offline_Devices FROM TBL_Device
            WHERE Username IN (
                SELECT Username FROM TBL_Gateway
                WHERE Username = %s
            ) AND
            Device_Status = %s;
        '''
        parameters = (username, 'OFFLINE')
        Cursor.execute(query, parameters)
        offline_devices = dictfetchall(Cursor)
        offline_devices = offline_devices[0]['Offline_Devices']


        query = '''
            SELECT COUNT(*) AS Online_Devices FROM TBL_Device
            WHERE Username IN (
                SELECT Username FROM TBL_Gateway
                WHERE Username = %s
            ) AND
            Device_Status = %s;
        '''
        parameters = (username, 'ONLINE')
        Cursor.execute(query, parameters)
        online_devices = dictfetchall(Cursor)
        online_devices = online_devices[0]['Online_Devices']


        row_0_1 = row[0] + ' - ' + row[1] + f'.       OFFLINE-Devices: {offline_devices}         ONLINE-Devies: {online_devices}'
        row_2 = row[2]
        row_3 = row[3]
        row_4 = random.randint(1, 6)
        row_icon = 'http://52.237.83.22:5050/static/Gateway_Icons/red-icon2-removebg.png' if row[4] == 'OFFLINE' else 'http://52.237.83.22:5050/static/Gateway_Icons/blue-icon2-removebg.png'
        gateway_lat_lng.append([row_0_1, row_2, row_3, row_4, row_icon, username])


    # gateway_lat_lng = [
    #     [
    #         row[0] + ' - ' + row[1],
    #         row[2],
    #         row[3],
    #         random.randint(1, 6),

    #     ] for row in results
    # ]

    return mark_safe(json.dumps(gateway_lat_lng))
