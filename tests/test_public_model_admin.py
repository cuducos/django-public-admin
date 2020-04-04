from public_admin.admin import PublicModelAdmin


def test_permissions_with_get(mocker):
    request = mocker.MagicMock()
    request.method = "GET"
    public_model_admin = PublicModelAdmin(mocker.Mock(), mocker.Mock())
    assert public_model_admin.has_view_permission(request)
    assert not any(
        (
            public_model_admin.has_add_permission(request),
            public_model_admin.has_change_permission(request),
            public_model_admin.has_delete_permission(request),
        )
    )


def test_permissions_with_post(mocker):
    request = mocker.MagicMock()
    request.method = "POST"
    public_model_admin = PublicModelAdmin(mocker.Mock(), mocker.Mock())
    assert not any(
        (
            public_model_admin.has_view_permission(request),
            public_model_admin.has_add_permission(request),
            public_model_admin.has_change_permission(request),
            public_model_admin.has_delete_permission(request),
        )
    )


def test_urls(mocker):
    public_model_admin = PublicModelAdmin(mocker.Mock(), mocker.Mock())
    assert len(public_model_admin.get_urls()) == 5
