from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from public_admin.admin import PublicModelAdmin


def test_permissions_with_get() -> None:
    request = RequestFactory().get("/")
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert public_model_admin.has_view_permission(request)
    assert not any(
        (
            public_model_admin.has_add_permission(request),
            public_model_admin.has_change_permission(request),
            public_model_admin.has_delete_permission(request),
        )
    )


def test_permissions_with_post() -> None:
    request = RequestFactory().post("/")
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert not any(
        (
            public_model_admin.has_view_permission(request),
            public_model_admin.has_add_permission(request),
            public_model_admin.has_change_permission(request),
            public_model_admin.has_delete_permission(request),
        )
    )


def test_urls() -> None:
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert len(public_model_admin.get_urls()) == 4


def test_object_permission_without_fields_allowlist() -> None:
    request = RequestFactory().get("/")
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert public_model_admin.has_view_permission(request)
    assert not public_model_admin.has_view_permission(request, Mock())
    assert public_model_admin.get_list_display_links(request, ("name",)) is None


@pytest.mark.parametrize(
    "attrs",
    (
        {"fields": ("name",)},
        {"fieldsets": ((None, {"fields": ("name",)}),)},
    ),
)
def test_object_permission_with_fields_allowlist(attrs: dict) -> None:
    request = RequestFactory().get("/")
    admin_class = type("Admin", (PublicModelAdmin,), attrs)
    public_model_admin = admin_class(Mock(), Mock())
    assert public_model_admin.has_view_permission(request, Mock())
    assert public_model_admin.get_list_display_links(request, ("name",)) == ["name"]


def test_object_permission_with_exclude() -> None:
    request = RequestFactory().get("/")
    admin_class = type("Admin", (PublicModelAdmin,), {"exclude": ("secret",)})
    public_model_admin = admin_class(Mock(), Mock())
    assert not public_model_admin.has_view_permission(request, Mock())
