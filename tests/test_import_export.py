from collections.abc import Iterator
from unittest.mock import Mock

from django.db import connection
from django.test import Client, RequestFactory
from pytest import fixture, importorskip, mark

from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp

if importorskip("import_export"):
    from tests.drinks import Drink, DrinkAdmin

URL = "/dashboard/tests/drink/"


@fixture(scope="module", autouse=True)
def drinks() -> Iterator[None]:
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Drink)
    Drink.objects.create(name="Coffee")
    yield
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(Drink)


@fixture
def client() -> Client:
    return Client()


def test_changelist(client: Client) -> None:
    response = client.get(URL)
    assert response.status_code == 200
    assert f"{URL}export/" in response.content.decode()
    assert f"{URL}import/" not in response.content.decode()


def test_export_form(client: Client) -> None:
    assert client.get(f"{URL}export/").status_code == 200


def test_export(client: Client) -> None:
    data = {"format": "0", "resource": "0", "drinkresource_name": "on"}
    response = client.post(f"{URL}export/", data)
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"
    assert "Coffee" in response.content.decode()


@mark.parametrize("view", ("import", "process_import"))
def test_import(client: Client, view: str) -> None:
    assert client.post(f"{URL}{view}/").status_code == 403
    assert Drink.objects.count() == 1


def test_import_form(client: Client) -> None:
    assert client.get(f"{URL}import/").status_code == 403


def test_get_to_custom_view(client: Client) -> None:
    """Custom views are reachable with GET, so they must be read-only. If this
    test breaks, the GET-only rule changed."""
    response = client.get(f"{URL}report/")
    assert response.status_code == 200
    assert response.content.decode() == "1 drinks"


def test_post_to_custom_view_named_like_export(client: Client) -> None:
    assert client.post(f"{URL}report_export/").status_code == 403
    assert Drink.objects.count() == 1


def test_changelist_post(client: Client) -> None:
    assert client.post(URL).status_code == 403


def test_has_permission_post_to_export() -> None:
    public_admin = PublicAdminSite("dashboard", PublicApp("tests", ("drink",)))
    public_admin.register(Drink, DrinkAdmin)
    request = RequestFactory().post("/")
    request.resolver_match = Mock(url_name="tests_drink_export")
    assert public_admin.has_permission(request)


def test_has_permission_post_to_export_not_registered() -> None:
    public_admin = PublicAdminSite("dashboard", PublicApp("tests", ("drink",)))
    public_admin.register(Drink, PublicModelAdmin)
    request = RequestFactory().post("/")
    request.resolver_match = Mock(url_name="tests_drink_export")
    assert not public_admin.has_permission(request)
