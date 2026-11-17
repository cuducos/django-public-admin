from typing import ClassVar

from django.db import models
from django.db.models import Manager

from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp


class Person(models.Model):
    name = models.CharField(max_length=32)
    objects: ClassVar[Manager]

    class Meta:
        app_label = "tests"

    def __str__(self) -> str:
        return f"Person {self.name}"


class Snack(models.Model):
    name = models.CharField(max_length=32)
    secret = models.CharField(max_length=32)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    objects: ClassVar[Manager]

    class Meta:
        app_label = "tests"


class ListDisplayAdmin(PublicModelAdmin):
    list_display = ("name",)


class ExcludeAdmin(PublicModelAdmin):
    exclude = ("secret", "owner")


class FieldsAdmin(PublicModelAdmin):
    fields = ("name",)


class FieldsetsAdmin(PublicModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)


SITES = {
    admin.__name__: PublicAdminSite(
        admin.__name__, PublicApp("tests", ("snack", "person"))
    )
    for admin in (ListDisplayAdmin, ExcludeAdmin, FieldsAdmin, FieldsetsAdmin)
}
for admin in (ListDisplayAdmin, ExcludeAdmin, FieldsAdmin, FieldsetsAdmin):
    SITES[admin.__name__].register(Snack, admin)
    SITES[admin.__name__].register(Person, PublicModelAdmin)
