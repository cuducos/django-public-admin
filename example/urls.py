from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from example.my_open_house.public_admin import public_admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", public_admin.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
