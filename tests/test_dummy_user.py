from public_admin.sites import DummyUser, PublicApp

PUBLIC_APPS = (
    PublicApp("my_open_house", ("beverage", "snack")),
    PublicApp("library", ("book", "journal")),
)


def test_has_module_permissions():
    user = DummyUser(PUBLIC_APPS)
    assert user.has_module_perms("my_open_house")
    assert user.has_module_perms("library")
    assert not user.has_module_perms("core")


def test_has_permissions():
    user = DummyUser(PUBLIC_APPS)
    assert user.has_perm("my_open_house.view_beverage")
    assert user.has_perm("my_open_house.view_snack")
    assert not user.has_perm("my_open_house.view_bedroom")
    assert user.has_perm("library.view_book")
    assert user.has_perm("library.view_journal")
    assert not user.has_perm("library.view_fine")
