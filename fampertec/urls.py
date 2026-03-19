from django.conf import settings
import os
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("perfil/", include("perfil.urls")),
]

if settings.DEBUG or os.getenv("SERVE_MEDIA", "0") == "1":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
