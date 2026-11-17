from collections.abc import Sequence

from django.contrib.admin import ModelAdmin
from django.db.models import Model
from django.http import HttpRequest
from django.urls.resolvers import URLPattern, URLResolver

from public_admin.sites import PublicAdminSite


class PublicModelAdmin(ModelAdmin):
    """This mimics the Django's native ModelAdmin but filters URLs that should
    not exist in a public admin, and deals with request-based permissions."""

    def has_fields_allowlist(self) -> bool:
        """Whether the fields shown in the object page are explicitly listed
        (in `fields` or `fieldsets`). `exclude` is not enough: any field added
        to the model later would be public by default."""
        return self.fields is not None or self.fieldsets is not None

    def has_view_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        """Only allows view requests if the method is GET. Object pages are
        only allowed if their fields are explicitly listed."""
        if request.method != "GET":
            return False
        return obj is None or self.has_fields_allowlist()

    def get_list_display_links(
        self, request: HttpRequest, list_display: Sequence[str]
    ) -> Sequence[str] | None:
        """Removes links to object pages if they are not allowed."""
        if not self.has_fields_allowlist():
            return None
        return super().get_list_display_links(request, list_display)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Denies permission to any request trying to add new objects."""
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        """Denies permission to any request trying to change objects."""
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        """Denies permission to any request trying to delete objects."""
        return False

    def get_urls(self) -> list[URLResolver | URLPattern]:
        """Filter out the URLs that should not exist in a public admin."""
        return [url for url in super().get_urls() if PublicAdminSite.valid_url(url)]
