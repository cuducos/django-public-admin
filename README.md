[![PyPI](https://img.shields.io/pypi/v/django-public-admin)](https://pypi.org/project/django-public-admin/) [![Tests](https://img.shields.io/github/actions/workflow/status/cuducos/django-public-admin/tests.yaml)](https://github.com/cuducos/django-public-admin/actions/workflows/tests.yaml) [![Documentation Status](https://readthedocs.org/projects/django-public-admin/badge/?version=latest)](https://django-public-admin.readthedocs.io/en/latest/?badge=latest) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-public-admin)](https://pypi.org/project/django-public-admin/) [![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-public-admin)](https://pypi.org/project/django-public-admin/)

# Django Public Admin


A public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/). A drop-in replacement for Django's native `AdminSite` and `ModelAdmin` for publicly accessible data. Check the [documentation](https://django-public-admin.readthedocs.io/en/latest/?badge=latest) for more information on how to use it.

## Contributing

We use [`uv`](https://docs.astral.sh/uv/) packaghe manager and `tox` to run tests with different Python ad Django versions. Also we use [Ruff](https://astral.sh/ruff) integrated with the tests (including format checks and linters):

```console
$ uv run tox
```

### Docs

To build the docs we use [Sphinx](https://www.sphinx-doc.org/en/):

```
$ uv run pip install -r docs/requirements.txt
$ uv run sphinx-build docs docs/_build/
```

Them just jump to `docs/_build/index.html`.

## License & Credits

This package is licensed under [MIT license](/LICENSE) and acknowledges [Serenata de Amor](https://github.com/okfn-brasil/serenata-de-amor)’s maintainers and creators: [Open Knowledge Brasil](https://br.okfn.org) and [Data Science Brigade](https://github.com/datasciencebr).
