# cozycornercafe/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Ensure this is imported
from django.conf.urls.static import static # Ensure this is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cafe_core.urls', namespace='cafe_core')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
