from django.utils.safestring import mark_safe
from django import template

import os
import json
import random
import requests
import mysql.connector as mysql


register = template.Library()


@register.simple_tag(name='top_five_alerts')
def top_five_alerts():
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

    # url = 'http://52.237.83.22:5050/alerts/'
    # response = requests.get(url)
    # data = response.json()['Alert'][:5]

    return data



@register.filter(name='latitude_longitude')
def latitude_longitude(value):
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
            row[3],
            random.randint(1, 6)
        ] for row in results
    ]

    return mark_safe(json.dumps(gateway_lat_lng))
