from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from management.views import error_handler
from authentication.views import page_not_found, access_denied

urlpatterns = [
    path('', include('authentication.urls', namespace='authentication')),
    path('mangement/', include('management.urls', namespace='management')),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
handler403 = access_denied
