from unittest.mock import Mock, patch

from django.db import models
from django.test import RequestFactory
from django.urls import path
from pytest import raises

from public_admin.exceptions import UnauthorizedModelError
from public_admin.sites import PublicAdminSite, PublicApp


class Beverage(models.Model):
    class Meta:
        app_label = "my_open_house"


class Music(models.Model):
    class Meta:
        app_label = "my_open_house"


PUBLIC_APPS = (
    PublicApp("my_open_house", ("beverage", "snack")),
    PublicApp("library", ("book", "journal")),
)


def test_init() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    assert not public_admin.actions
    assert not public_admin._global_actions
    assert public_admin.name == "dashboard"


def test_valid_url() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    valid, invalid = path("my_open_house/", Mock()), path("my_open_house/add/", Mock())
    assert public_admin.valid_url(valid)
    assert not public_admin.valid_url(invalid)


def test_urls() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    with patch.object(PublicAdminSite, "get_urls") as get_urls:
        get_urls.return_value = range(3)
        with patch.object(PublicAdminSite, "valid_url") as valid_url:
            valid_url.side_effect = (True, False, True)
            assert public_admin.urls == ([0, 2], "admin", "dashboard")


def test_has_permission_get() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = RequestFactory().get("/")
    assert public_admin.has_permission(request)


def test_has_permission_post() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = RequestFactory().post("/")
    request.resolver_match = Mock(url_name="my_open_house_beverage_changelist")
    assert not public_admin.has_permission(request)


def test_has_permission_without_resolver_match() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = RequestFactory().get("/")
    request.resolver_match = None
    assert public_admin.has_permission(request)
    request.method = "POST"
    assert not public_admin.has_permission(request)


def test_authorized_model_can_be_registered() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    public_admin.register(Beverage)


def test_non_authorized_model_cannot_be_registered() -> None:
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    with raises(UnauthorizedModelError):
        public_admin.register(Music)
