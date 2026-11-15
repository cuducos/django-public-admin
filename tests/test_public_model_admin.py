from unittest.mock import Mock

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
