from django.contrib import admin

from .models import (
    TblAcknowledgement, TblAlert, TblAlertCode,
    TblIncoming, TblSubscription
)



@admin.register(TblAcknowledgement)
class TblAcknowledgementdmin(admin.ModelAdmin):
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


# @admin.register(TblUser)
# class TblUserAdmin(admin.ModelAdmin):
# 	list_display = ['user_id', 'user_name',
# 					'user_login',
# 					'user_pwd']

#
