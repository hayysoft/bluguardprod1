from django.urls import path

from .mobile_app_api_views import (
	Vital_Surveillance,
	Wearers_Details,
	Get_Device_Details,
	Alerts_Details,
	Get_Alert_Details,
	Quanrantine_Surveillance_Data,
	Invidual_Quarantine,

	Support,
	Get_User_Message,
	logout_page,
)


urlpatterns = [
	path('Vital_Surveillance/<str:User_ID>/', Vital_Surveillance),
	path('Wearers_Details/<str:User_ID>/', Wearers_Details),
	path('Get_Device_Details/<str:Device_Mac>/', Get_Device_Details),

	path('Alerts_Details/<str:User_ID>/', Alerts_Details),
	path('Get_Alert_Details/<str:User_ID>/<str:Wearer_ID>/', Get_Alert_Details),
	path('Quanrantine_Surveillance_Data/<str:User_ID>/', Quanrantine_Surveillance_Data),

	path('Invidual_Quarantine/<str:Wearer_ID>/', Invidual_Quarantine),

	path('Get_User_Message/<str:Wearer_ID>/', Get_User_Message),
	path('Support/', Support),
	path('logout/', logout_page),
]