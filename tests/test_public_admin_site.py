from unittest.mock import Mock, patch

import pytest
from django.db import models

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


def test_init():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    assert not public_admin.actions
    assert not public_admin._global_actions
    assert public_admin.name == "dashboard"


def test_valid_url():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    valid, invalid = Mock(), Mock()
    valid.pattern.regex.pattern = "/my_open_house/"
    invalid.pattern.regex.pattern = "/my_open_house/add/"
    assert public_admin.valid_url(valid)
    assert not public_admin.valid_url(invalid)


def test_urls():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    with patch.object(PublicAdminSite, "get_urls") as get_urls:
        get_urls.return_value = range(3)
        with patch.object(PublicAdminSite, "valid_url") as valid_url:
            valid_url.side_effect = (True, False, True)
            assert public_admin.urls == ([0, 2], "admin", "dashboard")


def test_has_permission_get():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = Mock()
    request.method = "GET"
    assert public_admin.has_permission(request)


def test_has_permission_post():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    request = Mock()
    request.method = "POST"
    assert not public_admin.has_permission(request)


def test_authorized_model_can_be_registered():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    public_admin.register(Beverage)


def test_non_authorized_model_cannot_be_registered():
    public_admin = PublicAdminSite("dashboard", PUBLIC_APPS)
    with pytest.raises(UnauthorizedModelError):
        public_admin.register(Music)
