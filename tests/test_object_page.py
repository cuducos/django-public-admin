from collections.abc import Iterator

import pytest
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.test import Client

from tests.snacks import Snack


@pytest.fixture(scope="module", autouse=True)
def snack() -> Iterator[Snack]:
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(ContentType)
        schema_editor.create_model(Snack)
    yield Snack.objects.create(name="Popcorn", secret="Top secret")
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(Snack)
        schema_editor.delete_model(ContentType)


def test_object_page_with_fields(snack: Snack) -> None:
    response = Client().get(f"/open/tests/snack/{snack.pk}/change/")
    assert response.status_code == 200
    assert "Popcorn" in response.content.decode()
    assert "Top secret" not in response.content.decode()


def test_object_page_without_fields(snack: Snack) -> None:
    response = Client().get(f"/closed/tests/snack/{snack.pk}/change/")
    assert response.status_code == 403
    changelist = Client().get("/closed/tests/snack/").content.decode()
    assert f"/snack/{snack.pk}/change/" not in changelist
