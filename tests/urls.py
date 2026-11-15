from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver

from public_admin.sites import HAS_IMPORT_EXPORT

urlpatterns: list[URLPattern | URLResolver] = []

if HAS_IMPORT_EXPORT:
    from tests.drinks import public_admin

    urlpatterns.append(path("dashboard/", public_admin.urls))
