from example.my_open_house.models import Beverage, Snack
from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp


class BeverageModelAdmin(PublicModelAdmin):
    list_display = ("name", "amount", "alcoholic")
    list_filter = ("alcoholic",)


class SnackModelAdmin(PublicModelAdmin):
    list_display = ("name", "amount", "vegan")
    list_filter = ("vegan",)


public_app = PublicApp("my_open_house", models=("Beverage", "Snack"))
public_admin = PublicAdminSite("dashboard", public_app)
public_admin.register(Beverage, BeverageModelAdmin)
public_admin.register(Snack, SnackModelAdmin)
