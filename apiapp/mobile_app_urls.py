from django.urls import path

from .mobile_app_api_views import (
	Vital_Surveillance,
	Wearers_Details,
	Get_Device_Details,
	Alerts_Details,
	Get_Alert_Details,
)


urlpatterns = [
	path('Vital_Surveillance/', Vital_Surveillance),
	path('Wearers_Details/<str:User_ID>/', Wearers_Details),
	path('Get_Device_Details/<str:Device_Mac>/', Get_Device_Details),

	path('Alerts_Details/<str:User_ID>/', Alerts_Details),
	path('Get_Alert_Details/<str:User_ID>/<str:Wearer_ID>/', Get_Alert_Details),
]