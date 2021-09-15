from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apiapp.urls')),
   	path('', include('apiapp.portal_urls', namespace='apiapp')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth-login/', include('rest_framework.urls')),

    path('api/v1/app/', include('apiapp.mobile_app_urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL,
            document_root=settings.STATIC_ROOT)

