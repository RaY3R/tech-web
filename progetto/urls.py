from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from progetto import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('insertion/', include('insertion.urls')),
    path('api/', include('api.urls')),
    path('', include('user.urls')),
    path("__reload__/", include("django_browser_reload.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
