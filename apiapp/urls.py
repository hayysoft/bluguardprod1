from django.urls import path

from .views import (
	# GET Methods
	Get_Wearer_Message,
	Get_Wearer_All_Devices,
	Get_Wearer_Alert,
	Get_All_Users_Data,
	Get_All_Users,
	Get_Alert,
	Get_User_Message,
	Get_User_Password,
	Get_User_ID,
	Get_Ack,

	Get_Subscribed_Device,
	Get_Unsubscribed_Device,
	Get_All_Unsubscribed_Device,

	Get_All_Device,
	Get_Wearer,
	Get_Device_Vital,

	Get_Wearer_Survey,
	Get_Patient_Tag_Checkout_Status,


	# Post Methods
	Post_Add_Subscription,
	Post_Change_Password,
	Post_Change_Password_Wearer,
	Post_Change_Email,
	Post_Acknowledgement_Alert,
	Post_User_Login,
	Post_CR03_Registration,
	Post_Data_To_API,
	Post_Wearer_Login,
	Post_Wearer_Survey,
	Delete_Message,

	Post_Creat_Device_Alert,
	Post_Creat_Checkin_Api,

	Crest_CR03_Check_Out_Patient,
	Crest_CR03_Symptoms_Check_In,
)



urlpatterns = [
	# GET Methods
	path('Get_Wearer_Message/<str:Wearer_ID>/',
		 Get_Wearer_Message),
	path('Get_Wearer_All_Devices/<str:Wearer_ID>/',
		 Get_Wearer_All_Devices),
	path('Get_Wearer_Alert/<str:Wearer_ID>/', Get_Wearer_Alert),
	path('Get_All_Users_Data/', Get_All_Users_Data),
	path('Get_All_Users/', Get_All_Users,),
	path('Get_Alert/<str:Wearer_ID>/', Get_Alert),
	path('Get_User_Message/<str:User_id>/', Get_User_Message),
	path('Get_User_Password/<str:User_id>/', Get_User_Password),
	path('Get_User_ID/<str:User_Login>/', Get_User_ID),
	path('Get_Ack/<str:Alert_ID>/', Get_Ack),

	path('Get_Subscribed_Device/<str:User_id>/', Get_Subscribed_Device),
	path('Get_Unsubscribed_Device/<str:User_id>/', Get_Unsubscribed_Device),
	path('Get_All_Unsubscribed_Device/', Get_All_Unsubscribed_Device),

	path('Get_All_Device/', Get_All_Device),
	path('Get_Wearer/<str:Device_ID>/', Get_Wearer),
	path('Get_Device_Vital/<str:Device_ID>/', Get_Device_Vital),


	path('Get_Wearer_Survey/<str:Daily_Survey_Session>/<str:Wearer_ID>/',
		 Get_Wearer_Survey),
	path('Get_Patient_Tag_Checkout_Status/<str:Wearer_ID>/',
		 Get_Patient_Tag_Checkout_Status),

	# POST Methods
	path('Post_Add_Subscription/',
		 Post_Add_Subscription),
	path('Post_Change_Password/',
		 Post_Change_Password),
	path('Post_Change_Password_Wearer/',
		 Post_Change_Password_Wearer),
	path('Post_Change_Email/',
		 Post_Change_Email),
	path('Post_Acknowledgement_Alert/',
		 Post_Acknowledgement_Alert),
	path('Post_User_Login/',
		 Post_User_Login),
	path('Post_CR03_Registration/',
		Post_CR03_Registration),
	path('Post_Data_To_API/',
		 Post_Data_To_API),
	path('Post_Wearer_Login/',
		 Post_Wearer_Login),
	path('Post_Wearer_Survey/', Post_Wearer_Survey),
	path('Delete_Message/', Delete_Message),

	path('Post_Creat_Device_Alert/',
		 Post_Creat_Device_Alert),
	path('Post_Creat_Checkin_Api/',
		 Post_Creat_Checkin_Api),

	path('Crest_CR03_Check_Out_Patient/',
		 Crest_CR03_Check_Out_Patient),
	path('Crest_CR03_Symptoms_Check_In/',
		 Crest_CR03_Symptoms_Check_In),
]
