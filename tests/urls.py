from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver

from public_admin.sites import HAS_IMPORT_EXPORT
from tests.snacks import closed_site, open_site

urlpatterns: list[URLPattern | URLResolver] = [
    path("open/", open_site.urls),
    path("closed/", closed_site.urls),
]

if HAS_IMPORT_EXPORT:
    from tests.drinks import public_admin

    urlpatterns.append(path("dashboard/", public_admin.urls))
