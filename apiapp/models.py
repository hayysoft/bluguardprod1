from django.db import models



class TblAcknowledgement(models.Model):
    ack_id = models.CharField(db_column='Ack_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    user = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    ack_date = models.DateField(db_column='Ack_Date')  # Field name made lowercase.
    ack_time = models.TimeField(db_column='Ack_Time')  # Field name made lowercase.
    alert_id = models.CharField(db_column='Alert_ID', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_acknowledgement'

    def __str__(self):
        return f'{self.ack_id}'


class TblAlert(models.Model):
    alert_id = models.CharField(db_column='Alert_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    alert_code = models.ForeignKey('TblAlertCode', models.DO_NOTHING, db_column='Alert_Code')  # Field name made lowercase.
    alert_reading = models.CharField(db_column='Alert_Reading', max_length=10)  # Field name made lowercase.
    alert_date = models.DateField(db_column='Alert_Date', blank=True, null=True)  # Field name made lowercase.
    alert_time = models.TimeField(db_column='Alert_Time', blank=True, null=True)  # Field name made lowercase.
    device = models.ForeignKey('TblDevice', models.DO_NOTHING, db_column='Device_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_alert'

    def __str__(self):
        return f'{self.alert_id}'


class TblAlertCode(models.Model):
    alert_code = models.CharField(db_column='Alert_Code', primary_key=True, max_length=10)  # Field name made lowercase.
    alert_description = models.CharField(db_column='Alert_Description', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_alert_code'

    def __str__(self):
        return f'{self.alert_code}'


class TblCrestPatient(models.Model):
    patient_id = models.CharField(db_column='Patient_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    wearer = models.ForeignKey('TblWearer', models.DO_NOTHING, db_column='Wearer_ID')  # Field name made lowercase.
    patient_tag = models.CharField(db_column='Patient_Tag', max_length=50)  # Field name made lowercase.
    band_tag = models.CharField(db_column='Band_Tag', max_length=50)  # Field name made lowercase.
    created_date = models.DateField(db_column='Created_Date')  # Field name made lowercase.
    created_time = models.TimeField(db_column='Created_Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_crest_patient'

    def __str__(self):
        return f'{self.patient_id}'


class TblDailySurvey(models.Model):
    daily_survey_id = models.CharField(db_column='Daily_Survey_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    daily_survey_q1 = models.IntegerField(db_column='Daily_Survey_Q1', blank=True, null=True)  # Field name made lowercase.
    daily_survey_q2_y1 = models.IntegerField(db_column='Daily_Survey_Q2_Y1', blank=True, null=True)  # Field name made lowercase.
    daily_survey_q2_y2 = models.IntegerField(db_column='Daily_Survey_Q2_Y2', blank=True, null=True)  # Field name made lowercase.
    daily_survey_q2_y3 = models.IntegerField(db_column='Daily_Survey_Q2_Y3', blank=True, null=True)  # Field name made lowercase.
    daily_survey_q2_y4 = models.IntegerField(db_column='Daily_Survey_Q2_Y4', blank=True, null=True)  # Field name made lowercase.
    daily_survey_q2_y5 = models.IntegerField(db_column='Daily_Survey_Q2_Y5', blank=True, null=True)  # Field name made lowercase.
    daily_survey_q3 = models.IntegerField(db_column='Daily_Survey_Q3', blank=True, null=True)  # Field name made lowercase.
    daily_survey_date = models.DateField(db_column='Daily_Survey_Date', blank=True, null=True)  # Field name made lowercase.
    daily_survey_time = models.TimeField(db_column='Daily_Survey_Time', blank=True, null=True)  # Field name made lowercase.
    daily_survey_session = models.CharField(db_column='Daily_Survey_Session', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wearer = models.ForeignKey('TblWearer', models.DO_NOTHING, db_column='Wearer_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_daily_survey'

    def __str__(self):
        return f'{self.daily_survey_id}'


class TblDevice(models.Model):
    device_id = models.CharField(db_column='Device_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    device_type = models.CharField(db_column='Device_Type', max_length=50)  # Field name made lowercase.
    device_serial_no = models.CharField(db_column='Device_Serial_No', max_length=50)  # Field name made lowercase.
    device_mac = models.CharField(db_column='Device_Mac', unique=True, max_length=50)  # Field name made lowercase.
    device_bat_level = models.IntegerField(db_column='Device_Bat_Level', blank=True, null=True)  # Field name made lowercase.
    device_last_updated_date = models.DateField(db_column='Device_Last_Updated_Date', blank=True, null=True)  # Field name made lowercase.
    device_last_updated_time = models.TimeField(db_column='Device_Last_Updated_Time', blank=True, null=True)  # Field name made lowercase.
    wearer = models.ForeignKey('TblWearer', models.DO_NOTHING, db_column='Wearer_ID', blank=True, null=True)  # Field name made lowercase.
    device_temp = models.FloatField(db_column='Device_Temp', blank=True, null=True)  # Field name made lowercase.
    device_hr = models.CharField(db_column='Device_HR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    device_o2 = models.IntegerField(db_column='Device_O2', blank=True, null=True)  # Field name made lowercase.
    incoming_id = models.IntegerField(db_column='Incoming_Id', blank=True, null=True)  # Field name made lowercase.
    device_rssi = models.CharField(db_column='Device_RSSI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gateway_mac = models.CharField(db_column='Gateway_Mac', max_length=45, blank=True, null=True)  # Field name made lowercase.
    incorrect_data_flag = models.IntegerField(db_column='Incorrect_Data_Flag')  # Field name made lowercase.
    device_status = models.CharField(db_column='Device_Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    device_tag = models.CharField(db_column='Device_Tag', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_device'

    def __str__(self):
        return f'{self.device_id}'


class TblDeviceRawLength(models.Model):
    device_type = models.CharField(db_column='Device_Type', primary_key=True, max_length=50)  # Field name made lowercase.
    raw_data_length = models.IntegerField(db_column='Raw_Data_Length')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_device_raw_length'

    def __str__(self):
        return f'{self.device_type}'


class TblGateway(models.Model):
    gateway_id = models.CharField(db_column='Gateway_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    gateway_location = models.CharField(db_column='Gateway_Location', max_length=50)  # Field name made lowercase.
    gateway_address = models.CharField(db_column='Gateway_Address', max_length=50)  # Field name made lowercase.
    gateway_mac = models.CharField(db_column='Gateway_Mac', max_length=50)  # Field name made lowercase.
    gateway_serial_no = models.CharField(db_column='Gateway_Serial_No', max_length=50)  # Field name made lowercase.
    gateway_topic = models.CharField(db_column='Gateway_Topic', max_length=50)  # Field name made lowercase.
    gateway_latitude = models.CharField(db_column='Gateway_Latitude', max_length=50)  # Field name made lowercase.
    gateway_longitude = models.CharField(db_column='Gateway_Longitude', max_length=50)  # Field name made lowercase.
    gateway_type = models.CharField(db_column='Gateway_Type', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_gateway'

    def __str__(self):
        return f'{self.gateway_id}'


class TblIncoming(models.Model):
    incoming_id = models.CharField(db_column='Incoming_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    incoming_device_mac = models.CharField(db_column='Incoming_Device_Mac', max_length=50)  # Field name made lowercase.
    incoming_gateway_mac = models.CharField(db_column='Incoming_Gateway_Mac', max_length=50)  # Field name made lowercase.
    incoming_temp = models.FloatField(db_column='Incoming_Temp')  # Field name made lowercase.
    incoming_o2 = models.IntegerField(db_column='Incoming_O2')  # Field name made lowercase.
    incoming_hr = models.CharField(db_column='Incoming_HR', max_length=45, blank=True, null=True)  # Field name made lowercase.
    incoming_date = models.DateField(db_column='Incoming_Date')  # Field name made lowercase.
    incoming_time = models.TimeField(db_column='Incoming_Time')  # Field name made lowercase.
    device_status = models.CharField(db_column='Device_Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    incorrect_data_flag = models.IntegerField(db_column='Incorrect_Data_Flag', blank=True, null=True)  # Field name made lowercase.
    device_bat_level = models.IntegerField(db_column='Device_Bat_Level', blank=True, null=True)  # Field name made lowercase.
    device_rssi = models.CharField(db_column='Device_RSSI', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_incoming'

    def __str__(self):
        return f'{self.incoming_id}'


class TblMessage(models.Model):
    message_id = models.CharField(db_column='Message_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    message_description = models.CharField(db_column='Message_Description', max_length=100)  # Field name made lowercase.
    message_date = models.DateField(db_column='Message_Date')  # Field name made lowercase.
    message_time = models.TimeField(db_column='Message_Time')  # Field name made lowercase.
    message_type = models.CharField(db_column='Message_Type', max_length=50)  # Field name made lowercase.
    user = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    wearer_id = models.CharField(db_column='Wearer_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_message'

    def __str__(self):
        return f'{self.message_id}'


class TblOrganization(models.Model):
    org_id = models.CharField(db_column='Org_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    org_name = models.CharField(db_column='Org_Name', max_length=50)  # Field name made lowercase.
    org_rep = models.CharField(db_column='Org_Rep', max_length=50)  # Field name made lowercase.
    org_rep_email = models.CharField(db_column='Org_Rep_Email', max_length=50)  # Field name made lowercase.
    org_address = models.CharField(db_column='Org_Address', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_organization'

    def __str__(self):
        return f'{self.org_id}'


class TblSubscription(models.Model):
    subscription_id = models.CharField(db_column='Subscription_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    user = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    device = models.ForeignKey(TblDevice, models.DO_NOTHING, db_column='Device_ID', blank=True, null=True)  # Field name made lowercase.
    subscription_created_date = models.DateField(db_column='Subscription_Created_Date')  # Field name made lowercase.
    subscription_created_time = models.TimeField(db_column='Subscription_Created_Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_subscription'

    def __str__(self):
        return f'{self.subscription_id}'

class TblUser(models.Model):
    user_id = models.CharField(db_column='User_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_Name', max_length=50)  # Field name made lowercase.
    user_email = models.CharField(db_column='User_Email', max_length=50)  # Field name made lowercase.
    user_login = models.CharField(db_column='User_LogIn', max_length=50)  # Field name made lowercase.
    user_pwd = models.CharField(db_column='User_Pwd', max_length=50)  # Field name made lowercase.
    org_id = models.CharField(db_column='Org_ID', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_user'

    def __str__(self):
        return f'{self.user_id}'


class TblWearer(models.Model):
    wearer_id = models.CharField(db_column='Wearer_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    wearer_nick = models.CharField(db_column='Wearer_Nick', unique=True, max_length=50)  # Field name made lowercase.
    wearer_pwd = models.CharField(db_column='Wearer_Pwd', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_wearer'

    def __str__(self):
        return f'{self.wearer_id}'






