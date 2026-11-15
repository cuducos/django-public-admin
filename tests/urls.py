from django.urls import path

from public_admin.sites import HAS_IMPORT_EXPORT

urlpatterns = []

if HAS_IMPORT_EXPORT:
    from tests.drinks import public_admin

    urlpatterns.append(path("dashboard/", public_admin.urls))
