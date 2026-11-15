from typing import ClassVar

from django.db import models
from django.db.models import Manager
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.urls.resolvers import URLPattern
from import_export.admin import ImportExportMixin

from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp


class Drink(models.Model):
    name = models.CharField(max_length=32)
    objects: ClassVar[Manager]

    class Meta:
        app_label = "tests"


class DrinkAdmin(ImportExportMixin, PublicModelAdmin):
    def get_urls(self) -> list[URLPattern]:
        urls = [
            path(
                "report/",
                self.admin_site.admin_view(self.report),
                name="tests_drink_report",
            ),
            path(
                "report_export/",
                self.admin_site.admin_view(self.report_export),
                name="tests_drink_report_export",
            ),
        ]
        return urls + super().get_urls()

    def report(self, request: HttpRequest) -> HttpResponse:
        """A custom read-only view."""
        return HttpResponse(f"{Drink.objects.count()} drinks")

    def report_export(self, request: HttpRequest) -> HttpResponse:
        """A custom view whose name ends in `_export` but writes on POST."""
        Drink.objects.create(name="Anonymous POST wrote this")
        return HttpResponse()


public_admin = PublicAdminSite("dashboard", PublicApp("tests", ("drink",)))
public_admin.register(Drink, DrinkAdmin)
