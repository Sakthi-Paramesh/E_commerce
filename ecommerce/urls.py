from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('accounts/', include('accounts.urls')),
]

# Serve uploaded media files
urlpatterns += [
    path(
        'media/<path:path>',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]