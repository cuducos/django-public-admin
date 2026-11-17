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


@pytest.mark.parametrize(
    "attrs,allowed",
    (
        ({}, False),
        ({"exclude": ("secret",)}, False),
        ({"fields": ("name",)}, True),
        ({"fieldsets": ((None, {"fields": ("name",)}),)}, True),
    ),
)
def test_object_permission(attrs: dict, allowed: bool) -> None:
    request = RequestFactory().get("/")
    admin = type("Admin", (PublicModelAdmin,), attrs)(Mock(), Mock())
    assert admin.has_view_permission(request, Mock()) is allowed
