from django.contrib.admin import ModelAdmin

from public_admin.sites import PublicAdminSite


class PublicModelAdmin(ModelAdmin):
    """This mimics the Django's native ModelAdmin but filters URLs that should
    not exist in a public admin, and deals with request-based permissions."""

    def has_view_permission(self, request, obj=None):
        """Only allows view requests if the method is GET"""
        return request.method == "GET"

    def has_add_permission(self, request):
        """Denies permission to any request trying to add new objects."""
        return False

    def has_change_permission(self, request, obj=None):
        """Denies permission to any request trying to change objects."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Denies permission to any request trying to delete objects."""
        return False

    def get_urls(self):
        """Filter out the URLs that should not exist in a public admin."""
        return [url for url in super().get_urls() if PublicAdminSite.valid_url(url)]
