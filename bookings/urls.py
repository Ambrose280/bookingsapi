
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions 

schema_view = get_schema_view(
    
	openapi.Info(
        title='WebTuskAPI -> Booking Version',
        default_version='v1',
        description='RestFul API built by Ifiok for Fortune Ishaku',
        terms_of_service='https://www.ambrose280.github.io',
        contact=openapi.Contact(email='ifiokambrose@gmail.com'),
        license=openapi.License(name='Test License')
               ),
        
	public=True,

)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("__reload__/", include("django_browser_reload.urls")),
    path("api/v1/", include("tuskbookings.urls")),
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if 1 > 0:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)