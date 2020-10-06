from django.contrib import admin

from example.my_open_house.models import Beverage, Snack


class BeverageModelAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "alcoholic")
    list_filter = ("alcoholic",)


class SnackModelAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "vegan")
    list_filter = ("vegan",)


admin.site.register(Beverage, BeverageModelAdmin)
admin.site.register(Snack, SnackModelAdmin)
