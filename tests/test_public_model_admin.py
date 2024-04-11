from unittest.mock import Mock

from public_admin.admin import PublicModelAdmin


def test_permissions_with_get():
    request = Mock()
    request.method = "GET"
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert public_model_admin.has_view_permission(request)
    assert not any(
        (
            public_model_admin.has_add_permission(request),
            public_model_admin.has_change_permission(request),
            public_model_admin.has_delete_permission(request),
        )
    )


def test_permissions_with_post():
    request = Mock()
    request.method = "POST"
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert not any(
        (
            public_model_admin.has_view_permission(request),
            public_model_admin.has_add_permission(request),
            public_model_admin.has_change_permission(request),
            public_model_admin.has_delete_permission(request),
        )
    )


def test_urls():
    public_model_admin = PublicModelAdmin(Mock(), Mock())
    assert len(public_model_admin.get_urls()) == 4
