from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-user/', include('accounts.urls')),
    path('api-animals/', include('animals.urls')),
    path('api-content/', include('content.urls')),
    path('api-chats/', include('chats.urls')),
    path("api-auth/", include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
