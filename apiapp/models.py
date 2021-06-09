# from django.db import models

# import json

# class TblAlertQuerySet(models.QuerySet):
#     def serialize(self):
#         list_values = list(self.values("alert_id", "band_mac", "alert_date",
#                                        "alert_time", "alert_code"))
#         return list_values

# class TblAlertManager(models.Manager):
#     def get_queryset(self):
#         return TblAlertQuerySet(self.model, using=self._db)



# class TblAlert(models.Model):
#     alert_id = models.AutoField(db_column='Alert_Id', primary_key=True)  # Field name made lowercase.
#     band_mac = models.CharField(db_column='Band_Mac', max_length=50)  # Field name made lowercase.
#     alert_date = models.DateField(db_column='Alert_Date', blank=True, null=True)  # Field name made lowercase.
#     alert_time = models.TimeField(db_column='Alert_Time', blank=True, null=True)  # Field name made lowercase.
#     alert_code = models.IntegerField(db_column='Alert_Code')  # Field name made lowercase.

#     objects = TblAlertManager()

#     class Meta:
#         managed = False
#         db_table = 'tbl_alert'
#         verbose_name = 'TBL_Alert'
#         verbose_name_plural = 'TBL_Alert'

#     def __str__(self):
#         return f'TBL_Alert: ID = {self.alert_id}'

#     def serialize(self):
#         data = {
#             "alert_id": self.alert_id,
#             "band_mac": self.band_mac,
#             "alert_date": self.alert_date,
#             "alert_time": self.alert_time,
#             "alert_code": alert_code
#         }
#         data = json.dumps(data)
#         return data


# class TblDevice(models.Model):
#     device_id = models.AutoField(db_column='Device_Id', primary_key=True)  # Field name made lowercase.
#     last_updated_date = models.DateField(db_column='Last_Updated_Date', blank=True, null=True)  # Field name made lowercase.
#     last_updated_time = models.TimeField(db_column='Last_Updated_Time', blank=True, null=True)  # Field name made lowercase.
#     band_mac = models.CharField(db_column='Band_Mac', unique=True, max_length=50)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'tbl_device'
#         verbose_name = 'TBL_Device'
#         verbose_name_plural = 'TBL_Device'

#     def __str__(self):
#         return f'TBL_Device: ID = {self.device_id}'


# class TblIncoming(models.Model):
#     incoming_id = models.AutoField(db_column='Incoming_Id', primary_key=True)  # Field name made lowercase.
#     date = models.DateField(db_column='Date')  # Field name made lowercase.
#     time = models.TimeField(db_column='Time')  # Field name made lowercase.
#     type = models.CharField(db_column='Type', max_length=50)  # Field name made lowercase.
#     gateway_mac = models.CharField(db_column='Gateway_Mac', max_length=50)  # Field name made lowercase.
#     band_mac = models.CharField(db_column='Band_Mac', max_length=50)  # Field name made lowercase.
#     blename = models.CharField(db_column='BleName', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     rssi = models.IntegerField(db_column='Rssi')  # Field name made lowercase.
#     temperature = models.FloatField(db_column='Temperature')  # Field name made lowercase.
#     heartrate = models.CharField(db_column='HeartRate', max_length=45, blank=True, null=True)  # Field name made lowercase.
#     batterylevel = models.IntegerField(db_column='BatteryLevel', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'tbl_incoming'
#         verbose_name = 'TBL_Incoming'
#         verbose_name_plural = 'TBL_Incoming'

#     def __str__(self):
#         return f'TBL_Incoming: ID = {self.incoming_id}'



# class TblSubscriptionQuerySet(models.QuerySet):
#     def serialize(self):
#         list_values = list(self.values("subscription_id", "user",
#                                        "band_mac"))
#         print(list_values)
#         return json.dumps(list_values)

# class TblSubscriptionManager(models.Manager):
#     def get_queryset(self):
#         return TblSubscriptionQuerySet(self.model, using=self._db)


# class TblSubscription(models.Model):
#     subscription_id = models.AutoField(db_column='Subscription_Id', primary_key=True)  # Field name made lowercase.
#     user = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
#     band_mac = models.CharField(db_column='Band_Mac', max_length=45)  # Field name made lowercase.

#     objects = TblSubscriptionManager()

#     class Meta:
#         managed = False
#         db_table = 'tbl_subscription'
#         verbose_name = 'TBL_Subscription'
#         verbose_name_plural = 'TBL_Subscription'

#     def __str__(self):
#         return f'TBL_Subscription: ID = {self.subscription_id}'

#     def serialize(self):
#         data = {
#             "subscription_id": self.subscription_id,
#             "user": self.user,
#             "band_mac": self.band_mac
#         }
#         data = json.dumps(data)
#         return data


# class TblUser(models.Model):
#     user_id = models.AutoField(db_column='User_Id', primary_key=True)  # Field name made lowercase.
#     user_name = models.CharField(db_column='User_Name', max_length=50)  # Field name made lowercase.
#     user_login = models.CharField(db_column='User_LogIn', max_length=50)  # Field name made lowercase.
#     user_pwd = models.CharField(db_column='User_Pwd', max_length=50)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'tbl_user'
#         verbose_name = 'TBL_User'
#         verbose_name_plural = 'TBL_User'

#     def __str__(self):
#         return f'TBL_User: ID = {self.user_id}'
