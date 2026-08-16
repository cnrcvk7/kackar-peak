from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Django's built-in login/logout/password views (login, logout, etc.)
    path("hesap/", include("django.contrib.auth.urls")),
    path("", include("community.urls")),
]

# Serve uploaded media in development. In production Render handles /media via
# the disk mount + WhiteNoise is for static only, so media works in DEBUG here.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Branding for the admin panel
admin.site.site_header = "Kaçkar Peak Yönetim"
admin.site.site_title = "Kaçkar Peak"
admin.site.index_title = "İçerik Yönetimi"
