from django.contrib import admin

from .models import (
    TblAcknowledgement, TblAlert, TblAlertCode,
    TblIncoming, TblSubscription, TblUser, TblCrestPatient,
    TblDailySurvey, TblDevice, TblDeviceRawLength,
    TblGateway, TblMessage, TblOrganization,
    TblWearer
)



@admin.register(TblAcknowledgement)
class TblAcknowledgementAdmin(admin.ModelAdmin):
    list_display = ['ack_id', 'user',
                    'ack_date', 'ack_time',
                    'alert_id']



@admin.register(TblAlert)
class TblAlertAdmin(admin.ModelAdmin):
	list_display = ['alert_id', 'alert_code',
					'alert_reading', 'alert_date',
					'alert_time', 'device']


@admin.register(TblAlertCode)
class TblAlertCodeAdmin(admin.ModelAdmin):
    list_display = ['alert_code', 'alert_description']





@admin.register(TblIncoming)
class TblIncomingAdmin(admin.ModelAdmin):
	list_display = ['incoming_id', 'incoming_device_mac',
                    'incoming_gateway_mac', 'incoming_temp',
					'incoming_o2', 'incoming_hr',
					'incoming_date', 'incoming_time',
					'device_status', 'incorrect_data_flag',
					'device_bat_level', 'device_rssi']


@admin.register(TblSubscription)
class TblSubscriptionAdmin(admin.ModelAdmin):
	list_display = ['subscription_id', 'user',
					'device', 'subscription_created_date',
                    'subscription_created_time']


@admin.register(TblUser)
class TblUserAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'user_name',
					'user_email', 'user_login',
					'user_pwd', 'org_id']


@admin.register(TblCrestPatient)
class TblCrestPatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'wearer',
                    'patient_tag', 'band_tag',
                    'created_date', 'created_time']


@admin.register(TblDailySurvey)
class TblDailySurveyAdmin(admin.ModelAdmin):
    list_display = ['daily_survey_id', 'daily_survey_q1',
                    'daily_survey_q2_y1', 'daily_survey_q2_y2',
                    'daily_survey_q2_y3', 'daily_survey_q2_y4',
                    'daily_survey_q2_y5', 'daily_survey_q3',
                    'daily_survey_date', 'daily_survey_time',
                    'daily_survey_session', 'wearer']


@admin.register(TblDevice)
class TblDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'device_type',
                    'device_serial_no', 'device_mac',
                    'device_bat_level', 'device_last_updated_date',
                    'device_last_updated_time', 'wearer',
                    'device_temp', 'device_hr',
                    'device_o2', 'incoming_id',
                    'device_rssi', 'gateway_mac',
                    'incorrect_data_flag', 'device_status',
                    'device_tag']


@admin.register(TblDeviceRawLength)
class TblDeviceRawLengthAdmin(admin.ModelAdmin):
    list_display = ['device_type', 'raw_data_length']


@admin.register(TblGateway)
class TblGatewayAdmin(admin.ModelAdmin):
    list_display = ['gateway_id', 'gateway_location',
                    'gateway_address', 'gateway_mac',
                    'gateway_serial_no', 'gateway_topic',
                    'gateway_latitude', 'gateway_longitude',
                    'gateway_type']


@admin.register(TblMessage)
class TblMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'message_description',
                    'message_date', 'message_time',
                    'message_type', 'user',
                    'wearer_id']


@admin.register(TblOrganization)
class TblOrganizationAdmin(admin.ModelAdmin):
    list_display = ['org_id', 'org_name',
                    'org_rep', 'org_rep_email',
                    'org_address']


@admin.register(TblWearer)
class TblWearerAdmin(admin.ModelAdmin):
    list_display = ['wearer_id', 'wearer_nick',
                    'wearer_pwd']
