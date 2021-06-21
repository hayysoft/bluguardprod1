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

@register.simple_tag(name='top_five_alerts')
def top_five_alerts():
    Connector = mysql.connect(**config)

    Cursor = Connector.cursor()

    query = '''
        SELECT Alert_Date, Alert_Time, Alert_Reading, Device_ID
        FROM tbl_alert ORDER BY Alert_Time DESC LIMIT 6;
    '''
    Cursor.execute(query)
    results = Cursor.fetchall()

    data = [
        {
            'Alert_Date': row[0],
            'Alert_Time': row[1],
            'Device_Temp': row[2],
            'Device_ID': row[3]
        } for row in results
    ]






    for index, row in enumerate(results):
        Device_ID = row[3]
        query = '''
            SELECT Wearer_ID FROM tbl_device
            WHERE Device_ID = %s
        '''
        parameter = (Device_ID,)
        Cursor.execute(query, parameter)
        Fetch_Results = Cursor.fetchall()

        # Temp = Fetch_Results[0][0]
        # data[index]['Device_Temp'] = Temp

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
