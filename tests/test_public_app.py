from public_admin.sites import PublicApp


def test_public_app():
    public_app = PublicApp("my_open_house", ("beverage", "snack"))
    assert public_app.name == "my_open_house"
    assert public_app.permissions == (
        "my_open_house.view_beverage",
        "my_open_house.view_snack",
    )
