from django.urls import path

from .portal_views import (
	# Portal views
	patient_page,

	set_Q_Device_and_Q_Start,
	set_Q_Device_and_Q_End,
	set_to_assigned_unassigned,
	invidual_quarantine,

	invidual_files,
	device_json_display,

	top_five_alerts_api,
	qrcode_page,
	homepage,
	communication,
	messages,
	login_page,
	logout_page,
	settings_page,
	vitals_page,
	quanrentine_surveilance_page,
	Gateway_Lat_Lng,


	Device_View,
	Device_Create,
	Device_Update,
	Device_Delete,
	Lastest_Device_Data,

	Wearer_View,
	Wearer_Create,
	Wearer_Update,
	Wearer_Delete,

	Online_Gateways,
	Online_Gateways_API,
	Gateway_View,
	Gateway_Create,
	Gateway_Update,
	Gateway_Delete,

	Message_View,
	Message_Create,
	Message_Delete,

	Subscription_View,
	Subscription_Create,
	Subscription_Delete,

	Alert_View,
	Alert_Delete,
	Latest_Alerts_View,
	Get_Latest_Alerts,

	Get_All_Device_For_Portal,
	Get_All_Wearer_For_Portal,
	Get_All_Gateway_For_Portal,
	Get_All_Message_For_Portal,
	Get_All_Subscription_For_Portal,
	Get_All_Alert_For_Portal,
	Quanrantine_Surveillance_Data,
)

app_name = 'apiapp'


urlpatterns = [
	# Portal views
	path('patient_page/', patient_page, name='patient_page'),

	path('set_Q_Device_and_Q_Start/', #<str:Device_ID>/<str:Wearer_ID>/',
		 set_Q_Device_and_Q_Start,
		 name='set_Q_Device_and_Q_Start'),
	path('set_Q_Device_and_Q_End/', #<str:Device_ID>/<str:Wearer_ID>/',
		 set_Q_Device_and_Q_End,
		 name='set_Q_Device_and_Q_End'),
	path('set_to_assigned_unassigned/<str:wearer_id>/', set_to_assigned_unassigned),
	path('invidual_quarantine/<str:wearer_id>/', invidual_quarantine,
		 name='invidual_quarantine'),

	path('invidual_files/', invidual_files, name='invidual_files'),
	path('device_json_display/<str:file>/', device_json_display,
		 name='device_json_display'),

	path('top_five_alerts_api/', top_five_alerts_api),
	path('download-bg37/', qrcode_page, name='qrcode_page'),
	path('', homepage, name='homepage'),
	path('communication/', communication, name='communication'),
	path('messages/', messages, name='messages'),
	path('login/', login_page, name='login_page'),
	path('logout/', logout_page, name='logout_page'),
	path('settings/', settings_page, name='settings_page'),
	path('vitals/', vitals_page, name='vitals_page'),
	path('quanrentine_surveilance_page/', quanrentine_surveilance_page,
		 name='quanrentine_surveilance_page'),
	path('Gateway_Lat_Lng/', Gateway_Lat_Lng),

	path('device/', Device_View, name='device'),
	path('device-create/', Device_Create, name='Device_Create'),
	path('device-update/<str:Device_ID>/', Device_Update, name='Device_Update'),
	path('device-delete/<str:Device_ID>/', Device_Delete, name='Device_Delete'),
	path('Lastest_Device_Data/', Lastest_Device_Data),
	path('devices/', Get_All_Device_For_Portal),

	path('wearer/', Wearer_View, name='wearer'),
	path('wearer-create/', Wearer_Create, name='Wearer_Create'),
	path('wearer-update/<str:Wearer_ID>/', Wearer_Update, name='Wearer_Update'),
	path('wearer-delete/<str:Wearer_ID>/', Wearer_Delete, name='Wearer_Delete'),
	path('wearers/', Get_All_Wearer_For_Portal),

	path('online-gateways/', Online_Gateways, name='Online_Gateways'),
	path('online-gateways-api/', Online_Gateways_API),
	path('gateway/', Gateway_View, name='gateway'),
	path('gateway-create/', Gateway_Create, name='Gateway_Create'),
	path('gateway-update/<str:Gateway_ID>/', Gateway_Update, name='Gateway_Update'),
	path('gateway-delete/<str:Gateway_ID>/', Gateway_Delete, name='Gateway_Delete'),
	path('gateways/', Get_All_Gateway_For_Portal),


	path('message/', Message_View, name='message'),
	path('message-create/', Message_Create, name='Message_Create'),
	path('message-delete/<str:Message_ID>/', Message_Delete, name='Message_Delete'),
	path('get-messages/', Get_All_Message_For_Portal),

	path('subscription/', Subscription_View, name='subscription'),
	path('subscription-create/', Subscription_Create, name='Subscription_Create'),
	path('subscription-delete/<str:Subscription_ID>/', Subscription_Delete,
												name='Subscription_Delete'),
	path('subscriptions/', Get_All_Subscription_For_Portal),

	path('alert/', Alert_View, name='alert'),
	path('alert-delete/<str:Alert_ID>/', Alert_Delete, name='Alert_Delete'),
	path('alerts/', Get_All_Alert_For_Portal),
	path('latest_alerts_view/', Latest_Alerts_View, name='Latest_Alerts_View'),
	path('Get_Latest_Alerts/', Get_Latest_Alerts),

	path('Quanrantine_Surveillance_Data/',
		 Quanrantine_Surveillance_Data),
]

