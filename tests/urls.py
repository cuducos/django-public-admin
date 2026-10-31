from django.db import models
from django.urls import path
from import_export.admin import ImportExportMixin

from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp


class Drink(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        app_label = "tests"


class DrinkAdmin(ImportExportMixin, PublicModelAdmin):
    pass


public_admin = PublicAdminSite("dashboard", PublicApp("tests", ("drink",)))
public_admin.register(Drink, DrinkAdmin)

urlpatterns = [path("dashboard/", public_admin.urls)]
