from django.conf import settings
import os
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("perfil/", include("perfil.urls")),
]

if settings.DEBUG or os.getenv("SERVE_MEDIA", "1") == "1":
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
