from django import forms
from django.contrib.auth.models import User

import mysql.connector as mysql


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



class CreateWearerForDevice(forms.Form):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Wearer_ID FROM TBL_Wearer
        WHERE Wearer_ID NOT IN (
            SELECT Wearer_ID FROM TBL_Device
        );
    '''
    Cursor.execute(query)
    results = dictfetchall(Cursor)

    Wearer_IDs = []
    for row in results:
        if row['Wearer_ID'] not in Wearer_IDs:
            Wearer_IDs.append(row['Wearer_ID'])

    Wearer_ID_ = []
    for device_type in Wearer_IDs:
        Wearer_ID_.append((
            device_type, device_type
        ))

    Wearer_ID = forms.ChoiceField(
        choices=Wearer_ID_,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }))



class UserUpdateForm(forms.ModelForm):
    # username = forms.CharField(
    #     required=False,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'style': 'width: 300px;'
    #     }))
    password = forms.CharField(
        required=False,
        label='Change password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 300px;'
        }))
    email = forms.EmailField(
        required=False,
        label='Change email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'style': 'width: 300px;'
        }))
    # first_name = forms.CharField(
    #     required=False,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'style': 'width: 300px;'
    #     }))
    # last_name = forms.CharField(
    #     required=False,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'style': 'width: 300px;',
    #         'required': False
    #     }))

    class Meta:
        model = User
        fields = ['password', 'email']



class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 300px;',
            'placeholder': 'Username'
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 300px;',
            'placeholder': 'Password'
        }))



def unique(arr):
    new_arr = []
    for val in arr:
        if val not in new_arr:
            new_arr.append(val)

    return new_arr


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'
    input_formats='%H:%M:%S'

class DeviceCreateForm(forms.Form):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Device_Type, Device_Serial_No FROM TBL_Device
    '''
    Cursor.execute(query)
    results = dictfetchall(Cursor)

    Device_Types = []
    # Device_Serial_Nos = []
    for row in results:
        if row['Device_Type'] not in Device_Types:
            Device_Types.append(row['Device_Type'])

        # if row['Device_Serial_No'] not in Device_Serial_Nos:
        #     Device_Serial_Nos.append(row['Device_Serial_No'])

    Device_Types_ = []
    for device_type in Device_Types:
        Device_Types_.append((
            device_type, device_type
        ))

    # Device_Serial_Nos_ = []
    # for device_serial_No in Device_Serial_Nos:
    #     Device_Serial_Nos_.append((
    #         device_serial_No, device_serial_No
    #     ))


    Device_Type = forms.ChoiceField(
        choices=Device_Types_,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }))

    # Device_Type = forms.CharField(
    # 	label='Device_Type',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control'
    #     }))
    Device_Serial_No = forms.CharField(
    	label='Device_Serial_No',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Device_Mac = forms.CharField(
    	label='Device_Mac',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    # Device_Bat_Level = forms.CharField(
    # 	label='Device_Bat_Level',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control'
    #     }))
    # Device_Last_Updated_Date = forms.DateField(
    # 	label='Device_Last_Updated_Date',
    #     widget=DateInput(attrs={
    #         'class': 'form-control'
    #     }))
    # Device_Last_Updated_Time = forms.TimeField(
    # 	label='Device_Last_Updated_Time',
    #     widget=TimeInput(attrs={
    #         'class': 'form-control',
    #     }))
    # Wearer_ID = forms.CharField(
    # 	label='Wearer_ID',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'required': False,
    #     }))
    # Device_Temp = forms.FloatField(
    # 	label='Device_Temp',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'form-control'
    #     }))
    # Device_HR = forms.FloatField(
    # 	label='Device_HR',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'form-control'
    #     }))
    # Device_O2 = forms.IntegerField(
    # 	label='Device_O2',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'form-control'
    #     }))



class DeviceUpdateForm(forms.Form):
    # Device_Last_Updated_Date = forms.DateField(
    # 	label='Device_Last_Updated_Date',
    #     widget=DateInput(attrs={
    #         'class': 'form-control'
    #     }))
    # Device_Last_Updated_Time = forms.TimeField(
    # 	label='Device_Last_Updated_Time',
    #     widget=TimeInput(attrs={
    #         'class': 'form-control'
    #     }))
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Device_Type, Device_Serial_No FROM TBL_Device
    '''
    Cursor.execute(query)
    results = dictfetchall(Cursor)

    Device_Types = []
    for row in results:
        if row['Device_Type'] not in Device_Types:
            Device_Types.append(row['Device_Type'])

    Device_Types_ = []
    for device_type in Device_Types:
        Device_Types_.append((
            device_type, device_type
        ))



    Device_Type = forms.ChoiceField(
        choices=Device_Types_,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }))
    Device_Serial_No = forms.CharField(
        max_length=50,
    	label='Device_Serial_No',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Device_Mac = forms.CharField(
        max_length=50,
    	label='Device_Mac',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Mac = forms.CharField(
        max_length=50,
        label='Gateway_Mac',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Device_Status = forms.CharField(
        max_length=50,
        label='Device_Status',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Device_Tag = forms.CharField(
        max_length=50,
        label='Device_Tag',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))




class WearerCreateForm(forms.Form):
    Wearer_Nick = forms.CharField(
    	label='Wearer_Nick',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Wearer_Pwd = forms.CharField(
        label='Wearer_Password',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))


class WearerUpdateForm(forms.Form):
    Wearer_Nick = forms.CharField(
    	label='Wearer_Nick',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Wearer_Pwd = forms.CharField(
        label='Wearer_Password',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Status = forms.CharField(
        label='Status',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Patient_Tag_Status = forms.CharField(
        label='Patient_Tag_Status',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))



class GatewayCreateForm(forms.Form):
    Gateway_Location = forms.CharField(
    	label='Gateway_Location',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Address = forms.CharField(
    	label='Gateway_Address',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Mac = forms.CharField(
    	label='Gateway_Mac',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Serial_No = forms.CharField(
    	label='Gateway_Serial_No',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Topic = forms.CharField(
    	label='Gateway_Topic',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Latitude = forms.CharField(
        label='Gateway_Latitude',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Longitude = forms.CharField(
        label='Gateway_Longitude',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Gateway_Type = forms.CharField(
        label='Gateway_Type',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))



class MessageCreateForm(forms.Form):
    Message_Description = forms.CharField(
    	label='Message_Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Message_Date = forms.DateField(
    	label='Message_Date',
        widget=DateInput(attrs={
            'class': 'form-control'
        }))
    Message_Time = forms.TimeField(
    	label='Message_Time',
        widget=TimeInput(attrs={
            'class': 'form-control'
        }))
    Message_Type = forms.CharField(
    	label='Message_Type',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    User_ID = forms.CharField(
    	label='User_ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))




class SubscriptionCreateForm(forms.Form):
    User_ID = forms.CharField(
    	label='User_ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Device_ID = forms.CharField(
    	label='Device_ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    Subscription_Created_Date = forms.DateField(
    	label='Subscription_Created_Date',
        widget=DateInput(attrs={
            'class': 'form-control'
        }))
    Subscription_Created_Time = forms.TimeField(
    	label='Subscription_Created_Time',
        widget=TimeInput(attrs={
            'class': 'form-control'
        }))
