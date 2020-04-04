from public_admin.sites import PublicAdminSite
from public_admin.sites import PublicApp


PUBLIC_APPS = (
    PublicApp("my_open_house", ("beverage", "snack")),
    PublicApp("library", ("book", "journal")),
)


def test_init(mocker):
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    assert not public_admin.actions
    assert not public_admin._global_actions
    assert public_admin.name == "dashboard"


def test_valid_url(mocker):
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    valid, invalid = mocker.MagicMock(), mocker.MagicMock()
    valid.pattern.regex.pattern = "/my_open_house/"
    invalid.pattern.regex.pattern = "/my_open_house/add/"
    assert public_admin.valid_url(valid)
    assert not public_admin.valid_url(invalid)


def test_urls(mocker):
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    get_urls = mocker.patch.object(PublicAdminSite, "get_urls")
    get_urls.return_value = range(3)
    valid_url = mocker.patch.object(PublicAdminSite, "valid_url")
    valid_url.side_effect = (True, False, True)
    assert public_admin.urls == ([0, 2], "admin", "dashboard")


def test_has_permission_get(mocker):
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = mocker.MagicMock()
    request.method = "GET"
    assert public_admin.has_permission(request)


def test_has_permission_post(mocker):
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = mocker.MagicMock()
    request.method = "POST"
    assert not public_admin.has_permission(request)
