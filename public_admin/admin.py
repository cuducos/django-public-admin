from django.contrib.admin import ModelAdmin
from public_admin.sites import PublicAdminSite


class PublicModelAdmin(ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.method == "GET"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        return [url for url in super().get_urls() if PublicAdminSite.valid_url(url)]
