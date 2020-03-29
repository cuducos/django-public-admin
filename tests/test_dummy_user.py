from public_admin.sites import DummyUser


def test_has_module_permissions():
    user = DummyUser(public_apps=("my_open_house",))
    assert user.has_module_perms("my_open_house")
    assert not user.has_module_perms("core")


def test_has_permissions():
    user = DummyUser(public_apps=("my_open_house",), public_models=("beverage",))
    assert user.has_perm("my_open_house.change_beverage")
    assert not user.has_perm("my_open_house.add_beverage")
    assert not user.has_perm("my_open_house.delete_beverage")
