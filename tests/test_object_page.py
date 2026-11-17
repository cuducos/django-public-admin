from collections.abc import Iterator

import pytest
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.test import Client

from tests.snacks import Person, Snack


@pytest.fixture(scope="module", autouse=True)
def snack() -> Iterator[Snack]:
    with connection.schema_editor() as schema_editor:
        for model in (ContentType, Person, Snack):
            schema_editor.create_model(model)
    owner = Person.objects.create(name="Ana")
    yield Snack.objects.create(name="Popcorn", secret="Top secret", owner=owner)
    with connection.schema_editor() as schema_editor:
        for model in (Snack, Person, ContentType):
            schema_editor.delete_model(model)


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.parametrize("site", ("ListDisplayAdmin", "ExcludeAdmin"))
def test_object_page_without_fields_allowlist(client, snack, site) -> None:
    response = client.get(f"/{site}/tests/snack/{snack.pk}/change/")
    assert response.status_code == 403
    assert "Top secret" not in response.content.decode()


@pytest.mark.parametrize("site", ("ListDisplayAdmin", "ExcludeAdmin"))
def test_changelist_without_fields_allowlist(client, snack, site) -> None:
    response = client.get(f"/{site}/tests/snack/")
    assert response.status_code == 200
    assert ("Popcorn" if site == "ListDisplayAdmin" else str(snack)) in (
        response.content.decode()
    )
    assert f"/snack/{snack.pk}/change/" not in response.content.decode()


@pytest.mark.parametrize("site", ("FieldsAdmin", "FieldsetsAdmin"))
def test_object_page_with_fields_allowlist(client, snack, site) -> None:
    response = client.get(f"/{site}/tests/snack/{snack.pk}/change/")
    content = response.content.decode()
    assert response.status_code == 200
    assert "Popcorn" in content
    assert "Top secret" not in content
    assert "Secret" not in content
    assert "Person Ana" not in content
    assert "/person/1/change/" not in content


@pytest.mark.parametrize("site", ("FieldsAdmin", "FieldsetsAdmin"))
def test_changelist_with_fields_allowlist(client, snack, site) -> None:
    response = client.get(f"/{site}/tests/snack/")
    assert f"/snack/{snack.pk}/change/" in response.content.decode()
