from typing import ClassVar

from django.db import models
from django.db.models import Manager

from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp


class Snack(models.Model):
    name = models.CharField(max_length=32)
    secret = models.CharField(max_length=32)
    objects: ClassVar[Manager]

    class Meta:
        app_label = "tests"


class SnackAdmin(PublicModelAdmin):
    fields = ("name",)


open_site = PublicAdminSite("open", PublicApp("tests", ("snack",)))
open_site.register(Snack, SnackAdmin)
closed_site = PublicAdminSite("closed", PublicApp("tests", ("snack",)))
closed_site.register(Snack, PublicModelAdmin)
