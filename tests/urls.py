from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver

from public_admin.sites import HAS_IMPORT_EXPORT
from tests.snacks import SITES

urlpatterns: list[URLPattern | URLResolver] = [
    path(f"{name}/", site.urls) for name, site in SITES.items()
]

if HAS_IMPORT_EXPORT:
    from tests.drinks import public_admin

    urlpatterns.append(path("dashboard/", public_admin.urls))
