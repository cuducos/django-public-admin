from unittest.mock import Mock

import pytest

pytest.importorskip("import_export")

from django.db import connection  # noqa: E402
from django.test import Client  # noqa: E402

from public_admin.admin import PublicModelAdmin  # noqa: E402
from public_admin.sites import PublicAdminSite, PublicApp  # noqa: E402
from tests.drinks import Drink, DrinkAdmin  # noqa: E402

URL = "/dashboard/tests/drink/"


@pytest.fixture(scope="module", autouse=True)
def drinks():
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Drink)
    Drink.objects.create(name="Coffee")
    yield
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(Drink)


@pytest.fixture
def client():
    return Client()


def test_changelist(client):
    assert client.get(URL).status_code == 200


def test_export_form(client):
    assert client.get(f"{URL}export/").status_code == 200


def test_export(client):
    data = {"format": "0", "resource": "0", "drinkresource_name": "on"}
    response = client.post(f"{URL}export/", data)
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"
    assert "Coffee" in response.content.decode()


@pytest.mark.parametrize("view", ("import", "process_import"))
def test_import(client, view):
    assert client.post(f"{URL}{view}/").status_code == 403
    assert Drink.objects.count() == 1


def test_get_to_custom_view(client):
    """Custom views are reachable with GET, so they must be read-only. If this
    test breaks, the GET-only rule changed."""
    response = client.get(f"{URL}report/")
    assert response.status_code == 200
    assert response.content.decode() == "1 drinks"


def test_post_to_custom_view_named_like_export(client):
    assert client.post(f"{URL}report_export/").status_code == 403
    assert Drink.objects.count() == 1


def test_changelist_post(client):
    assert client.post(URL).status_code == 403


def test_has_permission_post_to_export():
    public_admin = PublicAdminSite("dashboard", PublicApp("tests", ("drink",)))
    public_admin.register(Drink, DrinkAdmin)
    request = Mock()
    request.method = "POST"
    request.resolver_match.url_name = "tests_drink_export"
    assert public_admin.has_permission(request)


def test_has_permission_post_to_export_not_registered():
    public_admin = PublicAdminSite("dashboard", PublicApp("tests", ("drink",)))
    public_admin.register(Drink, PublicModelAdmin)
    request = Mock()
    request.method = "POST"
    request.resolver_match.url_name = "tests_drink_export"
    assert not public_admin.has_permission(request)
